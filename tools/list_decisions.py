#!/usr/bin/env python3
"""Print the open decisions grouped by who must answer them, as a list to hand to each party.

Each line gives the decision id, the question, the assumption the graph builds on until it is
answered, and how many MVP rules cite it, most-cited first. --owner limits it to one party, and
--markdown prints a document to send.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, load_graph  # noqa: E402

OWNERS = {
    "COMPASS_OPERATIONS": "Compass operations",
    "COMPASS_HR_LEGAL_PAYROLL": "Compass HR, legal, and payroll",
    "COMPASS_FINANCE": "Compass finance",
    "INSTAWORK_PRODUCT": "Instawork product",
    "INSTAWORK_ENGINEERING": "Instawork engineering",
}


def mvp_citations(graph) -> Counter:
    counts: Counter = Counter()
    for doc in graph.requirements.values():
        if doc.get("requirement_phase") != "MVP":
            continue
        for rule in doc.get("requirement_rules") or []:
            counts.update(rule.get("rule_decisions") or [])
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--owner", choices=sorted(OWNERS))
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    graph = load_graph(args.root)
    counts = mvp_citations(graph)
    for owner, label in OWNERS.items():
        if args.owner and owner != args.owner:
            continue
        open_ones = [d for d in graph.decisions.values() if d.get("answer_from") == owner and d.get("status") == "open"]
        if not open_ones:
            continue
        open_ones.sort(key=lambda d: (not d.get("blocking"), -counts[d["decision_id"]], int(d["decision_id"].split("-")[1])))
        print(f"## {label} ({len(open_ones)} open)\n" if args.markdown else f"{label} ({len(open_ones)} open)")
        for d in open_ones:
            flag = " BLOCKING" if d.get("blocking") else ""
            cited = f"{counts[d['decision_id']]} MVP rules"
            if args.markdown:
                print(f"- **{d['decision_id']}**{flag} ({cited}): {d['question']}\n  Assumed until answered: {d['assumption']}")
            else:
                print(f"  {d['decision_id']}{flag} [{cited}] {d['question']}\n      assumed: {d['assumption']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
