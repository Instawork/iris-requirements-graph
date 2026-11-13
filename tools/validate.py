#!/usr/bin/env python3
"""Validate the Iris requirements graph.

Every check returns a list of (where, message) problems. The graph is valid when every check
returns none. CI runs all suites; run one with --suite or one check with --check.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import (  # noqa: E402
    IMPLICIT_FIELDS,
    LAYER_ORDER,
    PHASES,
    REPO_ROOT,
    REQUIREMENT_ID,
    REQUIREMENT_ID_IN_TEXT,
    ROLES,
    Graph,
    load_graph,
    parse_type,
    type_targets,
)

TITLE_MAX = 80
STATEMENT_MAX_SENTENCES = 3
SENTENCE_MAX_WORDS = 30
RULE_MAX_WORDS = 35
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
UPPER_TOKEN = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
DECISION_ID = re.compile(r"^D-\d+$")
DECISION_IN_TEXT = re.compile(r"\bD-\d+\b")
CONFLICT_IN_TEXT = re.compile(r"\bC-\d+\b")
INPUT_IN_TEXT = re.compile(r"\bI-\d+\b")
FEATURE_ID = re.compile(r"^[A-Z]+-\d+$")
CAPABILITY_ID = re.compile(r"^\d+\.\d+$")
SHEET_TABS = {"Decisions & Inputs", "Core Capabilities", "Summary", "Read Me", "Feature Detail"}
DETAIL_REQUIRED = {"SHEET", "PRD", "DEMO", "GRAPH", "SESSIONS", "FEEDBACK", "FAQ"}

REQUIREMENT_KEYS = {
    "requirement_id": str,
    "requirement_target_layer": str,
    "requirement_target_module": str,
    "requirement_phase": str,
    "requirement_title": str,
    "requirement_statement": str,
    "requirement_actors": list,
    "requirement_rules": list,
    "requirement_sources": list,
    "requirement_decisions": list,
    "requirement_features": list,
    "edges": list,
    "data_model": dict,
    "requirement_starting_flow": bool,
    "requirement_review": dict,
    "requirement_delivery": dict,
}
RULE_KEYS = {"rule_id", "rule_statement", "rule_sources", "rule_decisions"}
DATA_MODEL_KEYS = {"status", "reads", "writes", "detail"}
REVIEW_KEYS = {"status", "by", "at", "notes"}
DELIVERY_KEYS = {"status", "pull_requests"}
REVIEW_STATUSES = {"draft", "approved", "placeholder", "changes_requested"}
DELIVERY_STATUSES = {"not_started", "in_progress", "delivered"}
DECISION_KEYS = {"decision_id", "origin", "question", "status", "assumption", "blocking", "answer", "sources", "applies_to", "answer_from"}
ANSWER_FROM = {"COMPASS_OPERATIONS", "COMPASS_HR_LEGAL_PAYROLL", "COMPASS_FINANCE", "INSTAWORK_PRODUCT", "INSTAWORK_ENGINEERING"}
ENUM_KEYS = {"enum", "values", "transitions", "catalog", "phase", "description"}
ENTITY_KEYS = {"entity", "phase", "description", "fields", "unique", "constraints"}
FIELD_KEYS = {"name", "type", "nullable", "note"}
SETTING_KEYS = {"key", "type", "default", "scope", "meaning", "owner", "sources", "decisions"}
NOTIFICATION_KEYS = {"type", "trigger", "recipients", "channels", "owner", "sources", "decisions"}
UPLOAD_KEYS = {"type", "phase", "meaning", "uploaders", "owner", "sources", "decisions", "columns", "identified_by"}
COLUMN_KEYS = {"column", "kind", "required", "maps_to", "lookup", "note", "saved_by"}
COLUMN_KINDS = {"text", "date", "time", "money", "int", "yes_no"}
KIND_OF_FIELD_TYPE = {"bool": "yes_no", "money": "money", "int": "int", "date": "date"}
TERM_KEYS = {"term", "definition", "avoid", "source_words", "sources", "decisions"}

CHECKS: dict[str, tuple[str, callable]] = {}


def check(suite: str):
    def register(function):
        CHECKS[function.__name__] = (suite, function)
        return function

    return register


def where(graph: Graph, requirement_id: str) -> str:
    path = graph.paths.get(requirement_id)
    return str(path.relative_to(graph.root)) if path else str(requirement_id)


def phase_index(phase) -> int:
    return PHASES.index(phase) if phase in PHASES else -1


def requirement_text(doc: dict) -> list[tuple[str, str]]:
    texts = [("title", doc.get("requirement_title") or ""), ("statement", doc.get("requirement_statement") or "")]
    for rule in doc.get("requirement_rules") or []:
        if isinstance(rule, dict):
            texts.append((rule.get("rule_id") or "rule", rule.get("rule_statement") or ""))
    return texts


def all_requirement_decisions(doc: dict) -> set[str]:
    decisions = set(doc.get("requirement_decisions") or [])
    for rule in doc.get("requirement_rules") or []:
        if isinstance(rule, dict):
            decisions.update(rule.get("rule_decisions") or [])
    return decisions


def all_requirement_sources(doc: dict) -> list[str]:
    sources = list(doc.get("requirement_sources") or [])
    for rule in doc.get("requirement_rules") or []:
        if isinstance(rule, dict):
            sources.extend(rule.get("rule_sources") or [])
    return sources


def citation_problem(graph: Graph, citation) -> str | None:
    if not isinstance(citation, str) or not citation.strip():
        return "citation must be text"
    key, _, detail = citation.strip().partition(" ")
    detail = detail.strip()
    if key != "GRAPH" and key not in graph.sources:
        return f"citation {citation!r} starts with unknown source key {key!r}"
    if key in DETAIL_REQUIRED and not detail:
        return f"citation {citation!r} needs a detail after {key}, such as a feature id or section"
    if key == "SHEET" and detail:
        if FEATURE_ID.match(detail) and detail not in graph.features:
            return f"citation {citation!r} names an unknown sheet feature"
        if CAPABILITY_ID.match(detail) and detail not in graph.capabilities:
            return f"citation {citation!r} names an unknown sheet capability"
        if not FEATURE_ID.match(detail) and not CAPABILITY_ID.match(detail) and detail not in SHEET_TABS:
            return f"citation {citation!r} must name a feature id, a capability id, or a tab: {sorted(SHEET_TABS)}"
    return None


def sentences(text: str) -> list[str]:
    return [part for part in SENTENCE_SPLIT.split(" ".join(text.split())) if part]


def field_ref(graph: Graph, ref: str):
    """Resolve 'Entity.field' or 'Entity.*'. Returns (entity, field) or a problem string."""
    if not isinstance(ref, str) or "." not in ref:
        return f"{ref!r} must look like Entity.field or Entity.*"
    entity_name, _, field_name = ref.partition(".")
    entity = graph.entities.get(entity_name)
    if entity is None:
        return f"{ref!r} names unknown entity {entity_name}"
    if field_name != "*" and field_name not in entity["field_map"] and field_name not in IMPLICIT_FIELDS:
        return f"{ref!r} names unknown field {field_name} on {entity_name}"
    return (entity_name, field_name)


def entity_refs(graph: Graph, doc: dict, key: str) -> list[tuple[str, str]]:
    result = []
    for ref in (doc.get("data_model") or {}).get(key) or []:
        resolved = field_ref(graph, ref)
        if isinstance(resolved, tuple):
            result.append(resolved)
    return result


def writers_of(graph: Graph) -> dict[str, set[str]]:
    writers: dict[str, set[str]] = defaultdict(set)
    for requirement_id, doc in graph.requirements.items():
        for entity_name, _ in entity_refs(graph, doc, "writes"):
            writers[entity_name].add(requirement_id)
    return writers


def writes_field(graph: Graph, requirement_id: str, entity_name: str, field_name: str) -> bool:
    doc = graph.requirements.get(requirement_id) or {}
    return any(
        entity == entity_name and field in ("*", field_name)
        for entity, field in entity_refs(graph, doc, "writes")
    )


# ---------------------------------------------------------------- structure


@check("structure")
def files_parse(graph: Graph):
    return list(graph.load_errors)


@check("structure")
def requirement_keys(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        for key in doc:
            if key not in REQUIREMENT_KEYS:
                problems.append((here, f"unknown key {key!r}"))
        for key, kind in REQUIREMENT_KEYS.items():
            if key not in doc:
                problems.append((here, f"missing key {key!r}"))
            elif not isinstance(doc[key], kind):
                problems.append((here, f"{key} must be a {kind.__name__}"))
        for index, rule in enumerate(doc.get("requirement_rules") or []):
            if not isinstance(rule, dict):
                problems.append((here, f"rule {index + 1} must be a mapping"))
                continue
            for key in rule:
                if key not in RULE_KEYS:
                    problems.append((here, f"rule {rule.get('rule_id')} has unknown key {key!r}"))
            for key in RULE_KEYS:
                if key not in rule:
                    problems.append((here, f"rule {rule.get('rule_id')} is missing {key!r}"))
        for name, allowed in (
            ("data_model", DATA_MODEL_KEYS),
            ("requirement_review", REVIEW_KEYS),
            ("requirement_delivery", DELIVERY_KEYS),
        ):
            block = doc.get(name)
            if isinstance(block, dict):
                for key in block:
                    if key not in allowed:
                        problems.append((here, f"{name} has unknown key {key!r}"))
        for edge in doc.get("edges") or []:
            if not isinstance(edge, dict) or set(edge) != {"edge_type", "requirement_id"}:
                problems.append((here, f"edge {edge!r} must have exactly edge_type and requirement_id"))
            elif edge.get("edge_type") != "DEPENDS_ON":
                problems.append((here, f"edge_type {edge.get('edge_type')!r} is not DEPENDS_ON"))
    return problems


@check("structure")
def requirement_placement(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        match = REQUIREMENT_ID.match(str(requirement_id))
        if not match:
            problems.append((here, f"requirement_id {requirement_id!r} must look like REQ-MODULE-0001"))
            continue
        module_id = doc.get("requirement_target_module")
        if match.group(1) != module_id:
            problems.append((here, f"id module {match.group(1)} differs from requirement_target_module {module_id}"))
        module = graph.modules.get(module_id)
        if module is None:
            problems.append((here, f"unknown module {module_id}"))
            continue
        if doc.get("requirement_target_layer") != module["layer"]:
            problems.append((here, f"layer {doc.get('requirement_target_layer')} differs from module layer {module['layer']}"))
        expected = graph.root / "graph" / "requirements" / module["layer"] / module_id.lower() / f"{requirement_id}.req.yaml"
        if graph.paths[requirement_id] != expected:
            problems.append((here, f"file belongs at {expected.relative_to(graph.root)}"))
        if doc.get("requirement_phase") not in PHASES:
            problems.append((here, f"requirement_phase must be one of {PHASES}"))
    return problems


@check("structure")
def actors(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        listed = doc.get("requirement_actors") or []
        for actor in listed:
            if actor not in ROLES:
                problems.append((here, f"unknown actor {actor!r}; use one of {ROLES}"))
        if len(set(listed)) != len(listed):
            problems.append((here, "an actor is listed twice"))
        if doc.get("requirement_target_layer") in ("product", "user-interface") and not listed:
            problems.append((here, "product and user-interface requirements name at least one actor"))
    return problems


@check("structure")
def rules_present(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        rules = doc.get("requirement_rules") or []
        status = (doc.get("requirement_review") or {}).get("status")
        if not rules and not (status == "placeholder" and doc.get("requirement_phase") != "MVP"):
            problems.append((here, "needs at least one rule; only a P2 or P3 placeholder may have none"))
        ids = [rule.get("rule_id") for rule in rules if isinstance(rule, dict)]
        for rule_id in ids:
            if not re.match(r"^R\d+$", str(rule_id)):
                problems.append((here, f"rule_id {rule_id!r} must look like R1"))
        if len(set(ids)) != len(ids):
            problems.append((here, "rule ids repeat"))
    return problems


@check("structure")
def retired_ids(graph: Graph):
    problems = []
    for requirement_id, item in graph.retired.items():
        if requirement_id in graph.requirements:
            problems.append(("graph/retired.yaml", f"{requirement_id} is retired but still exists"))
        replaced_by = item.get("replaced_by")
        if replaced_by is not None and replaced_by not in graph.requirements:
            problems.append(("graph/retired.yaml", f"{requirement_id} is replaced by unknown {replaced_by}"))
        if not item.get("reason"):
            problems.append(("graph/retired.yaml", f"{requirement_id} needs a reason"))
    return problems


# ---------------------------------------------------------------- citations


@check("citations")
def citations_valid(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        for citation in all_requirement_sources(doc):
            problem = citation_problem(graph, citation)
            if problem:
                problems.append((here, problem))
        for decision_id in all_requirement_decisions(doc):
            if decision_id not in graph.decisions:
                problems.append((here, f"unknown decision {decision_id!r}"))
    return problems


@check("citations")
def every_rule_grounded(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        for rule in doc.get("requirement_rules") or []:
            if isinstance(rule, dict) and not (rule.get("rule_sources") or rule.get("rule_decisions")):
                problems.append((here, f"rule {rule.get('rule_id')} cites no source and no decision"))
        if not all_requirement_sources(doc) and not all_requirement_decisions(doc):
            problems.append((here, "cites no source and no decision"))
    return problems


@check("citations")
def graph_citations_have_decisions(graph: Graph):
    """A rule the graph supplies cites the decision that records the assumption."""
    problems = []
    for requirement_id, doc in graph.requirements.items():
        for rule in doc.get("requirement_rules") or []:
            if not isinstance(rule, dict):
                continue
            graph_cited = any(str(source).startswith("GRAPH") for source in rule.get("rule_sources") or [])
            if graph_cited and not rule.get("rule_decisions"):
                problems.append((where(graph, requirement_id), f"rule {rule.get('rule_id')} cites GRAPH but no decision"))
    return problems


@check("citations")
def rule_decisions_listed(graph: Graph):
    """requirement_decisions lists every decision a rule cites, so a reader of the header sees them all."""
    problems = []
    for requirement_id, doc in graph.requirements.items():
        listed = set(doc.get("requirement_decisions") or [])
        for rule in doc.get("requirement_rules") or []:
            if not isinstance(rule, dict):
                continue
            for decision_id in rule.get("rule_decisions") or []:
                if decision_id not in listed:
                    problems.append((where(graph, requirement_id), f"rule {rule.get('rule_id')} cites {decision_id}, which requirement_decisions does not list"))
    return problems


@check("citations")
def decisions_well_formed(graph: Graph):
    problems = []
    used = set()
    for doc in graph.requirements.values():
        used.update(all_requirement_decisions(doc))
    for catalog in (graph.settings, graph.notifications, graph.upload_types):
        for item in catalog.values():
            used.update(item.get("decisions") or [])
    for decision_id, decision in graph.decisions.items():
        here = f"graph/decisions.yaml {decision_id}"
        for key in decision:
            if key not in DECISION_KEYS:
                problems.append((here, f"unknown key {key!r}"))
        if not DECISION_ID.match(str(decision_id)):
            problems.append((here, "decision_id must look like D-1"))
        if decision.get("origin") not in ("sheet", "graph"):
            problems.append((here, "origin must be sheet or graph"))
        if not decision.get("question"):
            problems.append((here, "needs a question"))
        if not isinstance(decision.get("blocking"), bool):
            problems.append((here, "blocking must be true or false"))
        if decision.get("answer_from") not in ANSWER_FROM:
            problems.append((here, f"answer_from must be one of {', '.join(sorted(ANSWER_FROM))}"))
        if decision.get("status") == "open":
            if not decision.get("assumption"):
                problems.append((here, "an open decision needs the assumption the graph builds on"))
            if decision.get("answer"):
                problems.append((here, "an open decision has no answer yet"))
        elif decision.get("status") == "answered":
            if not decision.get("answer"):
                problems.append((here, "an answered decision needs its answer"))
        else:
            problems.append((here, "status must be open or answered"))
        if not decision.get("sources"):
            problems.append((here, "needs at least one source"))
        for citation in decision.get("sources") or []:
            problem = citation_problem(graph, citation)
            if problem:
                problems.append((here, problem))
        if decision_id not in used and not decision.get("applies_to"):
            problems.append((here, "no requirement or catalog entry cites it; cite it or set applies_to"))
    return problems


@check("citations")
def registers_well_formed(graph: Graph):
    problems = []
    for key, source in graph.sources.items():
        for needed in ("rank", "title", "url", "use"):
            if not source.get(needed):
                problems.append((f"graph/sources.yaml {key}", f"needs {needed}"))
    for conflict_id, conflict in graph.conflicts.items():
        for needed in ("topic", "keep", "drop"):
            if not conflict.get(needed):
                problems.append((f"graph/conflicts.yaml {conflict_id}", f"needs {needed}"))
        for decision_id in DECISION_IN_TEXT.findall(f"{conflict.get('keep')} {conflict.get('drop')}"):
            if decision_id not in graph.decisions:
                problems.append((f"graph/conflicts.yaml {conflict_id}", f"names unknown decision {decision_id}"))
    for input_id, item in graph.inputs.items():
        here = f"graph/inputs.yaml {input_id}"
        if item.get("origin") not in ("sheet", "graph"):
            problems.append((here, "origin must be sheet or graph"))
        if not item.get("ask"):
            problems.append((here, "needs an ask"))
        for citation in item.get("sources") or []:
            problem = citation_problem(graph, citation)
            if problem:
                problems.append((here, problem))
        for decision_id in item.get("decisions") or []:
            if decision_id not in graph.decisions:
                problems.append((here, f"unknown decision {decision_id}"))
    seen_terms = set()
    for term in graph.terms:
        here = f"graph/terms.yaml {term.get('term')}"
        for key in term:
            if key not in TERM_KEYS:
                problems.append((here, f"unknown key {key!r}"))
        if term.get("term") in seen_terms:
            problems.append((here, "term is defined twice"))
        seen_terms.add(term.get("term"))
        if not term.get("definition") or not term.get("sources"):
            problems.append((here, "needs a definition and sources"))
        for citation in term.get("sources") or []:
            problem = citation_problem(graph, citation)
            if problem:
                problems.append((here, problem))
    return problems


@check("citations")
def ids_in_text_exist(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        for label, text in requirement_text(doc):
            for found in REQUIREMENT_ID_IN_TEXT.findall(text):
                if found in graph.retired:
                    problems.append((here, f"{label} names retired {found}"))
                elif found not in graph.requirements:
                    problems.append((here, f"{label} names unknown {found}"))
            for found in DECISION_IN_TEXT.findall(text):
                if found not in graph.decisions:
                    problems.append((here, f"{label} names unknown decision {found}"))
            for found in CONFLICT_IN_TEXT.findall(text):
                if found not in graph.conflicts:
                    problems.append((here, f"{label} names unknown conflict {found}"))
            for found in INPUT_IN_TEXT.findall(text):
                if found not in graph.inputs:
                    problems.append((here, f"{label} names unknown input {found}"))
    return problems


@check("citations")
def upper_case_names_exist(graph: Graph):
    known = set(ROLES) | set(graph.settings) | set(graph.notifications) | set(graph.upload_types)
    for enum_name in graph.enums:
        known.update(graph.enum_values(enum_name))
    problems = []
    for requirement_id, doc in graph.requirements.items():
        for label, text in requirement_text(doc):
            for token in UPPER_TOKEN.findall(text):
                if token not in known:
                    problems.append((where(graph, requirement_id), f"{label} names {token}, which no enum or catalog defines"))
    return problems


# ---------------------------------------------------------------- scope


@check("scope")
def features_traced(graph: Graph):
    problems = []
    covered: dict[str, set[str]] = defaultdict(set)
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        for feature_id in doc.get("requirement_features") or []:
            if feature_id not in graph.features:
                problems.append((here, f"unknown feature {feature_id}"))
                continue
            feature_phase = graph.feature_phase(feature_id)
            covered[feature_id].add(doc.get("requirement_phase"))
            if phase_index(feature_phase) > phase_index(doc.get("requirement_phase")):
                problems.append((here, f"a {doc.get('requirement_phase')} requirement cites {feature_phase} feature {feature_id}"))
    for feature_id in graph.features:
        phase = graph.feature_phase(feature_id)
        if phase not in covered.get(feature_id, set()):
            problems.append(("graph/scope/features.yaml", f"{phase} feature {feature_id} has no {phase} requirement"))
    for capability_id, capability in graph.capabilities.items():
        if capability.get("phase") not in PHASES:
            problems.append(("graph/scope/capabilities.yaml", f"capability {capability_id} has phase {capability.get('phase')!r}"))
    for feature_id, feature in graph.features.items():
        if str(feature.get("capability_id")) not in graph.capabilities:
            problems.append(("graph/scope/features.yaml", f"{feature_id} names unknown capability {feature.get('capability_id')}"))
    return problems


# ---------------------------------------------------------------- edges


@check("edges")
def edges_resolve(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        targets = graph.depends_on(requirement_id)
        if len(set(targets)) != len(targets):
            problems.append((here, "an edge is listed twice"))
        for target in targets:
            if target == requirement_id:
                problems.append((here, "depends on itself"))
            elif target in graph.retired:
                problems.append((here, f"depends on retired {target}"))
            elif target not in graph.requirements:
                problems.append((here, f"depends on unknown {target}"))
    return problems


@check("edges")
def edges_point_down(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        source_layer = doc.get("requirement_target_layer")
        for target in graph.depends_on(requirement_id):
            target_doc = graph.requirements.get(target)
            if not target_doc or source_layer not in LAYER_ORDER:
                continue
            target_layer = target_doc.get("requirement_target_layer")
            if target_layer in LAYER_ORDER and LAYER_ORDER.index(target_layer) < LAYER_ORDER.index(source_layer):
                problems.append((here, f"{source_layer} depends up on {target_layer} {target}"))
            if phase_index(target_doc.get("requirement_phase")) > phase_index(doc.get("requirement_phase")):
                problems.append((here, f"a {doc.get('requirement_phase')} requirement depends on {target_doc.get('requirement_phase')} {target}"))
    return problems


@check("edges")
def edges_acyclic(graph: Graph):
    problems = []
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str):
        state[node] = 1
        stack.append(node)
        for target in graph.depends_on(node):
            if target not in graph.requirements:
                continue
            if state.get(target) == 1:
                cycle = stack[stack.index(target):] + [target]
                problems.append((where(graph, node), "dependency cycle: " + " -> ".join(cycle)))
            elif state.get(target) is None:
                visit(target)
        stack.pop()
        state[node] = 2

    for requirement_id in sorted(graph.requirements):
        if state.get(requirement_id) is None:
            visit(requirement_id)
    return problems


@check("edges")
def starting_flow_closed(graph: Graph):
    problems = []
    if not graph.starting_flow_seeds:
        problems.append(("graph/starting-flow.yaml", "lists no seeds"))
    for seed in graph.starting_flow_seeds:
        if seed not in graph.requirements:
            problems.append(("graph/starting-flow.yaml", f"seed {seed} is not a requirement"))
    flow = graph.starting_flow()
    for requirement_id, doc in graph.requirements.items():
        flagged = doc.get("requirement_starting_flow") is True
        if flagged != (requirement_id in flow):
            state = "is flagged but is not" if flagged else "is not flagged but is"
            problems.append((where(graph, requirement_id), f"{state} in the starting flow; run tools/set_starting_flow.py"))
        if requirement_id in flow and doc.get("requirement_phase") != "MVP":
            problems.append((where(graph, requirement_id), "only MVP requirements are in the starting flow"))
    return problems


@check("edges")
def starting_flow_names_in_flow(graph: Graph):
    """A starting-flow screen that names an MVP requirement needs it in the flow, or the slice dead-ends."""
    problems = []
    flow = graph.starting_flow()
    for requirement_id in sorted(flow):
        if graph.requirements[requirement_id].get("requirement_target_layer") != "user-interface":
            continue
        for rule in graph.requirements[requirement_id].get("requirement_rules") or []:
            if not isinstance(rule, dict):
                continue
            for named in sorted(set(REQUIREMENT_ID_IN_TEXT.findall(rule.get("rule_statement") or ""))):
                doc = graph.requirements.get(named)
                if doc and doc.get("requirement_phase") == "MVP" and named not in flow:
                    problems.append((where(graph, requirement_id), f"{rule.get('rule_id')} names {named}, which is not in the starting flow"))
    return problems


@check("edges")
def named_requirements_connected(graph: Graph):
    """A rule that names another requirement depends on it, directly or not, or is depended on by it."""
    problems = []
    closures = {rid: graph.dependency_closure(rid) for rid in graph.requirements}
    for requirement_id, doc in graph.requirements.items():
        for rule in doc.get("requirement_rules") or []:
            if not isinstance(rule, dict):
                continue
            for named in sorted(set(REQUIREMENT_ID_IN_TEXT.findall(rule.get("rule_statement") or ""))):
                if named == requirement_id or named not in graph.requirements:
                    continue
                if named not in closures[requirement_id] and requirement_id not in closures[named]:
                    problems.append((where(graph, requirement_id), f"{rule.get('rule_id')} names {named}, but neither depends on the other"))
    return problems


# ---------------------------------------------------------------- data model


@check("data-model")
def data_model_schema(graph: Graph):
    problems = []
    for path, doc in graph.data_model_files.items():
        module_id = doc.get("module")
        if module_id not in graph.modules:
            problems.append((path, f"unknown module {module_id}"))
        elif Path(path).stem != module_id.lower():
            problems.append((path, f"file for module {module_id} must be data-model/{module_id.lower()}.yaml"))
        for key in doc:
            if key not in ("module", "enums", "entities"):
                problems.append((path, f"unknown key {key!r}"))
    for name, enum in graph.enums.items():
        here = f"{enum['file']} enum {name}"
        for key in enum:
            if key not in ENUM_KEYS | {"module", "file"}:
                problems.append((here, f"unknown key {key!r}"))
        if enum.get("phase", "MVP") not in PHASES:
            problems.append((here, "phase must be MVP, P2, or P3"))
        values = enum.get("values") or []
        if not values:
            problems.append((here, "has no values"))
        names = [value.get("value") for value in values if isinstance(value, dict)]
        if len(set(names)) != len(names):
            problems.append((here, "a value repeats"))
        if not enum.get("catalog"):
            for value in values:
                if not isinstance(value, dict) or set(value) - {"value", "meaning", "phase"}:
                    problems.append((here, f"value {value!r} must have value and meaning"))
                elif not value.get("meaning"):
                    problems.append((here, f"value {value.get('value')} needs a meaning"))
    for name, entity in graph.entities.items():
        here = f"{entity['file']} entity {name}"
        for key in entity:
            if key not in ENTITY_KEYS | {"module", "file", "field_map"}:
                problems.append((here, f"unknown key {key!r}"))
        if entity.get("phase") not in PHASES:
            problems.append((here, "phase must be MVP, P2, or P3"))
        if not entity.get("description"):
            problems.append((here, "needs a description"))
        if not entity.get("fields"):
            problems.append((here, "has no fields"))
        for item in entity.get("fields") or []:
            if not isinstance(item, dict):
                problems.append((here, f"field {item!r} must be a mapping"))
                continue
            for key in item:
                if key not in FIELD_KEYS:
                    problems.append((here, f"field {item.get('name')} has unknown key {key!r}"))
            if item.get("name") in IMPLICIT_FIELDS:
                problems.append((here, f"field {item['name']} is implicit; do not list it"))
            if "nullable" in item and not isinstance(item["nullable"], bool):
                problems.append((here, f"field {item.get('name')} nullable must be true or false"))
            if parse_type(item.get("type")) is None:
                problems.append((here, f"field {item.get('name')} has unknown type {item.get('type')!r}"))
        for combo in entity.get("unique") or []:
            for field_name in combo or []:
                if field_name not in entity["field_map"] and field_name not in IMPLICIT_FIELDS:
                    problems.append((here, f"unique names unknown field {field_name}"))
    return problems


@check("data-model")
def data_model_refs(graph: Graph):
    problems = []
    for name, entity in graph.entities.items():
        here = f"{entity['file']} entity {name}"
        layer = graph.module_layer(entity["module"])
        for item in entity.get("fields") or []:
            if not isinstance(item, dict):
                continue
            for kind, target in type_targets(item.get("type")):
                if kind == "ref":
                    target_entity = graph.entities.get(target)
                    if target_entity is None:
                        problems.append((here, f"{item['name']} refers to unknown entity {target}"))
                        continue
                    target_layer = graph.module_layer(target_entity["module"])
                    target_phase = target_entity.get("phase")
                else:
                    target_enum = graph.enums.get(target)
                    if target_enum is None:
                        problems.append((here, f"{item['name']} uses unknown enum {target}"))
                        continue
                    target_layer = graph.module_layer(target_enum["module"])
                    target_phase = target_enum.get("phase", "MVP")
                if layer in LAYER_ORDER and target_layer in LAYER_ORDER and LAYER_ORDER.index(target_layer) < LAYER_ORDER.index(layer):
                    problems.append((here, f"{item['name']} is a {layer} field pointing up at {target_layer} {target}"))
                if phase_index(target_phase) > phase_index(entity.get("phase")):
                    problems.append((here, f"{item['name']} points at {target_phase} {target} from a {entity.get('phase')} entity"))
    return problems


@check("data-model")
def enums_used(graph: Graph):
    used = set()
    for entity in graph.entities.values():
        for item in entity.get("fields") or []:
            if isinstance(item, dict):
                used.update(target for kind, target in type_targets(item.get("type")) if kind == "enum")
    for setting in graph.settings.values():
        parsed = parse_type(setting.get("type"))
        if parsed and parsed[0] == "enum":
            used.add(parsed[1])
    return [(enum["file"], f"enum {name} is never used") for name, enum in graph.enums.items() if name not in used]


@check("data-model")
def status_transitions(graph: Graph):
    problems = []
    enum_fields: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for entity_name, entity in graph.entities.items():
        for item in entity.get("fields") or []:
            if isinstance(item, dict):
                for kind, target in type_targets(item.get("type")):
                    if kind == "enum":
                        enum_fields[target].append((entity_name, item["name"]))
                if item.get("name") == "status":
                    parsed = parse_type(item.get("type"))
                    if not parsed or parsed[0] != "enum":
                        problems.append((entity["file"], f"{entity_name}.status must be an enum"))
                    elif not graph.enums.get(parsed[1], {}).get("transitions"):
                        problems.append((entity["file"], f"{entity_name}.status uses {parsed[1]}, which lists no transitions"))
    for name, enum in graph.enums.items():
        transitions = enum.get("transitions")
        if not transitions:
            continue
        here = f"{enum['file']} enum {name}"
        values = set(graph.enum_values(name))
        reachable = set()
        edges = []
        for transition in transitions:
            if not isinstance(transition, dict) or set(transition) != {"from", "to", "requirement"}:
                problems.append((here, f"transition {transition!r} must have from, to, and requirement"))
                continue
            source, target, requirement_id = transition["from"], transition["to"], transition["requirement"]
            if source is not None and source not in values:
                problems.append((here, f"transition from unknown value {source}"))
            if target not in values:
                problems.append((here, f"transition to unknown value {target}"))
            if requirement_id not in graph.requirements:
                problems.append((here, f"transition {source} -> {target} names unknown {requirement_id}"))
            elif not any(writes_field(graph, requirement_id, entity_name, field_name) for entity_name, field_name in enum_fields[name]):
                fields = ", ".join(f"{e}.{f}" for e, f in enum_fields[name])
                problems.append((here, f"{requirement_id} makes {source} -> {target} but does not write {fields}"))
            if source is None:
                reachable.add(target)
            edges.append((source, target))
        changed = True
        while changed:
            changed = False
            for source, target in edges:
                if source in reachable and target not in reachable:
                    reachable.add(target)
                    changed = True
        for value in sorted(values - reachable):
            problems.append((here, f"value {value} can never be reached"))
    return problems


@check("data-model")
def requirement_data_model(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        block = doc.get("data_model") or {}
        status = block.get("status")
        reads = block.get("reads") or []
        writes = block.get("writes") or []
        layer = doc.get("requirement_target_layer")
        phase = doc.get("requirement_phase")
        for key in ("reads", "writes"):
            for ref in block.get(key) or []:
                resolved = field_ref(graph, ref)
                if isinstance(resolved, str):
                    problems.append((here, f"data_model.{key}: {resolved}"))
                    continue
                entity = graph.entities[resolved[0]]
                if phase_index(entity.get("phase")) > phase_index(phase):
                    problems.append((here, f"a {phase} requirement {key[:-1]}s {entity.get('phase')} entity {resolved[0]}"))
                if key == "writes" and entity["module"] != doc.get("requirement_target_module"):
                    problems.append((here, f"writes {resolved[0]}, which belongs to {entity['module']}; depend on the requirement that owns it"))
        if status == "covered":
            if not reads and not writes:
                problems.append((here, "data_model covered must list reads or writes"))
        elif status == "not_applicable":
            if reads or writes:
                problems.append((here, "data_model not_applicable lists no reads or writes"))
            if not block.get("detail"):
                problems.append((here, "data_model not_applicable needs a detail saying why"))
        elif status == "pending":
            blocking = [d for d in all_requirement_decisions(doc) if graph.decisions.get(d, {}).get("blocking")]
            if phase == "MVP" and not blocking:
                problems.append((here, "an MVP data_model may be pending only while a blocking decision is open"))
            if not block.get("detail"):
                problems.append((here, "data_model pending needs a detail saying what is missing"))
        else:
            problems.append((here, "data_model.status must be covered, not_applicable, or pending"))
        if layer == "user-interface" and writes:
            problems.append((here, "a user-interface requirement writes through product requirements, never directly"))
    return problems


@check("data-model")
def cross_module_reads(graph: Graph):
    problems = []
    writers = writers_of(graph)
    for requirement_id, doc in graph.requirements.items():
        module_id = doc.get("requirement_target_module")
        closure = graph.dependency_closure(requirement_id)
        for entity_name in sorted({entity for entity, _ in entity_refs(graph, doc, "reads")}):
            entity = graph.entities[entity_name]
            if entity["module"] == module_id:
                continue
            if not closure & writers.get(entity_name, set()):
                owners = ", ".join(sorted(writers.get(entity_name, set()))) or "no requirement"
                problems.append((where(graph, requirement_id), f"reads {entity_name} but depends on none of its writers ({owners})"))
    return problems


@check("data-model")
def entities_written(graph: Graph):
    problems = []
    writers = writers_of(graph)
    for name, entity in graph.entities.items():
        phases = {graph.requirements[r].get("requirement_phase") for r in writers.get(name, set())}
        if not any(phase_index(p) <= phase_index(entity.get("phase")) for p in phases):
            problems.append((entity["file"], f"{entity.get('phase')} entity {name} has no {entity.get('phase')} requirement that writes it"))
    return problems


# ---------------------------------------------------------------- catalogs


def _catalog_citations(graph: Graph, here: str, item: dict, problems: list):
    if not item.get("sources") and not item.get("decisions"):
        problems.append((here, "cites no source and no decision"))
    for citation in item.get("sources") or []:
        problem = citation_problem(graph, citation)
        if problem:
            problems.append((here, problem))
    for decision_id in item.get("decisions") or []:
        if decision_id not in graph.decisions:
            problems.append((here, f"unknown decision {decision_id}"))


def _owner(graph: Graph, here: str, item: dict, platform_requirement: str, token: str, problems: list):
    owner = item.get("owner")
    if owner not in graph.requirements:
        problems.append((here, f"owner {owner!r} is not a requirement"))
        return
    if owner != platform_requirement and platform_requirement not in graph.dependency_closure(owner):
        problems.append((here, f"owner {owner} must depend on {platform_requirement}"))
    texts = " ".join(text for _, text in requirement_text(graph.requirements[owner]))
    if token not in texts:
        problems.append((here, f"owner {owner} never names {token} in its rules"))


@check("catalogs")
def settings_catalog(graph: Graph):
    problems = []
    for key, item in graph.settings.items():
        here = f"graph/catalogs/settings.yaml {key}"
        for field_name in item:
            if field_name not in SETTING_KEYS:
                problems.append((here, f"unknown key {field_name!r}"))
        parsed = parse_type(item.get("type"))
        default = item.get("default")
        if parsed == ("scalar", "int"):
            if not isinstance(default, int) or isinstance(default, bool):
                problems.append((here, "default must be an int"))
        elif parsed == ("scalar", "bool"):
            if not isinstance(default, bool):
                problems.append((here, "default must be true or false"))
        elif parsed and parsed[0] == "enum":
            if default not in graph.enum_values(parsed[1]):
                problems.append((here, f"default {default!r} is not a {parsed[1]} value"))
        else:
            problems.append((here, f"type {item.get('type')!r} must be int, bool, or enum:Name"))
        if item.get("scope") not in ("any", "program"):
            problems.append((here, "scope must be any or program"))
        if not item.get("meaning"):
            problems.append((here, "needs a meaning"))
        _catalog_citations(graph, here, item, problems)
        _owner(graph, here, item, "REQ-ORG-0006", key, problems)
    return problems


@check("catalogs")
def notifications_catalog(graph: Graph):
    problems = []
    channels = set(graph.enum_values("NotificationChannel"))
    for key, item in graph.notifications.items():
        here = f"graph/catalogs/notifications.yaml {key}"
        for field_name in item:
            if field_name not in NOTIFICATION_KEYS:
                problems.append((here, f"unknown key {field_name!r}"))
        for needed in ("trigger", "recipients", "channels"):
            if not item.get(needed):
                problems.append((here, f"needs {needed}"))
        for channel in item.get("channels") or []:
            if channel not in channels:
                problems.append((here, f"unknown channel {channel}"))
        _catalog_citations(graph, here, item, problems)
        _owner(graph, here, item, "REQ-MESSAGING-0001", key, problems)
    return problems


@check("catalogs")
def upload_types_catalog(graph: Graph):
    problems = []
    for key, item in graph.upload_types.items():
        here = f"graph/catalogs/upload-types.yaml {key}"
        for field_name in item:
            if field_name not in UPLOAD_KEYS:
                problems.append((here, f"unknown key {field_name!r}"))
        if item.get("phase") not in PHASES:
            problems.append((here, "phase must be MVP, P2, or P3"))
        for role in item.get("uploaders") or []:
            if role not in ROLES:
                problems.append((here, f"unknown uploader {role}"))
        if not item.get("uploaders"):
            problems.append((here, "needs uploaders"))
        _catalog_citations(graph, here, item, problems)
        _owner(graph, here, item, "REQ-INTAKE-0002", key, problems)
        names = []
        for column in item.get("columns") or []:
            names.append(column.get("column"))
            col_here = f"{here} column {column.get('column')}"
            for field_name in column:
                if field_name not in COLUMN_KEYS:
                    problems.append((col_here, f"unknown key {field_name!r}"))
            if column.get("required") in (None, ""):
                problems.append((col_here, "needs required"))
            if column.get("kind") not in COLUMN_KINDS:
                problems.append((col_here, f"kind must be one of {', '.join(sorted(COLUMN_KINDS))}"))
            resolved = field_ref(graph, column.get("maps_to"))
            if isinstance(resolved, str):
                problems.append((col_here, resolved))
                continue
            mapped = graph.entities[resolved[0]]["field_map"].get(resolved[1]) or {}
            expected = KIND_OF_FIELD_TYPE.get(mapped.get("type"))
            if expected and column.get("kind") in COLUMN_KINDS and column["kind"] != expected:
                problems.append((col_here, f"kind must be {expected}, because {column['maps_to']} is a {mapped['type']}"))
            saver = column.get("saved_by") or item.get("owner")
            if saver not in graph.requirements:
                problems.append((col_here, f"saved_by {saver!r} is not a requirement"))
                continue
            entity_name, field_name = resolved
            saver_doc = graph.requirements[saver]
            touched = {e for e, _ in entity_refs(graph, saver_doc, "writes")}
            if field_name == "id":
                touched |= {e for e, _ in entity_refs(graph, saver_doc, "reads")}
                if entity_name not in touched:
                    problems.append((col_here, f"{saver} neither reads nor writes {entity_name}"))
            elif not writes_field(graph, saver, entity_name, field_name):
                problems.append((col_here, f"{saver} does not write {entity_name}.{field_name}; set saved_by to its writer"))
        if not names:
            problems.append((here, "needs columns"))
        if len(set(names)) != len(names):
            problems.append((here, "a column repeats"))
        if "identified_by" in item:
            sets = item["identified_by"]
            if not isinstance(sets, list) or not sets or not all(isinstance(one, list) and one for one in sets):
                problems.append((here, "identified_by must be a list of column sets, each with at least one column"))
            else:
                for name in sorted({name for one in sets for name in one} - set(names)):
                    problems.append((here, f"identified_by names {name!r}, which is not a column of the type"))
    return problems


@check("catalogs")
def saved_by_in_owner_closure(graph: Graph):
    """Only a type's owner is called with its rows, so it can pass a column on only to a requirement it depends on."""
    problems = []
    for key, item in graph.upload_types.items():
        owner = item.get("owner")
        if owner not in graph.requirements:
            continue
        closure = graph.dependency_closure(owner)
        for column in item.get("columns") or []:
            saver = column.get("saved_by")
            if saver and saver != owner and saver not in closure:
                here = f"graph/catalogs/upload-types.yaml {key} column {column.get('column')}"
                problems.append((here, f"saved_by {saver} is not a requirement that owner {owner} depends on"))
    return problems


