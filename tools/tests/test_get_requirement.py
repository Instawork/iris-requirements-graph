"""The bundle carries the catalog entries a requirement owns or names, and no others."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

from get_requirement import requirement_bundle  # noqa: E402
from irisgraph import REPO_ROOT, REQUIREMENT_ID_IN_TEXT, load_graph  # noqa: E402


class BundleCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = load_graph(REPO_ROOT)

    def uses(self, requirement_id: str, catalog: str) -> set[str]:
        return set(requirement_bundle(self.graph, requirement_id)["uses"].get(catalog, {}))

    def text(self, requirement_id: str) -> str:
        doc = self.graph.requirements[requirement_id]
        parts = [doc["requirement_statement"], str(doc["data_model"].get("detail") or "")]
        parts += [rule["rule_statement"] for rule in doc["requirement_rules"]]
        return " ".join(parts)

    def test_a_requirement_id_does_not_name_an_upload_type(self):
        checked = 0
        for requirement_id in self.graph.requirements:
            text = self.text(requirement_id)
            if "graph/catalogs/upload-types.yaml" in text:
                continue
            bare = REQUIREMENT_ID_IN_TEXT.sub(" ", text)
            for key in self.uses(requirement_id, "upload_types"):
                checked += 1
                self.assertIn(key, bare, f"{requirement_id} prints {key}, which only a requirement id names")
        self.assertGreater(checked, 0)

    def test_a_module_that_owns_a_catalog_enum_does_not_get_the_whole_catalog(self):
        self.assertEqual(self.uses("REQ-INTAKE-0005", "upload_types"), set())
        self.assertEqual(self.uses("REQ-ORG-0001", "settings"), set())

    def test_a_requirement_that_names_the_catalog_file_gets_the_whole_catalog(self):
        self.assertEqual(self.uses("REQ-INTAKE-0001", "upload_types"), set(self.graph.upload_types))
        self.assertEqual(self.uses("REQ-ORG-0006", "settings"), set(self.graph.settings))
        self.assertEqual(self.uses("REQ-MESSAGING-0001", "notifications"), set(self.graph.notifications))

    def test_owned_entries_are_printed_under_owns_only(self):
        for key, item in self.graph.upload_types.items():
            bundle = requirement_bundle(self.graph, item["owner"])
            self.assertIn(key, bundle["owns"]["upload_types"])
            self.assertNotIn(key, bundle["uses"].get("upload_types", {}))


if __name__ == "__main__":
    unittest.main()
