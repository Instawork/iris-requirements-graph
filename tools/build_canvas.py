#!/usr/bin/env python3
"""Generate the Cursor canvas from the graph files.

Writes canvas/iris-requirements-graph.canvas.tsx, which git ignores: the canvas is a view of the
files, so committing it would make every two graph pull requests conflict. --install also copies
it into a Cursor canvases directory so it opens beside a chat.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, Graph, load_graph, table_fields  # noqa: E402
from validate import run  # noqa: E402

TEMPLATE = Path(__file__).resolve().parent / "canvas" / "template.tsx"
OUTPUT_NAME = "iris-requirements-graph.canvas.tsx"
PLACEHOLDER = "/*__GRAPH_JSON__*/"


def _requirement(doc: dict) -> dict:
    block = doc.get("data_model") or {}
    return {
        "id": doc.get("requirement_id"),
        "layer": doc.get("requirement_target_layer"),
        "module": doc.get("requirement_target_module"),
        "phase": doc.get("requirement_phase"),
        "title": doc.get("requirement_title") or "",
        "statement": " ".join((doc.get("requirement_statement") or "").split()),
        "actors": doc.get("requirement_actors") or [],
        "rules": [
            {
                "id": rule.get("rule_id"),
                "text": " ".join((rule.get("rule_statement") or "").split()),
                "src": rule.get("rule_sources") or [],
                "dec": rule.get("rule_decisions") or [],
            }
            for rule in doc.get("requirement_rules") or []
            if isinstance(rule, dict)
        ],
        "src": doc.get("requirement_sources") or [],
        "dec": doc.get("requirement_decisions") or [],
        "features": doc.get("requirement_features") or [],
        "deps": [e.get("requirement_id") for e in doc.get("edges") or [] if isinstance(e, dict)],
        "dm": {
            "status": block.get("status") or "pending",
            "reads": block.get("reads") or [],
            "writes": block.get("writes") or [],
            "detail": block.get("detail"),
        },
        "start": doc.get("requirement_starting_flow") is True,
        "review": (doc.get("requirement_review") or {}).get("status") or "draft",
        "delivery": (doc.get("requirement_delivery") or {}).get("status") or "not_started",
        "prs": (doc.get("requirement_delivery") or {}).get("pull_requests") or [],
    }


def _clean(value):
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, list):
        return [_clean(v) for v in value]
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    return value


def graph_payload(graph: Graph) -> dict:
    module_order = [m["module_id"] for layer in graph.layers for m in layer.get("modules") or []]
    reqs = sorted(
        (_requirement(doc) for doc in graph.requirements.values()),
        key=lambda r: (module_order.index(r["module"]) if r["module"] in module_order else 999, r["id"]),
    )
    checks = [
        {"name": name, "suite": suite, "problems": [f"{where}: {message}" for where, message in problems]}
        for name, (suite, problems) in run(graph).items()
    ]
    payload = {
        "layers": [
            {
                "id": layer.get("layer"),
                "name": layer.get("layer_name"),
                "about": layer.get("about"),
                "modules": [{"id": m["module_id"], "name": m["module_name"], "about": m.get("about")} for m in layer.get("modules") or []],
            }
            for layer in graph.layers
        ],
        "reqs": reqs,
        "entities": [
            {
                "name": name,
                "module": entity["module"],
                "phase": entity.get("phase"),
                "description": entity.get("description") or "",
                "fields": table_fields(entity),
                "unique": entity.get("unique") or [],
                "constraints": entity.get("constraints") or [],
            }
            for name, entity in graph.entities.items()
        ],
        "enums": [
            {
                "name": name,
                "module": enum["module"],
                "values": [{"value": v.get("value"), "meaning": v.get("meaning") or ""} for v in enum.get("values") or []],
                "transitions": enum.get("transitions") or [],
                "catalog": enum.get("catalog"),
            }
            for name, enum in graph.enums.items()
        ],
        "sources": list(graph.sources.values()),
        "decisions": list(graph.decisions.values()),
        "conflicts": list(graph.conflicts.values()),
        "inputs": list(graph.inputs.values()),
        "terms": [{**t, "avoid": t.get("avoid") or [], "source_words": t.get("source_words") or []} for t in graph.terms],
        "capabilities": [{**c, "capability_id": str(c.get("capability_id"))} for c in graph.capabilities.values()],
        "features": [{**f, "capability_id": str(f.get("capability_id"))} for f in graph.features.values()],
        "settings": list(graph.settings.values()),
        "notifications": list(graph.notifications.values()),
        "uploads": list(graph.upload_types.values()),
    }
    payload = _clean(payload)
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
    payload["meta"] = {"digest": f"graph {digest}", "checks": checks}
    return payload


def render(graph: Graph) -> str:
    template = TEMPLATE.read_text()
    if PLACEHOLDER not in template:
        raise SystemExit(f"{TEMPLATE} has no {PLACEHOLDER} marker")
    data = json.dumps(graph_payload(graph), ensure_ascii=False, separators=(",", ":"))
    return template.replace(PLACEHOLDER, data)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(REPO_ROOT))
    parser.add_argument("--install", help="also copy the canvas into this Cursor canvases directory")
    args = parser.parse_args(argv)
    root = Path(args.root)
    output = root / "canvas" / OUTPUT_NAME
    text = render(load_graph(root))
    output.parent.mkdir(exist_ok=True)
    output.write_text(text)
    print(f"wrote {output.relative_to(root)} ({len(text) // 1024} KB)")
    if args.install:
        target = Path(args.install).expanduser() / OUTPUT_NAME
        shutil.copyfile(output, target)
        print(f"installed {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
