#!/usr/bin/env python3
"""Print a requirement with everything a builder needs to implement it.

The output is YAML: the requirement itself, its direct dependencies and dependents, the
decisions it rests on, the full definition of every entity it reads or writes, the status
transitions it makes, and the catalog entries it owns.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, Graph, load_graph, type_targets  # noqa: E402


def _status(doc: dict) -> dict:
    return {
        "review": (doc.get("requirement_review") or {}).get("status"),
        "delivery": (doc.get("requirement_delivery") or {}).get("status"),
    }


def _entity_view(graph: Graph, name: str) -> dict:
    entity = graph.entities[name]
    view = {
        "module": entity["module"],
        "phase": entity.get("phase"),
        "description": entity.get("description"),
        "fields": entity.get("fields"),
    }
    for key in ("unique", "constraints"):
        if entity.get(key):
            view[key] = entity[key]
    return view


def _enum_view(graph: Graph, name: str) -> dict:
    enum = graph.enums[name]
    view = {"module": enum["module"], "values": enum.get("values")}
    if enum.get("transitions"):
        view["transitions"] = enum["transitions"]
    return view


def requirement_bundle(graph: Graph, requirement_id: str) -> dict:
    doc = graph.requirements[requirement_id]
    block = doc.get("data_model") or {}
    entity_names = []
    for ref in (block.get("reads") or []) + (block.get("writes") or []):
        name = str(ref).partition(".")[0]
        if name in graph.entities and name not in entity_names:
            entity_names.append(name)
    enum_names = []
    for name in entity_names:
        for item in graph.entities[name].get("fields") or []:
            for kind, target in type_targets(item.get("type")):
                if kind == "enum" and target in graph.enums and target not in enum_names:
                    enum_names.append(target)
    decision_ids = set(doc.get("requirement_decisions") or [])
    for rule in doc.get("requirement_rules") or []:
        decision_ids.update(rule.get("rule_decisions") or [])
    transitions = []
    for name, enum in graph.enums.items():
        for transition in enum.get("transitions") or []:
            if transition.get("requirement") == requirement_id:
                transitions.append({"enum": name, "from": transition.get("from"), "to": transition.get("to")})
    owns = {
        "settings": [key for key, item in graph.settings.items() if item.get("owner") == requirement_id],
        "notifications": [key for key, item in graph.notifications.items() if item.get("owner") == requirement_id],
        "upload_types": [key for key, item in graph.upload_types.items() if item.get("owner") == requirement_id],
    }
    owned_catalog = {
        "settings": {key: graph.settings[key] for key in owns["settings"]},
        "notifications": {key: graph.notifications[key] for key in owns["notifications"]},
        "upload_types": {key: graph.upload_types[key] for key in owns["upload_types"]},
    }
    return {
        "requirement": doc,
        "depends_on": [
            {"requirement_id": target, "title": graph.requirements[target].get("requirement_title"), **_status(graph.requirements[target])}
            for target in graph.depends_on(requirement_id)
            if target in graph.requirements
        ],
        "depended_on_by": [
            {"requirement_id": source, "title": graph.requirements[source].get("requirement_title")}
            for source in graph.dependents(requirement_id)
        ],
        "decisions": {decision_id: graph.decisions.get(decision_id) for decision_id in sorted(decision_ids)},
        "makes_transitions": transitions,
        "owns": {key: value for key, value in owned_catalog.items() if value},
        "entities": {name: _entity_view(graph, name) for name in entity_names},
        "enums": {name: _enum_view(graph, name) for name in enum_names},
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("requirement_ids", nargs="+")
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)
    graph = load_graph(args.root)
    missing = [rid for rid in args.requirement_ids if rid not in graph.requirements]
    if missing:
        for rid in missing:
            retired = graph.retired.get(rid)
            hint = f" (retired; replaced by {retired.get('replaced_by')})" if retired else ""
            print(f"unknown requirement {rid}{hint}", file=sys.stderr)
        return 1
    bundles = [requirement_bundle(graph, rid) for rid in args.requirement_ids]
    yaml.safe_dump_all(bundles, sys.stdout, sort_keys=False, allow_unicode=True, width=100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
