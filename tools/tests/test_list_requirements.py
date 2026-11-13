"""list_requirements reports how far each open blocking decision reaches."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

from irisgraph import REPO_ROOT, load_graph  # noqa: E402
from list_requirements import blocking_lines, blocking_reach  # noqa: E402


class BlockingReachTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="iris-blocking-"))
        shutil.copytree(REPO_ROOT / "graph", self.dir / "graph")
        shutil.copytree(REPO_ROOT / "data-model", self.dir / "data-model")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def set_decision(self, decision_id, **values):
        path = self.dir / "graph" / "decisions.yaml"
        doc = yaml.safe_load(path.read_text())
        for decision in doc["decisions"]:
            if decision["decision_id"] == decision_id:
                decision.update(values)
        path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

    def test_reach_is_every_requirement_that_cites_it_or_depends_on_one_that_does(self):
        graph = load_graph(self.dir)
        cited_by = next(
            rid
            for rid in sorted(graph.requirements)
            if graph.dependents(rid) and graph.requirements[rid].get("requirement_decisions")
        )
        decision_id = graph.requirements[cited_by]["requirement_decisions"][0]
        self.set_decision(decision_id, blocking=True, status="open")
        graph = load_graph(self.dir)
        stopped = blocking_reach(graph)[decision_id]
        self.assertIn(cited_by, stopped)
        for dependent in graph.dependents(cited_by):
            self.assertIn(dependent, stopped)
        for rid in stopped:
            cites = any(
                decision_id in (graph.requirements[r].get("requirement_decisions") or [])
                for r in {rid} | graph.dependency_closure(rid)
            )
            self.assertTrue(cites, rid)
        self.assertTrue(any(line.startswith(f"{decision_id} is open and blocking") for line in blocking_lines(graph)))

    def test_an_answered_or_non_blocking_decision_is_not_listed(self):
        graph = load_graph(self.dir)
        for decision_id in list(blocking_reach(graph)):
            self.set_decision(decision_id, blocking=False)
        self.assertEqual(blocking_reach(load_graph(self.dir)), {})


if __name__ == "__main__":
    unittest.main()
