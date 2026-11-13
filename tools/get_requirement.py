#!/usr/bin/env python3
"""Print a requirement with everything a builder needs to implement it.

The output is YAML: the requirement itself, its direct dependencies and dependents, the
decisions it rests on with the conflicts and inputs tied to them, the full definition of every
entity it reads or writes, the status transitions it makes, the catalog entries it owns, and
the catalog entries its rules name but another requirement owns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, Graph, load_graph, type_targets  # noqa: E402

UPPER_TOKEN = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
DECISION_IN_TEXT = re.compile(r"\bD-\d+\b")
CONFLICT_IN_TEXT = re.compile(r"\bC-\d+\b")
INPUT_IN_TEXT = re.compile(r"\bI-\d+\b")


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
    text = " ".join(
        [doc.get("requirement_statement") or ""] + [rule.get("rule_statement") or "" for rule in doc.get("requirement_rules") or []]
    )
    tokens = set(UPPER_TOKEN.findall(text)) | set(re.findall(r"\b[A-Z]{3,}\b", text))
    module = doc.get("requirement_target_module")
    catalogs = {"settings": graph.settings, "notifications": graph.notifications, "upload_types": graph.upload_types}
    enum_of = {"settings": "SettingKey", "notifications": "NotificationType", "upload_types": "UploadType"}
    used_catalog = {}
    for name, catalog in catalogs.items():
        whole = (graph.enums.get(enum_of[name]) or {}).get("module") == module
        used_catalog[name] = {
            key: catalog[key] for key in sorted(catalog) if (whole or key in tokens) and key not in owns[name]
        }
    named_conflicts = set(CONFLICT_IN_TEXT.findall(text))
    conflicts = {
        conflict_id: conflict
        for conflict_id, conflict in graph.conflicts.items()
        if conflict_id in named_conflicts
        or requirement_id in f"{conflict.get('keep')} {conflict.get('drop')}"
        or decision_ids & set(DECISION_IN_TEXT.findall(f"{conflict.get('keep')} {conflict.get('drop')}"))
    }
    named_inputs = set(INPUT_IN_TEXT.findall(text))
    inputs = {
        input_id: item
        for input_id, item in graph.inputs.items()
        if input_id in named_inputs or decision_ids & set(item.get("decisions") or [])
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
        "decisions": {decision_id: graph.decisions.get(decision_id) for decision_id in sorted(decision_ids, key=lambda d: int(d[2:]))},
        "conflicts": dict(sorted(conflicts.items(), key=lambda item: int(item[0][2:]))),
        "inputs": dict(sorted(inputs.items(), key=lambda item: int(item[0][2:]))),
        "makes_transitions": transitions,
        "owns": {key: value for key, value in owned_catalog.items() if value},
        "uses": {key: value for key, value in used_catalog.items() if value},
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
