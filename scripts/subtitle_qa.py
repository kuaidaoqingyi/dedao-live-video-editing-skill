#!/usr/bin/env python3
"""Lightweight QA for Chinese SRT subtitles used in short-video edits."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_FILLERS = [
    "啊",
    "嗯",
    "呃",
    "哎呀",
    "那个",
]

PUNCTUATION_RE = re.compile(r"[，。！？；：“”《》（）、,.!?;:\"'()]")
TIMECODE_RE = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}$")


def parse_bad_terms(items: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in items:
        if "=" not in item:
            raise SystemExit(f"--bad-term must be WRONG=CORRECT, got: {item}")
        wrong, correct = item.split("=", 1)
        pairs.append((wrong.strip(), correct.strip()))
    return pairs


def iter_text_lines(srt_text: str):
    for line_no, line in enumerate(srt_text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.isdigit():
            continue
        if TIMECODE_RE.match(stripped):
            continue
        yield line_no, stripped


def main() -> int:
    parser = argparse.ArgumentParser(description="QA Chinese SRT subtitles.")
    parser.add_argument("srt", type=Path)
    parser.add_argument("--max-chars", type=int, default=16)
    parser.add_argument("--bad-term", action="append", default=[], help="Wrong=Correct term pair")
    parser.add_argument("--filler", action="append", default=[], help="Extra filler word to flag")
    args = parser.parse_args()

    text = args.srt.read_text(encoding="utf-8")
    bad_terms = parse_bad_terms(args.bad_term)
    fillers = DEFAULT_FILLERS + args.filler

    issues: list[str] = []

    for line_no, line in iter_text_lines(text):
        if PUNCTUATION_RE.search(line):
            issues.append(f"{line_no}: punctuation residue: {line}")
        compact = re.sub(r"\s+", "", line)
        if len(compact) > args.max_chars:
            issues.append(f"{line_no}: over {args.max_chars} chars ({len(compact)}): {line}")
        for filler in fillers:
            if filler and filler in compact:
                issues.append(f"{line_no}: filler `{filler}`: {line}")
        for wrong, correct in bad_terms:
            if wrong and wrong in line:
                issues.append(f"{line_no}: bad term `{wrong}` -> `{correct}`: {line}")

    if issues:
        print("\n".join(issues))
        return 1

    print("subtitle qa ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
