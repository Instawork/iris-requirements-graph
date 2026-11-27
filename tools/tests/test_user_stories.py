"""docs/user-stories.md cites only MVP requirements, cites every MVP screen, and reaches every MVP requirement."""

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
        cls.mvp = {
            doc["requirement_id"]: doc
            for doc in cls.graph.requirements.values()
            if doc["requirement_phase"] == "MVP"
        }

    def test_every_cited_requirement_is_mvp(self):
        self.assertEqual(sorted(self.cited - set(self.mvp)), [])

    def test_every_mvp_screen_is_cited_by_a_story(self):
        screens = {
            requirement_id
            for requirement_id, doc in self.mvp.items()
            if doc["requirement_target_layer"] == "user-interface"
        }
        self.assertEqual(sorted(screens - self.cited), [])

    def test_every_mvp_requirement_is_cited_or_needed_by_a_cited_one(self):
        reached: set[str] = set()
        pending = list(self.cited)
        while pending:
            requirement_id = pending.pop()
            if requirement_id in reached or requirement_id not in self.mvp:
                continue
            reached.add(requirement_id)
            pending.extend(
                edge["requirement_id"]
                for edge in self.mvp[requirement_id].get("edges") or []
                if edge.get("edge_type") == "DEPENDS_ON"
            )
        self.assertEqual(sorted(set(self.mvp) - reached), [])


if __name__ == "__main__":
    unittest.main()
