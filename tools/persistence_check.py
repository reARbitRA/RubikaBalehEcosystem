#!/usr/bin/env python3
"""Verify that a SPEC-FORGE session has durable, auditable handoff state.

The checker intentionally uses only the Python standard library and git.  It has two modes:

* ``--audit-ledger --clean-tree`` is safe before work starts.  It checks literal path claims in
  append-only ledger entries and verifies that the current checkout is clean.
* ``--receipt --verify-remote`` is the end-of-session receipt.  It repeats the local checks and
  proves that the checked-out branch's HEAD is present on ``origin``.

Repository documents are data.  Ledger parsing therefore recognises only literal repository paths
on lines that make a past-tense creation claim; it never evaluates document content as commands.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


CLAIM_VERB_RE = re.compile(
    r"\b(?:added|created|migrated|wrote|generated|committed|restored|moved)\b",
    re.IGNORECASE,
)
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
BRACE_PATH_RE = re.compile(r"^([^{}]*)\{([^{}]+)\}([^{}]*)$")

# These are paths that are meaningful repository artefacts, rather than shell commands or prose.
# Keep the list deliberately small: a false missing-path report is worse than leaving a prose-only
# statement outside the audit's mechanical scope.
TOP_LEVEL_FILES = {"AGENTS.md", "Makefile", "README.md", ".gitignore"}
TOP_LEVEL_DIRS = {
    ".forge",
    ".github",
    "brainstorm",
    "decisions",
    "knowledge",
    "ops",
    "plans",
    "quality",
    "specs",
    "src",
    "tasks",
    "tests",
    "tools",
    "vision",
}


class CheckResult:
    """Collect human-readable messages while preserving a single success/failure result."""

    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notes: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.failures

    def note(self, message: str) -> None:
        self.notes.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)


def run_git(repo_root: Path, *args: str) -> tuple[int, str, str]:
    """Run git in *repo_root* without interpreting any document content as shell syntax."""

    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def expand_brace_path(value: str) -> Iterable[str]:
    """Expand the one-level ``dir/{A,B}.md`` notation used in legacy ledger entries."""

    match = BRACE_PATH_RE.match(value)
    if not match:
        yield value
        return
    prefix, choices, suffix = match.groups()
    for choice in choices.split(","):
        choice = choice.strip()
        if choice:
            yield f"{prefix}{choice}{suffix}"


def is_literal_repo_path(value: str) -> bool:
    """Return whether *value* is a safe, literal relative path worth auditing."""

    value = value.strip().replace("\\", "/")
    if not value or value.startswith(("/", "~")):
        return False
    if any(token in value for token in ("*", "?", "<", ">", "\n", "\r")):
        return False
    if ".." in value or " " in value:
        return False

    first = value.rstrip("/").split("/", 1)[0]
    if value in TOP_LEVEL_FILES:
        return True
    return first in TOP_LEVEL_DIRS and "/" in value.rstrip("/") or value.rstrip("/") in TOP_LEVEL_DIRS


def claimed_paths(ledger_text: str) -> list[str]:
    """Extract literal file/directory claims from ledger creation statements.

    A ledger is prose, so this deliberately audits a conservative subset: inline-code paths on
    lines that say an artefact was created, added, written, migrated, restored, moved, generated,
    or committed.  It skips globs, ranges, shell commands, and paths mentioned in negative context.
    """

    found: set[str] = set()
    for line in ledger_text.splitlines():
        if not CLAIM_VERB_RE.search(line):
            continue
        for raw in CODE_SPAN_RE.findall(line):
            for candidate in expand_brace_path(raw.strip()):
                candidate = candidate.strip().rstrip(".,:;")
                if is_literal_repo_path(candidate):
                    found.add(candidate.rstrip("/"))
    return sorted(found)


def check_ledger(repo_root: Path, result: CheckResult) -> None:
    ledger = repo_root / ".forge" / "LEDGER.md"
    if not ledger.is_file():
        result.fail("ledger audit: .forge/LEDGER.md is missing")
        return

    paths = claimed_paths(ledger.read_text(encoding="utf-8"))
    missing = [path for path in paths if not (repo_root / path).exists()]
    result.note(f"ledger audit: {len(paths)} literal creation claim(s) checked")
    if missing:
        for path in missing:
            result.fail(f"ledger audit: MISSING claimed path: {path}")


def check_clean_tree(repo_root: Path, result: CheckResult) -> None:
    code, output, error = run_git(repo_root, "status", "--porcelain")
    if code != 0:
        detail = error or output or "not a git work tree"
        result.fail(f"working tree: unable to inspect ({detail})")
        return
    if output:
        result.fail("working tree: DIRTY")
        for line in output.splitlines():
            result.fail(f"working tree: {line}")
    else:
        result.note("working tree: clean")


def branch_and_head(repo_root: Path, result: CheckResult) -> tuple[str | None, str | None]:
    branch_code, branch, branch_error = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    head_code, head, head_error = run_git(repo_root, "rev-parse", "HEAD")
    if branch_code != 0 or not branch or branch == "HEAD":
        result.fail(f"receipt: cannot determine a branch ({branch_error or branch or 'detached HEAD'})")
        return None, None
    if head_code != 0 or not head:
        result.fail(f"receipt: cannot determine local HEAD ({head_error or head or 'unknown'})")
        return None, None
    result.note(f"receipt: branch {branch}")
    result.note(f"receipt: local HEAD {head}")
    return branch, head


def check_remote(repo_root: Path, branch: str | None, head: str | None, result: CheckResult) -> None:
    if not branch or not head:
        return
    ref = f"refs/heads/{branch}"
    code, output, error = run_git(repo_root, "ls-remote", "origin", ref)
    if code != 0:
        result.fail(f"remote: cannot read origin {ref} ({error or output or 'git ls-remote failed'})")
        return
    fields = output.split()
    remote_head = fields[0] if fields else ""
    if not remote_head:
        result.fail(f"remote: {ref} does not exist on origin")
        return
    result.note(f"receipt: remote {ref} {remote_head}")
    if remote_head != head:
        result.fail(f"remote: HEAD mismatch (local {head}, origin {remote_head})")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="repository root to inspect (default: current directory)")
    parser.add_argument("--audit-ledger", action="store_true", help="check literal ledger creation claims")
    parser.add_argument("--clean-tree", action="store_true", help="require git status --porcelain to be empty")
    parser.add_argument("--receipt", action="store_true", help="print an end-of-session persistence receipt")
    parser.add_argument("--verify-remote", action="store_true", help="require origin's current branch ref to equal HEAD")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(args.repo_root).expanduser().resolve()
    result = CheckResult()

    if not repo_root.is_dir():
        result.fail(f"repository root does not exist: {repo_root}")
    else:
        # A receipt is intentionally self-contained: it always records local cleanliness and ledger
        # continuity even if callers omit their individual flags.
        if args.audit_ledger or args.receipt:
            check_ledger(repo_root, result)
        if args.clean_tree or args.receipt:
            check_clean_tree(repo_root, result)
        if args.receipt or args.verify_remote:
            branch, head = branch_and_head(repo_root, result)
            if args.verify_remote:
                check_remote(repo_root, branch, head, result)

    for note in result.notes:
        print(note)
    for failure in result.failures:
        print(failure, file=sys.stderr)
    print(f"persistence-check: {'OK' if result.ok else 'FAIL'}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
