#!/usr/bin/env python3
"""Validate that every `pages` entry in docs.json points to an existing .mdx file."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def walk_pages(node) -> list[str]:
    out: list[str] = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, list):
        for x in node:
            out.extend(walk_pages(x))
    elif isinstance(node, dict):
        for k in ("pages", "groups", "tabs", "languages", "versions", "anchors", "dropdowns", "global"):
            if k in node:
                out.extend(walk_pages(node[k]))
    return out


def main() -> int:
    data = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    paths = walk_pages(data.get("navigation", {}))

    missing: list[str] = []
    for p in paths:
        # Strip any anchor
        p_clean = p.split("#", 1)[0]
        if not p_clean:
            continue
        # Absolute URL? skip.
        if p_clean.startswith("http"):
            continue
        candidates = [ROOT / f"{p_clean}.mdx", ROOT / f"{p_clean}.md", ROOT / p_clean]
        if not any(c.is_file() for c in candidates):
            missing.append(p)

    if missing:
        print(f"MISSING {len(missing)} paths:")
        for p in sorted(set(missing)):
            print(f"  - {p}")
        return 1
    print(f"OK — all {len(paths)} navigation paths resolve to files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
