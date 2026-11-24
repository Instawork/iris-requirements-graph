"""The user stories hold every MVP screen once, with all its rules, and every link lands on an anchor."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

from build_user_stories import PERSONA_FILES, render  # noqa: E402
from irisgraph import REPO_ROOT, load_graph  # noqa: E402

ANCHOR = re.compile(r'<a id="([^"]+)"></a>')
LINK = re.compile(r"\]\(([^)#\s]*)#([^)\s]+)\)")


class UserStoriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = load_graph(REPO_ROOT)
        cls.files = render(cls.graph)
        cls.anchors = {name: set(ANCHOR.findall(text)) for name, text in cls.files.items()}

    def mvp(self, layer: str) -> list[dict]:
        return [
            doc
            for doc in self.graph.requirements.values()
            if doc["requirement_phase"] == "MVP" and doc["requirement_target_layer"] == layer
        ]

    def test_every_mvp_screen_is_one_story_in_one_persona_file(self):
        persona_names = [name for name, *_ in PERSONA_FILES]
        for doc in self.mvp("user-interface"):
            anchor = doc["requirement_id"].lower()
            holders = [name for name in persona_names if anchor in self.anchors[name]]
            self.assertEqual(len(holders), 1, f"{doc['requirement_id']} is in {holders}")

    def test_each_story_lists_every_rule_of_its_requirement(self):
        for doc in self.mvp("user-interface"):
            anchor = doc["requirement_id"].lower()
            name = next(name for name, *_ in PERSONA_FILES if anchor in self.anchors[name])
            section = self.files[name].split(f'<a id="{anchor}"></a>', 1)[1].split('<a id="', 1)[0]
            for rule in doc["requirement_rules"]:
                self.assertIn(f"- **{rule['rule_id']}.** ", section, f"{doc['requirement_id']}.{rule['rule_id']}")

    def test_later_phase_requirements_are_left_out(self):
        later = {doc["requirement_id"].lower() for doc in self.graph.requirements.values() if doc["requirement_phase"] != "MVP"}
        for name, anchors in self.anchors.items():
            self.assertFalse(anchors & later, f"{name} holds {sorted(anchors & later)}")

    def test_every_link_lands_on_an_anchor(self):
        checked = 0
        for name, text in self.files.items():
            for target_file, target_anchor in LINK.findall(text):
                if target_file.startswith("http"):
                    continue
                target = target_file or name
                checked += 1
                self.assertIn(target_anchor, self.anchors.get(target, set()), f"{name} links to {target}#{target_anchor}")
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()
