"""The validator passes on the real graph and catches each kind of break.

Each mutation test copies the graph to a temporary directory, breaks one thing, and expects
the named check to report it.
"""

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

from irisgraph import REPO_ROOT, load_graph  # noqa: E402
from validate import CHECKS, run  # noqa: E402


class GraphCopy:
    def __init__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="iris-graph-"))
        shutil.copytree(REPO_ROOT / "graph", self.dir / "graph")
        shutil.copytree(REPO_ROOT / "data-model", self.dir / "data-model")
        self.graph = load_graph(self.dir)

    def close(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def requirement_path(self, requirement_id: str) -> Path:
        return self.graph.paths[requirement_id]

    def edit_requirement(self, requirement_id: str, change):
        path = self.requirement_path(requirement_id)
        doc = yaml.safe_load(path.read_text())
        change(doc)
        path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

    def edit_yaml(self, relative: str, change):
        path = self.dir / relative
        doc = yaml.safe_load(path.read_text())
        change(doc)
        path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

    def problems(self, check_name: str):
        return run(load_graph(self.dir), checks=[check_name])[check_name][1]


def pick(graph, *, layer=None, phase=None, with_edges=False, with_writes=False):
    for requirement_id in sorted(graph.requirements):
        doc = graph.requirements[requirement_id]
        if layer and doc.get("requirement_target_layer") != layer:
            continue
        if phase and doc.get("requirement_phase") != phase:
            continue
        if with_edges and not graph.depends_on(requirement_id):
            continue
        if with_writes and not (doc.get("data_model") or {}).get("writes"):
            continue
        return requirement_id
    raise AssertionError("no requirement matches")


class RealGraphTests(unittest.TestCase):
    def test_every_check_passes(self):
        results = run(load_graph(REPO_ROOT))
        failing = {name: problems[:5] for name, (_, problems) in results.items() if problems}
        self.assertEqual(failing, {})

    def test_every_check_is_exercised_by_a_mutation(self):
        exercised = {name[len("test_"):].split("__")[0] for name in dir(MutationTests) if name.startswith("test_")}
        missing = sorted(set(CHECKS) - exercised - {"files_parse"})
        self.assertEqual(missing, [])


class MutationTests(unittest.TestCase):
    def setUp(self):
        self.copy = GraphCopy()
        self.g = self.copy.graph

    def tearDown(self):
        self.copy.close()

    def assertCaught(self, check_name: str, needle: str = ""):
        problems = self.copy.problems(check_name)
        self.assertTrue(any(needle in message for _, message in problems), f"{check_name} missed it: {problems[:5]}")

    def test_requirement_keys(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d.update(migration_entities=["Shift"]))
        self.assertCaught("requirement_keys", "unknown key")

    def test_requirement_placement(self):
        rid = pick(self.g, layer="product")
        self.copy.edit_requirement(rid, lambda d: d.update(requirement_target_layer="platform"))
        self.assertCaught("requirement_placement", "layer")

    def test_actors(self):
        rid = pick(self.g, layer="product", phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d.update(requirement_actors=[]))
        self.assertCaught("actors", "at least one actor")

    def test_rules_present(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d.update(requirement_rules=[]))
        self.assertCaught("rules_present", "at least one rule")

    def test_retired_ids(self):
        retired = next(iter(self.g.retired))
        rid = pick(self.g)
        source = self.copy.requirement_path(rid)
        target = source.with_name(f"{retired}.req.yaml")
        doc = yaml.safe_load(source.read_text())
        doc["requirement_id"] = retired
        target.write_text(yaml.safe_dump(doc, sort_keys=False))
        self.assertCaught("retired_ids", "still exists")

    def test_citations_valid(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_sources=["SHEET ZZ-99"]))
        self.assertCaught("citations_valid", "unknown sheet feature")

    def test_citations_valid__bare_feedback(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_sources=["FEEDBACK"]))
        self.assertCaught("citations_valid", "FEEDBACK")

    def test_every_rule_grounded(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_sources=[], rule_decisions=[]))
        self.assertCaught("every_rule_grounded", "cites no source")

    def test_decisions_well_formed(self):
        self.copy.edit_yaml("graph/decisions.yaml", lambda d: d["decisions"][0].update(assumption=None))
        self.assertCaught("decisions_well_formed", "assumption")

    def test_decisions_well_formed__answer_from(self):
        self.copy.edit_yaml("graph/decisions.yaml", lambda d: d["decisions"][0].pop("answer_from"))
        self.assertCaught("decisions_well_formed", "answer_from")

    def test_decisions_well_formed__two_questions(self):
        self.copy.edit_yaml("graph/decisions.yaml", lambda d: d["decisions"][0].update(question="Which day? Which zone?"))
        self.assertCaught("decisions_well_formed", "one question")

    def test_decisions_well_formed__long_assumption(self):
        self.copy.edit_yaml("graph/decisions.yaml", lambda d: d["decisions"][0].update(assumption="word " * 51))
        self.assertCaught("decisions_well_formed", "at most 50 words")

    def test_registers_well_formed(self):
        self.copy.edit_yaml("graph/conflicts.yaml", lambda d: d["conflicts"][0].update(keep=""))
        self.assertCaught("registers_well_formed", "needs keep")

    def test_ids_in_text_exist(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_statement="It calls REQ-NOPE-0001 first."))
        self.assertCaught("ids_in_text_exist", "REQ-NOPE-0001")

    def test_upper_case_names_exist(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_statement="It sends MADE_UP_EVENT to the Agency."))
        self.assertCaught("upper_case_names_exist", "MADE_UP_EVENT")

    def test_features_traced(self):
        feature_id = next(f for f in self.g.features if self.g.feature_phase(f) == "MVP")

        def drop(doc_id):
            self.copy.edit_requirement(doc_id, lambda d: d.update(requirement_features=[f for f in d["requirement_features"] if f != feature_id]))

        for rid, doc in self.g.requirements.items():
            if feature_id in (doc.get("requirement_features") or []):
                drop(rid)
        self.assertCaught("features_traced", feature_id)

    def test_edges_resolve(self):
        rid = pick(self.g)
        self.copy.edit_requirement(rid, lambda d: d["edges"].append({"edge_type": "DEPENDS_ON", "requirement_id": "REQ-NOPE-0001"}))
        self.assertCaught("edges_resolve", "unknown")

    def test_edges_point_down__layer(self):
        platform = pick(self.g, layer="platform", phase="MVP")
        product = pick(self.g, layer="product", phase="MVP")
        self.copy.edit_requirement(platform, lambda d: d["edges"].append({"edge_type": "DEPENDS_ON", "requirement_id": product}))
        self.assertCaught("edges_point_down", "depends up")

    def test_edges_point_down__phase(self):
        mvp = pick(self.g, layer="product", phase="MVP")
        later = pick(self.g, layer="product", phase="P3")
        self.copy.edit_requirement(mvp, lambda d: d["edges"].append({"edge_type": "DEPENDS_ON", "requirement_id": later}))
        self.assertCaught("edges_point_down", "P3")

    def test_edges_acyclic(self):
        rid = pick(self.g, with_edges=True)
        target = self.g.depends_on(rid)[0]
        self.copy.edit_requirement(target, lambda d: d["edges"].append({"edge_type": "DEPENDS_ON", "requirement_id": rid}))
        self.assertCaught("edges_acyclic", "cycle")

    def test_starting_flow_closed(self):
        flagged = [r for r, d in self.g.requirements.items() if d.get("requirement_starting_flow") and self.g.depends_on(r)]
        target = self.g.depends_on(flagged[0])[0]
        self.copy.edit_requirement(target, lambda d: d.update(requirement_starting_flow=False))
        self.assertCaught("starting_flow_closed", "not")

    def test_starting_flow_closed__unknown_seed(self):
        self.copy.edit_yaml("graph/starting-flow.yaml", lambda d: d["seeds"].append("REQ-NOPE-0001"))
        self.assertCaught("starting_flow_closed", "REQ-NOPE-0001")

    def test_starting_flow_names_in_flow(self):
        screen, outside = next(
            (screen, r)
            for screen in sorted(self.g.starting_flow())
            if self.g.requirements[screen]["requirement_target_layer"] == "user-interface"
            for r, d in sorted(self.g.requirements.items())
            if d["requirement_phase"] == "MVP" and not d["requirement_starting_flow"] and screen in self.g.dependency_closure(r)
        )
        self.copy.edit_requirement(screen, lambda d: d["requirement_rules"][0].update(rule_statement=f"Saving opens {outside}."))
        self.assertCaught("starting_flow_names_in_flow", outside)

    def test_named_requirements_connected(self):
        rid = pick(self.g, layer="platform", phase="MVP")
        other = next(
            r
            for r in sorted(self.g.requirements)
            if r != rid and r not in self.g.dependency_closure(rid) and rid not in self.g.dependency_closure(r)
        )
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_statement=f"{other} does the rest."))
        self.assertCaught("named_requirements_connected", other)

    def test_graph_citations_have_decisions(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_sources=["GRAPH a guess"], rule_decisions=[]))
        self.assertCaught("graph_citations_have_decisions", "cites GRAPH")

    def test_rule_decisions_listed(self):
        rid = next(r for r, d in sorted(self.g.requirements.items()) if any(rule.get("rule_decisions") for rule in d["requirement_rules"]))
        self.copy.edit_requirement(rid, lambda d: d.update(requirement_decisions=[]))
        self.assertCaught("rule_decisions_listed", "does not list")

    def test_removed_ids_retired(self):
        rid = pick(self.g, phase="P3")
        git = ["git", "-c", "user.email=t@example.com", "-c", "user.name=t"]
        subprocess.run([*git, "init", "-q"], cwd=self.copy.dir, check=True)
        subprocess.run([*git, "add", "-A"], cwd=self.copy.dir, check=True)
        subprocess.run([*git, "commit", "-qm", "base"], cwd=self.copy.dir, check=True)
        self.copy.requirement_path(rid).unlink()
        self.assertCaught("removed_ids_retired", rid)

    def test_data_model_schema(self):
        def broken(doc):
            doc["entities"][0]["fields"][0]["or a stray phrase"] = None

        self.copy.edit_yaml("data-model/org.yaml", broken)
        self.assertCaught("data_model_schema", "unknown key")

    def test_data_model_refs(self):
        self.copy.edit_yaml("data-model/audit.yaml", lambda d: d["entities"][0]["fields"].append({"name": "shift_id", "type": "ref:Shift"}))
        self.assertCaught("data_model_refs", "pointing up")

    def test_data_model_naming__ref_without_id(self):
        self.copy.edit_yaml("data-model/audit.yaml", lambda d: d["entities"][0]["fields"].append({"name": "approver", "type": "ref:User"}))
        self.assertCaught("data_model_naming", "ends in _id")

    def test_data_model_naming__bool_prefix(self):
        self.copy.edit_yaml("data-model/audit.yaml", lambda d: d["entities"][0]["fields"].append({"name": "active", "type": "bool"}))
        self.assertCaught("data_model_naming", "starts with is_")

    def test_data_model_naming__list_of_refs(self):
        self.copy.edit_yaml("data-model/audit.yaml", lambda d: d["entities"][0]["fields"].append({"name": "user_ids", "type": "list:ref:User"}))
        self.assertCaught("data_model_naming", "join entity")

    def test_data_model_naming__record_id_without_type(self):
        self.copy.edit_yaml("data-model/audit.yaml", lambda d: d["entities"][0]["fields"].append({"name": "target_id", "type": "int"}))
        self.assertCaught("data_model_naming", "target_type")

    def test_data_model_naming__reserved_word(self):
        self.copy.edit_yaml("data-model/audit.yaml", lambda d: d["entities"][0]["fields"].append({"name": "values", "type": "json"}))
        self.assertCaught("data_model_naming", "reserved word")

    def test_enums_used(self):
        self.copy.edit_yaml("data-model/org.yaml", lambda d: d["enums"].append({"enum": "Unused", "values": [{"value": "A", "meaning": "A."}]}))
        self.assertCaught("enums_used", "Unused")

    def test_status_transitions(self):
        def broken(doc):
            for enum in doc["enums"]:
                if enum.get("transitions"):
                    enum["values"].append({"value": "LIMBO", "meaning": "Never reached."})
                    return

        self.copy.edit_yaml("data-model/ordering.yaml", broken)
        self.assertCaught("status_transitions", "LIMBO")

    def test_requirement_data_model(self):
        rid = pick(self.g, layer="product", phase="MVP", with_writes=True)
        own = self.g.requirements[rid]["requirement_target_module"]
        foreign = next(name for name, e in self.g.entities.items() if e["module"] != own and e["phase"] == "MVP")
        self.copy.edit_requirement(rid, lambda d: d["data_model"]["writes"].append(f"{foreign}.*"))
        self.assertCaught("requirement_data_model", "belongs to")

    def test_cross_module_reads(self):
        rid = pick(self.g, layer="platform", phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["data_model"].update(status="covered", reads=(d["data_model"].get("reads") or []) + ["AccessLink.*"], detail=None))
        writers = {r for r, d in self.g.requirements.items() if any(str(x).startswith("AccessLink.") for x in (d.get("data_model") or {}).get("writes") or [])}
        if rid in writers or writers & self.g.dependency_closure(rid) or self.g.entities["AccessLink"]["module"] == self.g.requirements[rid]["requirement_target_module"]:
            self.skipTest("picked requirement already reaches the writer")
        self.assertCaught("cross_module_reads", "AccessLink")

    def test_entities_written(self):
        def strip(doc):
            doc["data_model"]["writes"] = [w for w in doc["data_model"].get("writes") or [] if not str(w).startswith("AuditEvent.")]

        for rid, doc in self.g.requirements.items():
            if any(str(w).startswith("AuditEvent.") for w in (doc.get("data_model") or {}).get("writes") or []):
                self.copy.edit_requirement(rid, strip)
        self.assertCaught("entities_written", "AuditEvent")

    def test_settings_catalog(self):
        self.copy.edit_yaml("graph/catalogs/settings.yaml", lambda d: d["settings"][0].update(default="fifteen"))
        self.assertCaught("settings_catalog", "default")

    def test_notifications_catalog(self):
        self.copy.edit_yaml("graph/catalogs/notifications.yaml", lambda d: d["notifications"][0].update(channels=["PIGEON"]))
        self.assertCaught("notifications_catalog", "PIGEON")

    def test_notifications_catalog__subject(self):
        self.copy.edit_yaml("graph/catalogs/notifications.yaml", lambda d: d["notifications"][0].update(subject="Booking"))
        self.assertCaught("notifications_catalog", "must be an entity")

    def test_notifications_catalog__no_subject(self):
        self.copy.edit_yaml("graph/catalogs/notifications.yaml", lambda d: d["notifications"][0].pop("subject"))
        self.assertCaught("notifications_catalog", "must be an entity")

    def test_upload_types_catalog(self):
        self.copy.edit_yaml("graph/catalogs/upload-types.yaml", lambda d: d["upload_types"][0]["columns"][0].update(maps_to="RateLine.nope"))
        self.assertCaught("upload_types_catalog", "nope")

    def test_upload_types_catalog__kind(self):
        self.copy.edit_yaml("graph/catalogs/upload-types.yaml", lambda d: d["upload_types"][0]["columns"][0].update(kind="number"))
        self.assertCaught("upload_types_catalog", "kind must be one of")

    def test_upload_types_catalog__kind_of_field(self):
        def broken(doc):
            for upload_type in doc["upload_types"]:
                for column in upload_type["columns"]:
                    if column["kind"] == "money":
                        column["kind"] = "text"
                        return

        self.copy.edit_yaml("graph/catalogs/upload-types.yaml", broken)
        self.assertCaught("upload_types_catalog", "kind must be money")

    def test_upload_types_catalog__identified_by(self):
        self.copy.edit_yaml("graph/catalogs/upload-types.yaml", lambda d: d["upload_types"][0].update(identified_by=[["no_such_column"]]))
        self.assertCaught("upload_types_catalog", "no_such_column")

    def test_saved_by_in_owner_closure(self):
        def broken(doc):
            for upload_type in doc["upload_types"]:
                owner = upload_type["owner"]
                outside = next(r for r in sorted(self.g.requirements) if r != owner and r not in self.g.dependency_closure(owner))
                for column in upload_type["columns"]:
                    if column.get("saved_by"):
                        column["saved_by"] = outside
                        return outside
            raise AssertionError("no column has saved_by")

        self.copy.edit_yaml("graph/catalogs/upload-types.yaml", broken)
        self.assertCaught("saved_by_in_owner_closure", "is not a requirement that owner")

    def test_review_state(self):
        rid = pick(self.g, phase="MVP", with_edges=True)
        self.copy.edit_requirement(rid, lambda d: d.update(requirement_review={"status": "approved", "by": "pdongritot", "at": "2026-11-13", "notes": None}))
        self.assertCaught("review_state", "depends on")

    def test_delivery_state(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d.update(requirement_delivery={"status": "delivered", "pull_requests": []}))
        self.assertCaught("delivery_state", "delivered")

    def test_text_shape(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_statement="First sentence here. Second sentence here."))
        self.assertCaught("text_shape", "one sentence")

    def test_glossary(self):
        rid = pick(self.g, phase="MVP")
        self.copy.edit_requirement(rid, lambda d: d["requirement_rules"][0].update(rule_statement="The Supplier is told at once."))
        self.assertCaught("glossary", "Supplier")

    def test_no_duplicates(self):
        first = pick(self.g, phase="MVP")
        second = next(r for r in sorted(self.g.requirements) if r != first and self.g.requirements[r].get("requirement_rules"))
        text = self.g.requirements[first]["requirement_rules"][0]["rule_statement"]
        self.copy.edit_requirement(second, lambda d: d["requirement_rules"][0].update(rule_statement=text))
        self.assertCaught("no_duplicates", "word for word")


if __name__ == "__main__":
    unittest.main()
