#!/usr/bin/env python3
"""List requirements, filtered, in build order (dependencies first).

--ready lists what the factory can build now: approved, not delivered, and every dependency
delivered. --blocking lists each open blocking decision with the requirements it stops from being
approved; every other listing ends with the same counts on stderr.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, Graph, load_graph  # noqa: E402


def build_order(graph: Graph) -> list[str]:
    """Requirement ids with every dependency before its dependents; ties sorted by id."""
    remaining = {rid: {t for t in graph.depends_on(rid) if t in graph.requirements} for rid in graph.requirements}
    order: list[str] = []
    while remaining:
        free = sorted(rid for rid, targets in remaining.items() if not targets)
        if not free:
            order.extend(sorted(remaining))
            break
        for rid in free:
            order.append(rid)
            del remaining[rid]
        for targets in remaining.values():
            targets.difference_update(free)
    return order


def is_ready(graph: Graph, requirement_id: str) -> bool:
    doc = graph.requirements[requirement_id]
    if (doc.get("requirement_review") or {}).get("status") != "approved":
        return False
    if (doc.get("requirement_delivery") or {}).get("status") == "delivered":
        return False
    return all(
        (graph.requirements[t].get("requirement_delivery") or {}).get("status") == "delivered"
        for t in graph.depends_on(requirement_id)
        if t in graph.requirements
    )


def blocking_reach(graph: Graph) -> dict[str, list[str]]:
    """For each open blocking decision, the requirements that cite it or depend on one that does."""
    cited: dict[str, set[str]] = {}
    for rid, doc in graph.requirements.items():
        decisions = set(doc.get("requirement_decisions") or [])
        for rule in doc.get("requirement_rules") or []:
            if isinstance(rule, dict):
                decisions.update(rule.get("rule_decisions") or [])
        cited[rid] = decisions
    reach: dict[str, list[str]] = {}
    for decision_id, decision in graph.decisions.items():
        if decision.get("blocking") is not True or decision.get("status") != "open":
            continue
        reach[decision_id] = sorted(
            rid
            for rid in graph.requirements
            if any(decision_id in cited[r] for r in {rid} | graph.dependency_closure(rid))
        )
    return reach


def blocking_lines(graph: Graph, with_ids: bool = False) -> list[str]:
    lines = []
    for decision_id, stopped in blocking_reach(graph).items():
        mvp = sum(1 for rid in stopped if graph.requirements[rid].get("requirement_phase") == "MVP")
        line = f"{decision_id} is open and blocking: it stops {len(stopped)} requirement(s), {mvp} of them MVP"
        lines.append(f"{line}: {' '.join(stopped)}" if with_ids and stopped else line)
    return lines


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(REPO_ROOT))
    parser.add_argument("--module", action="append", help="repeatable")
    parser.add_argument("--layer", action="append", help="repeatable")
    parser.add_argument("--phase", action="append", help="repeatable")
    parser.add_argument("--review", action="append", help="review status; repeatable")
    parser.add_argument("--delivery", action="append", help="delivery status; repeatable")
    parser.add_argument("--starting-flow", action="store_true")
    parser.add_argument("--ready", action="store_true")
    parser.add_argument("--ids-only", action="store_true")
    parser.add_argument("--blocking", action="store_true", help="list each open blocking decision and what it stops")
    args = parser.parse_args(argv)
    graph = load_graph(args.root)
    if args.blocking:
        print("\n".join(blocking_lines(graph, with_ids=not args.ids_only) or ["No open decision is blocking."]))
        return 0
    for rid in build_order(graph):
        doc = graph.requirements[rid]
        review = (doc.get("requirement_review") or {}).get("status")
        delivery = (doc.get("requirement_delivery") or {}).get("status")
        if args.module and doc.get("requirement_target_module") not in args.module:
            continue
        if args.layer and doc.get("requirement_target_layer") not in args.layer:
            continue
        if args.phase and doc.get("requirement_phase") not in args.phase:
            continue
        if args.review and review not in args.review:
            continue
        if args.delivery and delivery not in args.delivery:
            continue
        if args.starting_flow and doc.get("requirement_starting_flow") is not True:
            continue
        if args.ready and not is_ready(graph, rid):
            continue
        if args.ids_only:
            print(rid)
        else:
            print(f"{rid:26} {doc.get('requirement_phase'):4} {review:18} {delivery:12} {doc.get('requirement_title')}")
    if not args.ids_only:
        for line in blocking_lines(graph):
            print(line, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
