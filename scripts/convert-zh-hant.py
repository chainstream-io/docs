#!/usr/bin/env python3
"""Convert all Simplified Chinese docs to Traditional Chinese (zh-Hant).

Walks the entire cn/ directory tree and produces a mirror under zh-Hant/.
Code blocks, inline code, and technical identifiers are preserved;
only prose text is converted using OpenCC (s2twp).
"""

import os
import re
import sys
from pathlib import Path

from opencc import OpenCC

DOCS_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = DOCS_ROOT / "cn"
DST_ROOT = DOCS_ROOT / "zh-Hant"

cc = OpenCC("s2twp")

CODE_BLOCK_RE = re.compile(r"(```[\s\S]*?```)", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"(`[^`\n]+?`)")
LINK_PATH_RE = re.compile(r"(/cn/)")

PROTECTED_PATTERNS = [
    CODE_BLOCK_RE,
    INLINE_CODE_RE,
]


def convert_file(src_path: Path, dst_path: Path) -> None:
    content = src_path.read_text(encoding="utf-8")

    placeholders: dict[str, str] = {}
    counter = 0

    for pattern in PROTECTED_PATTERNS:
        def replacer(m, _counter=[counter]):
            key = f"\x00PLACEHOLDER_{_counter[0]}\x00"
            _counter[0] += 1
            placeholders[key] = m.group(0)
            return key
        content = pattern.sub(replacer, content)
        counter = len(placeholders)

    content = cc.convert(content)

    content = LINK_PATH_RE.sub("/zh-Hant/", content)

    for key, original in placeholders.items():
        original = LINK_PATH_RE.sub("/zh-Hant/", original)
        content = content.replace(key, original)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(content, encoding="utf-8")


def main():
    if not SRC_ROOT.is_dir():
        print(f"Source directory not found: {SRC_ROOT}")
        sys.exit(1)

    section_filter = sys.argv[1] if len(sys.argv) > 1 else None

    mdx_files = sorted(SRC_ROOT.rglob("*.mdx"))

    if section_filter:
        mdx_files = [f for f in mdx_files if section_filter in str(f.relative_to(SRC_ROOT))]

    if not mdx_files:
        print("No .mdx files found to convert.")
        sys.exit(0)

    converted = 0
    skipped = 0
    for src_path in mdx_files:
        rel = src_path.relative_to(SRC_ROOT)
        dst_path = DST_ROOT / rel

        try:
            convert_file(src_path, dst_path)
            print(f"  OK: {rel}")
            converted += 1
        except Exception as e:
            print(f"  FAIL: {rel} — {e}")
            skipped += 1

    print(f"\nDone — {converted} converted, {skipped} failed out of {len(mdx_files)} files.")


if __name__ == "__main__":
    main()
