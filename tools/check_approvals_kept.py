#!/usr/bin/env python3
"""Fail when a change drops an approval the base graph has, or edits an approved requirement unreviewed.

An approval is `requirement_review.status: approved`. Each requirement is matched by its id, so
moving a file keeps it. A change to an approved requirement's content keeps the approval only
when `requirement_review.by` names a reviewer in `graph/reviewers.yaml` and `requirement_review.at`
is new, which records who approved the edit. Content is everything except
`requirement_review`, `requirement_delivery`, and `requirement_starting_flow`. An approved id that
is gone from the head fails too: retiring an approved requirement is decided on the pull request.

Usage: `python3 tools/check_approvals_kept.py --base origin/main [--head HEAD]`. Exit 0 when
every approval is kept, 1 when one is not, 2 when git or a file cannot be read.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
NOT_CONTENT = {"requirement_review", "requirement_delivery", "requirement_starting_flow"}


class GitError(Exception):
    pass


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=120, check=False)
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def _yaml_at(root: Path, ref: str, path: str):
    try:
        return yaml.safe_load(_git(root, "show", f"{ref}:{path}"))
    except yaml.YAMLError as error:
        raise GitError(f"{ref}:{path} is not YAML: {error}") from error


def requirements_at(root: Path, ref: str) -> dict[str, dict]:
    found = {}
    for path in _git(root, "ls-tree", "-r", "--name-only", ref, "--", "graph/requirements").splitlines():
        if path.endswith(".req.yaml"):
            doc = _yaml_at(root, ref, path)
            if isinstance(doc, dict) and doc.get("requirement_id"):
                found[doc["requirement_id"]] = doc
    return found


def reviewers_at(root: Path, ref: str) -> set[str]:
    doc = _yaml_at(root, ref, "graph/reviewers.yaml") or {}
    return {item.get("reviewer_id") for item in doc.get("reviewers") or [] if isinstance(item, dict)}


def _review(doc: dict) -> dict:
    review = doc.get("requirement_review")
    return review if isinstance(review, dict) else {}


def _content(doc: dict) -> dict:
    return {key: value for key, value in doc.items() if key not in NOT_CONTENT}


def approval_problems(root: Path, base: str, head: str) -> list[str]:
    merge_base = _git(root, "merge-base", base, head).strip()
    before = requirements_at(root, merge_base)
    after = requirements_at(root, head)
    reviewers = reviewers_at(root, head)
    problems = []
    for requirement_id, old in sorted(before.items()):
        if _review(old).get("status") != "approved":
            continue
        new = after.get(requirement_id)
        if new is None:
            problems.append(f"{requirement_id} was approved and is gone from the graph")
            continue
        review = _review(new)
        if review.get("status") != "approved":
            problems.append(f"{requirement_id} was approved and is now {review.get('status')!r}")
            continue
        if _content(new) != _content(old):
            if review.get("by") not in reviewers:
                problems.append(f"{requirement_id} is approved and edited, but requirement_review.by is not a reviewer")
            if review.get("at") == _review(old).get("at"):
                problems.append(f"{requirement_id} is approved and edited, but requirement_review.at is unchanged")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)
    try:
        problems = approval_problems(Path(args.root), args.base, args.head)
    except GitError as error:
        print(error, file=sys.stderr)
        return 2
    for problem in problems:
        print(problem)
    print(f"{len(problems)} approval problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
