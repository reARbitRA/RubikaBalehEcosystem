"""
tests/test_forge_integrity.py

Meta-tests: the repository must keep obeying its own methodology. These run under both
`pytest` and stdlib `unittest` (see quality/TEST-STRATEGY.md §3) so `make test` stays green
with zero installs.

These are *not* a substitute for spec-level tests. Once a spec exists, its ACs get their own
`test_ac_<n>_<slug>` tests; forge-lint (rule F9) fails the build if they do not exist.
"""

import os
import re
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

import forge_lint  # noqa: E402

TASKS_DIR = os.path.join(REPO_ROOT, "tasks")
TRACE_PATH = os.path.join(REPO_ROOT, ".forge", "TRACE.md")
AGENTS_PATH = os.path.join(REPO_ROOT, "AGENTS.md")
STATE_PATH = os.path.join(REPO_ROOT, ".forge", "STATE.md")
LEDGER_PATH = os.path.join(REPO_ROOT, ".forge", "LEDGER.md")
TEMPLATES_DIR = os.path.join(REPO_ROOT, ".forge", "templates")


def _read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


class ForgeGateTests(unittest.TestCase):
    """The gate itself must pass on a clean checkout."""

    def test_forge_lint_passes_on_clean_repo(self):
        self.assertEqual(
            0, forge_lint.main(["--repo-root", REPO_ROOT]),
            "forge-lint reported violations — run `make forge-lint` and read the F-rule ids",
        )

    def test_secret_scan_finds_nothing(self):
        self.assertEqual(
            0, forge_lint.main(["--repo-root", REPO_ROOT, "--secrets-only"]),
            "secret material detected — see quality/SECURITY-BASELINE.md §1",
        )

    def test_expected_directory_tree_exists(self):
        missing = [d for d in forge_lint.EXPECTED_DIRS
                   if not os.path.isdir(os.path.join(REPO_ROOT, d))]
        self.assertEqual([], missing, "missing directories — see `make bootstrap`")


class ConstitutionTests(unittest.TestCase):
    """AGENTS.md must actually be an entry point."""

    def test_agents_md_declares_bootstrap_rules_and_handoff(self):
        text = _read(AGENTS_PATH)
        for needle in ("## 1. Bootstrap sequence", "## 2. Non-negotiable rules",
                       "## 4. Handoff", "make bootstrap && make test"):
            self.assertIn(needle, text, f"AGENTS.md is missing {needle!r}")

    def test_templates_exist_and_contain_placeholders(self):
        expected = ["spec.md", "plan.md", "task.md", "adr.md", "brainstorm.md",
                    "knowledge.md", "state.md", "ledger.md"]
        for name in expected:
            path = os.path.join(TEMPLATES_DIR, name)
            self.assertTrue(os.path.isfile(path), f"missing template {name}")
            self.assertIn("<", _read(path), f"template {name} has no placeholders")


class MemoryTests(unittest.TestCase):
    """STATE and LEDGER must keep their shape, or the next session is blind."""

    def test_state_names_baseline_and_next_steps(self):
        text = _read(STATE_PATH)
        self.assertIn("## Green baseline", text)
        self.assertIn("## Next up", text)
        self.assertIn("## Blocked", text)

    def test_ledger_has_at_least_one_entry(self):
        self.assertRegex(_read(LEDGER_PATH), re.compile(r"^## \d{4}-\d{2}-\d{2}T", re.M))

    def test_ledger_entries_carry_verification(self):
        entries = re.findall(r"^\*\*Verification:\*\*(.*)$", _read(LEDGER_PATH), re.M)
        self.assertTrue(entries, "no ledger entry records a verification command")
        for entry in entries:
            self.assertIn("exit", entry.lower())


class TaskTests(unittest.TestCase):
    """Task cards must be well formed and traceable."""

    def _task_files(self):
        for folder in ("OPEN", "DOING", "REVIEW", "DONE"):
            directory = os.path.join(TASKS_DIR, folder)
            if not os.path.isdir(directory):
                continue
            for name in sorted(os.listdir(directory)):
                if name.endswith(".md"):
                    yield folder, os.path.join(directory, name)

    def test_task_cards_are_well_formed(self):
        found = 0
        for folder, path in self._task_files():
            found += 1
            fm, err = forge_lint.parse_frontmatter(_read(path))
            self.assertIsNone(err, f"{path}: {err}")
            self.assertTrue(str(fm["id"]).startswith("T-"), f"{path}: id must start with T-")
            self.assertIn(fm["status"], forge_lint.LIFECYCLES["task"], f"{path}: bad status")
            self.assertIn("plan", fm, f"{path}: missing plan")
            self.assertIn("size", fm, f"{path}: missing size")
            self.assertIn(fm["size"], {"XS", "S", "M", "L"}, f"{path}: bad size")
            if folder == "DONE":
                self.assertIn("## Verification", _read(path),
                              f"{path}: a DONE task must record its verification")
        self.assertGreater(found, 0, "no task cards found at all")

    def test_trace_rows_reference_existing_tasks(self):
        trace = _read(TRACE_PATH)
        referenced = set(re.findall(r"\bT-\d{3}\b", trace))
        self.assertTrue(referenced, "TRACE.md references no tasks")
        existing = {os.path.splitext(name)[0].split("-")[0] + "-" + name.split("-")[1]
                    for _, path in self._task_files()
                    for name in [os.path.basename(path)]}
        # compare on the T-### token only
        existing_ids = set()
        for _, path in self._task_files():
            fm, _ = forge_lint.parse_frontmatter(_read(path))
            if fm:
                existing_ids.add(str(fm["id"]).strip())
        for ref in referenced:
            self.assertIn(ref, existing_ids,
                          f"TRACE.md references {ref} but no task card defines it")


class LegacyMigrationTests(unittest.TestCase):
    """The migrated corpus must stay migrated and stay traceable."""

    def test_no_loose_markdown_at_repository_root(self):
        allowed = {"README.md", "AGENTS.md"}
        root_md = [n for n in os.listdir(REPO_ROOT)
                   if n.endswith(".md") and n not in allowed]
        self.assertEqual([], root_md,
                         "loose markdown at the root — move it into the taxonomy "
                         "(.forge/CONVENTIONS.md §1)")

    def test_every_migrated_document_records_provenance(self):
        for sub in ("brainstorm", "knowledge"):
            directory = os.path.join(REPO_ROOT, sub)
            for dirpath, dirnames, filenames in os.walk(directory):
                for name in filenames:
                    if name.endswith(".md"):
                        text = _read(os.path.join(dirpath, name))
                        self.assertIn("Provenance", text,
                                      f"{sub}/{name} has no Provenance section")


if __name__ == "__main__":
    unittest.main(verbosity=2)
