#!/usr/bin/env python3
"""Flag the starting flow: the given requirements and everything they depend on.

Every other requirement is unflagged, so the flow is always closed under DEPENDS_ON.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, load_graph  # noqa: E402

FLAG = re.compile(r"^requirement_starting_flow: (true|false)$", re.M)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("seeds", nargs="+", help="requirement ids at the end of the flow, such as screens")
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)
    graph = load_graph(Path(args.root))
    unknown = [s for s in args.seeds if s not in graph.requirements]
    if unknown:
        print(f"unknown requirement ids: {', '.join(unknown)}", file=sys.stderr)
        return 1
    flow = set(args.seeds)
    for seed in args.seeds:
        flow |= graph.dependency_closure(seed)
    later = sorted(r for r in flow if graph.requirements[r].get("requirement_phase") != "MVP")
    if later:
        print(f"the flow reaches requirements after MVP: {', '.join(later)}", file=sys.stderr)
        return 1
    changed = 0
    for requirement_id, path in graph.paths.items():
        text = path.read_text()
        want = "true" if requirement_id in flow else "false"
        new, count = FLAG.subn(f"requirement_starting_flow: {want}", text)
        if count != 1:
            print(f"{path}: expected one requirement_starting_flow line, found {count}", file=sys.stderr)
            return 1
        if new != text:
            path.write_text(new)
            changed += 1
    print(f"{len(flow)} requirements in the starting flow; {changed} files changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
