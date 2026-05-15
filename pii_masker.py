#!/usr/bin/env python3
"""
PII Masker for text-based documents/transcripts.

Usage examples:
  python pii_masker.py --input meeting.txt --output meeting.masked.txt
  python pii_masker.py --input notes.md --in-place
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PII_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "EMAIL",
        re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
        "[MASKED_EMAIL]",
    ),
    (
        "PHONE",
        re.compile(r"\b(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)\d{3,4}[\s.-]?\d{3,4}\b"),
        "[MASKED_PHONE]",
    ),
    (
        "SSN",
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "[MASKED_SSN]",
    ),
    (
        "CREDIT_CARD",
        re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        "[MASKED_CREDIT_CARD]",
    ),
    (
        "IPV4",
        re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "[MASKED_IP]",
    ),
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def mask_pii(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    masked = text

    for label, pattern, replacement in PII_PATTERNS:
        masked, n = pattern.subn(replacement, masked)
        counts[label] = n

    return masked, counts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mask common PII patterns from text documents/transcripts"
    )
    parser.add_argument("--input", required=True, help="Path to input .txt/.md file")
    parser.add_argument(
        "--output",
        help="Path to output file. If omitted, use --in-place or print to stdout.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input file with masked content.",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Print masking counts per PII type.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.in_place and args.output:
        parser.error("Use either --in-place or --output, not both.")

    try:
        input_path = Path(args.input)
        original = read_text(input_path)
        masked, counts = mask_pii(original)

        if args.in_place:
            write_text(input_path, masked)
            print(f"Masked document written in-place: {input_path}")
        elif args.output:
            output_path = Path(args.output)
            write_text(output_path, masked)
            print(f"Masked document written to: {output_path}")
        else:
            print(masked)

        if args.report:
            print("\nMasking report:")
            for k, v in counts.items():
                print(f"- {k}: {v}")

        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
