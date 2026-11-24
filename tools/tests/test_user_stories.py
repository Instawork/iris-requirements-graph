"""docs/user-stories.md covers every MVP screen, and every requirement it cites is one."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from irisgraph import REPO_ROOT, REQUIREMENT_ID_IN_TEXT, load_graph  # noqa: E402

STORIES = REPO_ROOT / "docs" / "user-stories.md"
COVERS = re.compile(r"^\*Covers: (.+)\*$", re.MULTILINE)


class UserStoriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = load_graph(REPO_ROOT)
        cls.cited = {
            requirement_id
            for line in COVERS.findall(STORIES.read_text(encoding="utf-8"))
            for requirement_id in REQUIREMENT_ID_IN_TEXT.findall(line)
        }
        cls.mvp_screens = {
            doc["requirement_id"]
            for doc in cls.graph.requirements.values()
            if doc["requirement_phase"] == "MVP" and doc["requirement_target_layer"] == "user-interface"
        }

    def test_every_mvp_screen_is_covered_by_a_story(self):
        self.assertEqual(sorted(self.mvp_screens - self.cited), [])

    def test_every_cited_requirement_is_an_mvp_screen(self):
        self.assertEqual(sorted(self.cited - self.mvp_screens), [])


if __name__ == "__main__":
    unittest.main()
