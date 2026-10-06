#!/usr/bin/env python3
"""
forge-lint — the CI gate for the SPEC-FORGE methodology.

Fails the build when:
  F1  a .md outside src/ lacks valid frontmatter (missing keys, bad semver, bad dates)
  F2  a document's status is not legal for its type (lifecycle violation)
  F3  a document's id prefix does not match its type
  F4  two documents share an id (ids are globally unique)
  F5  depends_on / implements / supersedes points at an id that does not exist
  F6  a file under src/ has no SPEC header and no TRACE.md row
  F7  a task in tasks/DOING/ was last updated more than N hours ago (default 48)
  F8  a change set touching src/ did not append to .forge/LEDGER.md
  F9  a spec at IMPLEMENTED/VERIFIED has an AC with no matching test_ac_<n> test
  S1  secret material (private keys, .env files, token shapes) is present

Usage:
  python3 tools/forge_lint.py                 # full gate
  python3 tools/forge_lint.py --base-ref origin/main
  python3 tools/forge_lint.py --secrets-only  # secret scan only (used by make secret-scan)
  python3 tools/forge_lint.py --max-doing-age-hours 24

Exit code 0 = clean, 1 = violations. Every violation names the file and the fix.
Stdlib only — no third-party imports, ever (quality/SECURITY-BASELINE.md §6).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------- #
# Methodology tables (kept in sync with .forge/CONVENTIONS.md §3 and §4)
# --------------------------------------------------------------------------- #

TYPE_PREFIX = {
    "forge": "FORGE",
    "vision": "VISION",
    "brainstorm": "BRAIN",
    "spec": "SPEC",
    "adr": "ADR",
    "plan": "PLAN",
    "task": "T",
    "knowledge": "KNOW",
    "quality": "QUAL",
    "ops": "OPS",
    "state": "STATE",
    "ledger": "LEDGER",
}

LIFECYCLES = {
    "forge": {"ACTIVE", "ARCHIVED"},
    "vision": {"ACTIVE", "SUPERSEDED", "ARCHIVED"},
    "brainstorm": {"SEED", "GROWING", "PROMOTED", "ABANDONED"},
    "spec": {"DRAFT", "REVIEW", "APPROVED", "IMPLEMENTING", "IMPLEMENTED", "VERIFIED", "DEPRECATED"},
    "adr": {"PROPOSED", "ACCEPTED", "SUPERSEDED"},
    "plan": {"DRAFT", "ACTIVE", "COMPLETE", "ARCHIVED"},
    "task": {"OPEN", "DOING", "REVIEW", "DONE", "BLOCKED"},
    "knowledge": {"DRAFT", "CURRENT", "SUPERSEDED", "ARCHIVED"},
    "quality": {"DRAFT", "ACTIVE", "SUPERSEDED"},
    "ops": {"DRAFT", "ACTIVE", "SUPERSEDED"},
    "state": {"ACTIVE"},
    "ledger": {"ACTIVE"},
}

REQUIRED_KEYS = [
    "id", "title", "type", "status", "version", "owner",
    "created", "updated", "supersedes", "depends_on", "implements", "traces_to",
    "tags", "confidence",
]

# Documents deliberately exempt from the frontmatter rule (documented in CONVENTIONS.md §2):
#   README.md                        — the human-facing front door, conventionally un-frontmattered
#   .github/PULL_REQUEST_TEMPLATE.md  — GitHub requires this exact shape for the PR body
#   .forge/templates/**              — blank templates are incomplete by definition
EXEMPT_FROM_FRONTMATTER = (
    os.path.join("README.md"),
    os.path.join(".github", "PULL_REQUEST_TEMPLATE.md"),
    os.path.join(".forge", "templates"),
)

EXPECTED_DIRS = [
    ".forge", ".forge/templates", ".github", ".github/workflows",
    "vision", "brainstorm", "specs", "decisions", "plans",
    "tasks", "tasks/OPEN", "tasks/DOING", "tasks/REVIEW", "tasks/DONE",
    "knowledge", "knowledge/snippets", "knowledge/examples", "knowledge/apis",
    "knowledge/research", "quality", "ops", "src", "tests", "tools",
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".arena"}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
AC_RE = re.compile(r"\bAC-(\d+)\b")
SPEC_HEADER_RE = re.compile(r"SPEC-\d+")
LEDGER_ENTRY_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}T", re.MULTILINE)

SECRET_PATTERNS = [
    ("S1a", "private key block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("S1b", "AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("S1c", "GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{16,}\b")),
    ("S1d", "Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("S1e", "Google API key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
]

SECRET_FILE_NAMES = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519", "credentials"}
SECRET_FILE_SUFFIXES = (".pem", ".key", ".p12", ".pfx")


# --------------------------------------------------------------------------- #
# Minimal YAML-subset frontmatter parser (flat key: value, inline lists)
# --------------------------------------------------------------------------- #

def parse_frontmatter(text: str):
    """Return (dict, error). Only the flat subset used by this repo is supported."""
    if not text.startswith("---"):
        return None, "file does not start with a '---' frontmatter fence"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "frontmatter is not closed by a '---' fence"
    block = text[3:end].strip("\n")
    data: dict = {}
    for lineno, raw in enumerate(block.splitlines(), start=1):
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            return None, f"frontmatter line {lineno} is not 'key: value': {line!r}"
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            items = [v.strip().strip("'\"") for v in inner.split(",")] if inner else []
            data[key] = [v for v in items if v]
        else:
            data[key] = value.strip("'\"")
    return data, None


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def iter_markdown(repo_root: str):
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def rel(repo_root: str, path: str) -> str:
    return os.path.relpath(path, repo_root).replace(os.sep, "/")


def is_exempt(relpath: str) -> bool:
    for exempt in EXEMPT_FROM_FRONTMATTER:
        if relpath == exempt or relpath.startswith(exempt.rstrip("/") + "/"):
            return True
    return False


# --------------------------------------------------------------------------- #
# Individual rules
# --------------------------------------------------------------------------- #

def check_documents(repo_root: str, docs: list, errors: list, warnings: list) -> dict:
    """Rules F1–F5, F9. Returns {id: (relpath, frontmatter)}."""
    registry: dict = {}

    for path in docs:
        r = rel(repo_root, path)
        if is_exempt(r):
            continue
        text = read_text(path)
        fm, err = parse_frontmatter(text)
        if err:
            errors.append(f"F1 {r}: {err}. Fix: add the universal frontmatter block "
                          f"(.forge/CONVENTIONS.md §2).")
            continue

        missing = [k for k in REQUIRED_KEYS if k not in fm]
        if missing:
            errors.append(f"F1 {r}: missing frontmatter keys {missing}. "
                          f"Fix: add them (.forge/templates/*).")
            continue

        doc_id = str(fm["id"]).strip()
        dtype = str(fm["type"]).strip()

        # F3 — prefix must encode the type
        expected_prefix = TYPE_PREFIX.get(dtype)
        if expected_prefix is None:
            errors.append(f"F2 {r}: unknown type {dtype!r}. Legal types: {sorted(TYPE_PREFIX)}.")
            continue
        if not doc_id.startswith(expected_prefix + "-"):
            errors.append(f"F3 {r}: id {doc_id!r} does not start with the prefix "
                          f"{expected_prefix + '-'} required for type {dtype!r} "
                          f"(.forge/CONVENTIONS.md §3).")

        # F2 — lifecycle
        if str(fm["status"]).strip() not in LIFECYCLES[dtype]:
            errors.append(f"F2 {r}: status {fm['status']!r} is not legal for type {dtype!r}. "
                          f"Legal: {sorted(LIFECYCLES[dtype])}.")

        # F1 — semver + dates + enums
        if not SEMVER_RE.match(str(fm["version"]).strip()):
            errors.append(f"F1 {r}: version {fm['version']!r} is not semver (x.y.z).")
        for key in ("created", "updated"):
            if not DATE_RE.match(str(fm[key]).strip()):
                errors.append(f"F1 {r}: {key} {fm[key]!r} is not an ISO date (YYYY-MM-DD).")
        if str(fm["owner"]).strip() not in {"human", "agent", "pair"}:
            errors.append(f"F1 {r}: owner {fm['owner']!r} must be human|agent|pair.")
        if str(fm["confidence"]).strip() not in {"low", "medium", "high"}:
            errors.append(f"F1 {r}: confidence {fm['confidence']!r} must be low|medium|high.")

        # F4 — globally unique ids
        if doc_id in registry:
            errors.append(f"F4 {r}: id {doc_id!r} is already used by {registry[doc_id][0]}. "
                          f"Fix: ids are globally unique (.forge/CONVENTIONS.md §3).")
        else:
            registry[doc_id] = (r, fm)

        # F9 — AC coverage for implemented specs
        if dtype == "spec" and str(fm["status"]).strip() in {"IMPLEMENTED", "VERIFIED"}:
            acs = sorted({int(n) for n in AC_RE.findall(text)})
            if acs:
                test_blob = ""
                tests_dir = os.path.join(repo_root, "tests")
                if os.path.isdir(tests_dir):
                    for dirpath, dirnames, filenames in os.walk(tests_dir):
                        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                        for name in filenames:
                            if name.endswith(".py"):
                                test_blob += read_text(os.path.join(dirpath, name))
                for n in acs:
                    if not re.search(rf"test_ac_{n}(?:_|\b)", test_blob):
                        errors.append(f"F9 {r}: AC-{n} has no matching test. "
                                      f"Fix: add test_ac_{n}_<slug> in tests/ "
                                      f"(quality/TEST-STRATEGY.md §2).")

    # F5 — referential integrity (depends_on / implements / supersedes)
    for doc_id, (r, fm) in registry.items():
        for key in ("depends_on", "implements", "supersedes"):
            for ref in fm.get(key, []) or []:
                ref = str(ref).strip()
                if ref and ref not in registry:
                    errors.append(f"F5 {r}: {key} references unknown id {ref!r}. "
                                  f"Fix: create that document or drop the reference.")

    return registry


def check_src_traceability(repo_root: str, errors: list) -> int:
    """Rule F6 — every file under src/ traces to a spec."""
    src_dir = os.path.join(repo_root, "src")
    if not os.path.isdir(src_dir):
        return 0
    trace_text = ""
    trace_path = os.path.join(repo_root, ".forge", "TRACE.md")
    if os.path.isfile(trace_path):
        trace_text = read_text(trace_path)

    checked = 0
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name == ".gitkeep":
                continue
            path = os.path.join(dirpath, name)
            r = rel(repo_root, path)
            checked += 1
            head = "\n".join(read_text(path).splitlines()[:20])
            if SPEC_HEADER_RE.search(head):
                continue
            if r in trace_text or name in trace_text:
                warnings.append(f"F6 {r}: no SPEC header, but found in .forge/TRACE.md. "
                                f"Preferred fix: add a '/* SPEC-### */' header comment.")
                continue
            errors.append(f"F6 {r}: file under src/ has no '# SPEC-###' header and no row in "
                          f".forge/TRACE.md. Fix: add the header, or add a trace row "
                          f"(.forge/CONVENTIONS.md §6).")
    return checked


def check_stale_doing(repo_root: str, errors: list, max_age_hours: int) -> int:
    """Rule F7 — no zombie DOING tasks."""
    doing_dir = os.path.join(repo_root, "tasks", "DOING")
    if not os.path.isdir(doing_dir):
        return 0
    now = datetime.now()
    checked = 0
    for name in sorted(os.listdir(doing_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(doing_dir, name)
        fm, err = parse_frontmatter(read_text(path))
        if err or not fm:
            errors.append(f"F7 {name}: unreadable frontmatter ({err}).")
            continue
        checked += 1
        updated = str(fm.get("updated", "")).strip()
        try:
            when = datetime.strptime(updated, "%Y-%m-%d")
        except ValueError:
            errors.append(f"F7 {name}: updated={updated!r} is not an ISO date.")
            continue
        age = now - when
        if age > timedelta(hours=max_age_hours):
            errors.append(f"F7 {name}: task has been DOING for {age.days}d "
                          f"(> {max_age_hours}h). Fix: finish it, or write 'BLOCKED: <question>' "
                          f"and move it to tasks/REVIEW/ (ops/RUNBOOK.md RB-6).")
    return checked


def check_ledger_for_src_changes(repo_root: str, base_ref: str | None, errors: list) -> None:
    """Rule F8 — a change set touching src/ must append to the ledger."""
    if not base_ref:
        return
    try:
        out = subprocess.run(
            ["git", "-C", repo_root, "diff", "--name-only", f"{base_ref}...HEAD"],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        warnings_append("F8 skipped: git unavailable.")
        return
    if out.returncode != 0:
        warnings_append(f"F8 skipped: could not diff against {base_ref} ({out.stderr.strip()}).")
        return
    changed = [line.strip() for line in out.stdout.splitlines() if line.strip()]
    touches_src = any(c == "src" or c.startswith("src/") for c in changed)
    if not touches_src:
        return
    if not any(c == ".forge/LEDGER.md" for c in changed):
        errors.append(f"F8: this change set touches src/ but does not append to .forge/LEDGER.md. "
                      f"Fix: add a handoff entry (.forge/templates/ledger.md).")


_WARNINGS_BUFFER: list = []


def warnings_append(message: str) -> None:
    _WARNINGS_BUFFER.append(message)


# --------------------------------------------------------------------------- #
# Secret scan
# --------------------------------------------------------------------------- #

def scan_secrets(repo_root: str, errors: list) -> int:
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = os.path.join(dirpath, name)
            r = rel(repo_root, path)

            if name in SECRET_FILE_NAMES and name != ".env.example":
                errors.append(f"S1 {r}: file named {name!r} must never be committed "
                              f"(quality/SECURITY-BASELINE.md §1).")
                continue
            if name.endswith(SECRET_FILE_SUFFIXES):
                errors.append(f"S1 {r}: key/certificate file {name!r} must never be committed.")
                continue

            if name.endswith((".md", ".py", ".txt", ".yml", ".yaml", ".json", ".js", ".html",
                              ".css", ".sh", ".cfg", ".toml", ".ini", ".example")):
                scanned += 1
                text = read_text(path)
                for code, label, pattern in SECRET_PATTERNS:
                    if pattern.search(text):
                        errors.append(f"{code} {r}: possible {label}. Fix: remove it, rotate the "
                                      f"credential, then purge history (ops/RUNBOOK.md RB-4).")
    return scanned


# --------------------------------------------------------------------------- #
# Structure
# --------------------------------------------------------------------------- #

def check_tree(repo_root: str, errors: list) -> None:
    for d in EXPECTED_DIRS:
        if not os.path.isdir(os.path.join(repo_root, d)):
            errors.append(f"T1 missing directory: {d}/. Fix: mkdir -p {d} && touch {d}/.gitkeep")


def check_templates(repo_root: str, errors: list) -> None:
    tdir = os.path.join(repo_root, ".forge", "templates")
    expected = ["spec.md", "plan.md", "task.md", "adr.md", "brainstorm.md",
                "knowledge.md", "state.md", "ledger.md"]
    for name in expected:
        path = os.path.join(tdir, name)
        if not os.path.isfile(path):
            errors.append(f"T2 missing template: .forge/templates/{name}")
        elif "<" not in read_text(path):
            errors.append(f"T2 .forge/templates/{name} has no <placeholder> markers — it is not a "
                          f"usable template.")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="SPEC-FORGE methodology gate.")
    parser.add_argument("--base-ref", default=os.environ.get("FORGE_BASE_REF"),
                        help="git ref to diff against for rule F8 (e.g. origin/main)")
    parser.add_argument("--max-doing-age-hours", type=int, default=48)
    parser.add_argument("--secrets-only", action="store_true",
                        help="run only the secret scan (used by 'make secret-scan')")
    parser.add_argument("--repo-root", default=REPO_ROOT)
    args = parser.parse_args(argv)

    repo_root = os.path.abspath(args.repo_root)
    errors: list = []
    warnings: list = []

    scanned_files = scan_secrets(repo_root, errors)
    if args.secrets_only:
        for w in _WARNINGS_BUFFER:
            warnings.append(w)
        _report("secret-scan", errors, warnings, extra=f"{scanned_files} text files scanned")
        return 1 if errors else 0

    check_tree(repo_root, errors)
    check_templates(repo_root, errors)

    docs = sorted(iter_markdown(repo_root))
    registry = check_documents(repo_root, docs, errors, warnings)
    src_files = check_src_traceability(repo_root, errors)
    doing = check_stale_doing(repo_root, errors, args.max_doing_age_hours)
    check_ledger_for_src_changes(repo_root, args.base_ref, errors)

    for w in _WARNINGS_BUFFER:
        warnings.append(w)

    extra = (f"{len(registry)} documents checked · {src_files} files under src/ · "
             f"{doing} DOING tasks · {scanned_files} text files scanned")
    _report("forge-lint", errors, warnings, extra=extra)
    return 1 if errors else 0


def _report(name: str, errors: list, warnings: list, extra: str = "") -> int:
    print(f"{name}: {extra}" if extra else f"{name}:")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if errors:
        print(f"{name}: FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
    else:
        print(f"{name}: OK — 0 errors, {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
