"""Regression tests for the session-persistence receipt tool (T-007)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "persistence_check.py"


class PersistenceCheckTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> None:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args], text=True, capture_output=True, check=False
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"git {' '.join(args)} failed:\n{completed.stdout}\n{completed.stderr}",
        )

    def make_repo(self, root: Path, claimed_path: str = "knowledge/claimed.md") -> None:
        self.git(root, "init", "-q")
        self.git(root, "config", "user.name", "persistence-check-test")
        self.git(root, "config", "user.email", "persistence-check-test@example.invalid")
        (root / ".forge").mkdir()
        target = root / claimed_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("present\n", encoding="utf-8")
        (root / ".forge" / "LEDGER.md").write_text(
            "# LEDGER\n\n## session\n\n**Did:** Created `" + claimed_path + "`.\n",
            encoding="utf-8",
        )
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "test fixture")

    def run_checker(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--repo-root", str(repo), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_audit_and_clean_tree_accept_existing_ledger_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory) / "repo"
            repo.mkdir()
            self.make_repo(repo)

            completed = self.run_checker(repo, "--audit-ledger", "--clean-tree")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("ledger audit: 1 literal creation claim(s) checked", completed.stdout)
            self.assertIn("working tree: clean", completed.stdout)
            self.assertTrue(completed.stdout.rstrip().endswith("persistence-check: OK"))

    def test_audit_reports_missing_ledger_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory) / "repo"
            repo.mkdir()
            self.make_repo(repo)
            (repo / "knowledge" / "claimed.md").unlink()
            self.git(repo, "add", "-u")
            self.git(repo, "commit", "-qm", "remove claimed artifact")

            completed = self.run_checker(repo, "--audit-ledger", "--clean-tree")

            self.assertEqual(completed.returncode, 1)
            self.assertIn("MISSING claimed path: knowledge/claimed.md", completed.stderr)
            self.assertTrue(completed.stdout.rstrip().endswith("persistence-check: FAIL"))

    def test_receipt_verifies_current_branch_on_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            remote = root / "origin.git"
            repo = root / "repo"
            repo.mkdir()
            self.make_repo(repo)
            subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
            self.git(repo, "remote", "add", "origin", str(remote))
            branch = subprocess.run(
                ["git", "-C", str(repo), "branch", "--show-current"],
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            self.git(repo, "push", "-q", "-u", "origin", f"HEAD:refs/heads/{branch}")

            completed = self.run_checker(repo, "--receipt", "--verify-remote")

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn(f"receipt: branch {branch}", completed.stdout)
            self.assertIn(f"receipt: remote refs/heads/{branch}", completed.stdout)
            self.assertTrue(completed.stdout.rstrip().endswith("persistence-check: OK"))


if __name__ == "__main__":
    unittest.main()
