#!/usr/bin/env python3
"""Write requirement_starting_flow from graph/starting-flow.yaml: the seeds and everything they depend on.

Pass --add or --remove to change the seed list first. Every other requirement is unflagged, so
the flow is always closed under DEPENDS_ON.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, load_graph  # noqa: E402

FLAG = re.compile(r"^requirement_starting_flow: (true|false)$", re.M)
SEED_LINE = re.compile(r"^- (REQ-\S+)\n", re.M)


def write_seeds(path: Path, seeds: list[str]) -> None:
    text = path.read_text()
    header = text[: SEED_LINE.search(text).start()] if SEED_LINE.search(text) else text.rstrip("\n") + "\n"
    path.write_text(header + "".join(f"- {seed}\n" for seed in seeds))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--add", nargs="*", default=[], help="seed requirement ids to add")
    parser.add_argument("--remove", nargs="*", default=[], help="seed requirement ids to remove")
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)
    root = Path(args.root)
    graph = load_graph(root)
    seeds = [seed for seed in graph.starting_flow_seeds if seed not in args.remove]
    seeds += [seed for seed in args.add if seed not in seeds]
    unknown = [seed for seed in seeds if seed not in graph.requirements]
    if unknown:
        print(f"unknown requirement ids: {', '.join(unknown)}", file=sys.stderr)
        return 1
    if args.add or args.remove:
        write_seeds(root / "graph" / "starting-flow.yaml", seeds)
        graph = load_graph(root)
    flow = graph.starting_flow()
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
    print(f"{len(flow)} requirements in the starting flow from {len(seeds)} seeds; {changed} files changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