# ---------------------------------------------------------------- review and delivery


@check("review")
def removed_ids_retired(graph: Graph):
    """A requirement id that ever had a file in git history is still a requirement or is retired."""
    from next_requirement_id import history_ids

    if not (graph.root / ".git").exists():
        return []
    gone = history_ids(graph.root, all_branches=False) - set(graph.requirements) - set(graph.retired)
    return [("graph/retired.yaml", f"{requirement_id} was removed without being retired") for requirement_id in sorted(gone)]


@check("review")
def review_state(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        review = doc.get("requirement_review") or {}
        status = review.get("status")
        if status not in REVIEW_STATUSES:
            problems.append((here, f"requirement_review.status must be one of {sorted(REVIEW_STATUSES)}"))
            continue
        if status == "placeholder" and doc.get("requirement_phase") == "MVP":
            problems.append((here, "an MVP requirement cannot be a placeholder"))
        if status == "changes_requested" and not review.get("notes"):
            problems.append((here, "changes_requested needs notes"))
        if status == "approved":
            if review.get("by") not in graph.reviewers:
                problems.append((here, f"approved by {review.get('by')!r}, who is not in graph/reviewers.yaml"))
            if not review.get("at"):
                problems.append((here, "approved needs at"))
            for target in graph.depends_on(requirement_id):
                target_status = (graph.requirements.get(target, {}).get("requirement_review") or {}).get("status")
                if target_status != "approved":
                    problems.append((here, f"approved, but depends on {target}, which is {target_status}"))
            for rid in {requirement_id} | graph.dependency_closure(requirement_id):
                for decision_id in all_requirement_decisions(graph.requirements[rid]):
                    decision = graph.decisions.get(decision_id) or {}
                    if decision.get("blocking") and decision.get("status") == "open":
                        problems.append((here, f"approved, but {rid} rests on open blocking decision {decision_id}"))
    return problems


@check("review")
def delivery_state(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        delivery = doc.get("requirement_delivery") or {}
        status = delivery.get("status")
        pull_requests = delivery.get("pull_requests")
        if status not in DELIVERY_STATUSES:
            problems.append((here, f"requirement_delivery.status must be one of {sorted(DELIVERY_STATUSES)}"))
            continue
        if not isinstance(pull_requests, list):
            problems.append((here, "requirement_delivery.pull_requests must be a list"))
            pull_requests = []
        for url in pull_requests:
            if not isinstance(url, str) or not url.startswith("https://"):
                problems.append((here, f"pull request {url!r} must be an https URL"))
        review_status = (doc.get("requirement_review") or {}).get("status")
        if status in ("in_progress", "delivered") and review_status != "approved":
            problems.append((here, f"{status}, but the requirement is {review_status}, not approved"))
        if status == "delivered":
            if not pull_requests:
                problems.append((here, "delivered needs at least one pull request"))
            for target in graph.depends_on(requirement_id):
                target_status = (graph.requirements.get(target, {}).get("requirement_delivery") or {}).get("status")
                if target_status != "delivered":
                    problems.append((here, f"delivered, but depends on {target}, which is {target_status}"))
    return problems


# ---------------------------------------------------------------- style


@check("style")
def text_shape(graph: Graph):
    problems = []
    for requirement_id, doc in graph.requirements.items():
        here = where(graph, requirement_id)
        title = doc.get("requirement_title") or ""
        if not title or len(title) > TITLE_MAX:
            problems.append((here, f"title must be 1 to {TITLE_MAX} characters"))
        if title.endswith((".", ":", ";", ",")):
            problems.append((here, "title ends with punctuation"))
        if title and not title[0].isupper():
            problems.append((here, "title starts with a capital letter"))
        if REQUIREMENT_ID_IN_TEXT.search(title):
            problems.append((here, "title names a requirement id"))
        statement = " ".join((doc.get("requirement_statement") or "").split())
        parts = sentences(statement)
        if not statement.endswith("."):
            problems.append((here, "statement ends with a period"))
        if not 1 <= len(parts) <= STATEMENT_MAX_SENTENCES:
            problems.append((here, f"statement has {len(parts)} sentences; keep it to 1 to {STATEMENT_MAX_SENTENCES}"))
        for sentence in parts:
            if len(sentence.split()) > SENTENCE_MAX_WORDS:
                problems.append((here, f"a statement sentence has {len(sentence.split())} words; keep each at {SENTENCE_MAX_WORDS} or fewer"))
        for rule in doc.get("requirement_rules") or []:
            if not isinstance(rule, dict):
                continue
            text = " ".join((rule.get("rule_statement") or "").split())
            label = rule.get("rule_id")
            if not text.endswith("."):
                problems.append((here, f"rule {label} ends with a period"))
            if len(sentences(text)) != 1:
                problems.append((here, f"rule {label} must be one sentence"))
            if len(text.split()) > RULE_MAX_WORDS:
                problems.append((here, f"rule {label} has {len(text.split())} words; keep it at {RULE_MAX_WORDS} or fewer"))
    return problems


@check("style")
def glossary(graph: Graph):
    problems = []
    patterns = []
    for term in graph.terms:
        for word in term.get("avoid") or []:
            patterns.append((term.get("term"), word, re.compile(rf"(?<![\w-]){re.escape(word)}(?![\w-])", re.IGNORECASE)))
    for requirement_id, doc in graph.requirements.items():
        for label, text in requirement_text(doc):
            for term, word, pattern in patterns:
                if pattern.search(text):
                    problems.append((where(graph, requirement_id), f"{label} says {word!r}; use {term!r}"))
    return problems


@check("style")
def no_duplicates(graph: Graph):
    problems = []
    seen: dict[str, str] = {}
    for requirement_id, doc in sorted(graph.requirements.items()):
        for label, text in requirement_text(doc):
            if label == "title":
                continue
            normalized = " ".join(text.lower().split())
            if not normalized:
                continue
            if normalized in seen and seen[normalized] != f"{requirement_id} {label}":
                problems.append((where(graph, requirement_id), f"{label} repeats {seen[normalized]} word for word"))
            else:
                seen[normalized] = f"{requirement_id} {label}"
    return problems


# ---------------------------------------------------------------- runner


def run(graph: Graph, suites=None, checks=None):
    results = {}
    for name, (suite, function) in CHECKS.items():
        if suites and suite not in suites:
            continue
        if checks and name not in checks:
            continue
        results[name] = (suite, function(graph))
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(REPO_ROOT), help="repository root that holds graph/ and data-model/")
    parser.add_argument("--suite", action="append", help="run only this suite; repeatable")
    parser.add_argument("--check", action="append", help="run only this check; repeatable")
    parser.add_argument("--list-checks", action="store_true")
    args = parser.parse_args(argv)
    if args.list_checks:
        for name, (suite, function) in CHECKS.items():
            print(f"{suite:12} {name}")
        return 0
    graph = load_graph(args.root)
    results = run(graph, args.suite, args.check)
    total = 0
    for name, (suite, problems) in results.items():
        if problems:
            print(f"\n[{suite}] {name}: {len(problems)} problem(s)")
            for location, message in problems:
                print(f"  {location}: {message}")
            total += len(problems)
    passed = sum(1 for _, problems in results.values() if not problems)
    print(f"\n{passed}/{len(results)} checks passed, {total} problem(s).")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
