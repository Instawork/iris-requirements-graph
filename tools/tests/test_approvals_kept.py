"""check_approvals_kept keeps approvals across edits only when a reviewer records the edit."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

from check_approvals_kept import approval_problems  # noqa: E402
from irisgraph import REPO_ROOT  # noqa: E402

GIT = ["git", "-c", "user.email=t@example.com", "-c", "user.name=t"]


class ApprovalsKeptTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="iris-approvals-"))
        shutil.copytree(REPO_ROOT / "graph", self.dir / "graph")
        self.path = sorted((self.dir / "graph" / "requirements").glob("**/*.req.yaml"))[0]
        self.reviewer = yaml.safe_load((self.dir / "graph" / "reviewers.yaml").read_text())["reviewers"][0]["reviewer_id"]
        self.edit(lambda d: d.update(requirement_review={"status": "approved", "by": self.reviewer, "at": "2026-11-01", "notes": None}))
        self.git("init", "-q", "-b", "main")
        self.commit("base")
        self.git("checkout", "-q", "-b", "change")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def git(self, *args):
        subprocess.run([*GIT, *args], cwd=self.dir, check=True, capture_output=True)

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message, "--allow-empty")

    def edit(self, change):
        doc = yaml.safe_load(self.path.read_text())
        change(doc)
        self.path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

    def problems(self):
        self.commit("change")
        return approval_problems(self.dir, "main", "HEAD")

    def test_untouched_approval_passes(self):
        self.assertEqual(self.problems(), [])

    def test_downgrade_fails(self):
        self.edit(lambda d: d["requirement_review"].update(status="draft"))
        self.assertTrue(any("now 'draft'" in p for p in self.problems()))

    def test_removed_requirement_fails(self):
        self.path.unlink()
        self.assertTrue(any("gone" in p for p in self.problems()))

    def test_edit_without_new_review_fails(self):
        self.edit(lambda d: d.update(requirement_title="A changed title"))
        self.assertTrue(any("at is unchanged" in p for p in self.problems()))

    def test_edit_with_new_review_passes(self):
        self.edit(lambda d: (d.update(requirement_title="A changed title"), d["requirement_review"].update(at="2026-11-02")))
        self.assertEqual(self.problems(), [])

    def test_delivery_change_needs_no_review(self):
        self.edit(lambda d: d["requirement_delivery"].update(status="in_progress"))
        self.assertEqual(self.problems(), [])


if __name__ == "__main__":
    unittest.main()
