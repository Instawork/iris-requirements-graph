#!/usr/bin/env python3
"""Allocate the next requirement ids for a module, above every number it has ever used.

Used numbers come from the current files, graph/retired.yaml, and every requirement file name
in the git history, so a deleted id is never handed out again.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from irisgraph import REPO_ROOT, REQUIREMENT_ID, load_graph  # noqa: E402

ID_IN_PATH = re.compile(r"(REQ-[A-Z][A-Z0-9-]*-\d{4})\.req\.yaml")


def history_ids(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "log", "--all", "--name-only", "--format=", "--", "graph/requirements"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"git log failed: {result.stderr.strip()}")
    return set(ID_IN_PATH.findall(result.stdout))


def next_ids(root: Path, module: str, count: int) -> list[str]:
    graph = load_graph(root)
    if module not in graph.modules:
        raise SystemExit(f"unknown module {module}")
    used = set(graph.requirements) | set(graph.retired) | history_ids(root)
    numbers = [int(match.group(2)) for match in map(REQUIREMENT_ID.match, used) if match and match.group(1) == module]
    start = max(numbers, default=0) + 1
    return [f"REQ-{module}-{number:04d}" for number in range(start, start + count)]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("module", help="module id from graph/layers.yaml, such as TIME or UNIT-WEB")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)
    if args.count < 1:
        raise SystemExit("--count must be at least 1")
    print("\n".join(next_ids(Path(args.root), args.module, args.count)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
