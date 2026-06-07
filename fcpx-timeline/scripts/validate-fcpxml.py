#!/usr/bin/env python3

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from typing import List, Optional


TIME_RE = re.compile(r"^(?P<num>-?\d+)(?:/(?P<den>\d+))?s$")


def parse_time(value: str) -> Optional[Fraction]:
    match = TIME_RE.match(value)
    if not match:
        return None
    num = int(match.group("num"))
    den = int(match.group("den") or "1")
    if den == 0:
        return None
    return Fraction(num, den)


def is_frame_safe(value: Fraction, fps: Fraction) -> bool:
    return value * fps == int(value * fps)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated FCPXML timeline.")
    parser.add_argument("fcpxml", type=Path)
    parser.add_argument("--fps", default="30", help="Timeline fps, e.g. 30, 25, 24000/1001")
    args = parser.parse_args()

    if not args.fcpxml.exists():
        print(f"FAIL: file does not exist: {args.fcpxml}")
        return 1

    try:
        fps = Fraction(args.fps)
    except Exception:
        print(f"FAIL: invalid --fps value: {args.fps}")
        return 2

    try:
        tree = ET.parse(args.fcpxml)
    except ET.ParseError as exc:
        print(f"FAIL: XML parse error: {exc}")
        return 1

    root = tree.getroot()
    failures: List[str] = []

    if root.tag != "fcpxml":
        failures.append(f"root tag must be fcpxml, got {root.tag}")

    for tag in ["resources", "library", "event", "project", "sequence", "spine"]:
        if root.find(f".//{tag}") is None:
            failures.append(f"missing <{tag}> element")

    for elem in root.iter():
        for attr in ["duration", "offset", "start", "tcStart"]:
            value = elem.attrib.get(attr)
            if not value:
                continue
            parsed = parse_time(value)
            if parsed is None:
                failures.append(f"{elem.tag}@{attr} has unsupported time format: {value}")
                continue
            if not is_frame_safe(parsed, fps):
                failures.append(f"{elem.tag}@{attr} is not frame-safe at {fps}fps: {value}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(f"PASS: {args.fcpxml} is structurally valid and frame-safe at {fps}fps")
    return 0


if __name__ == "__main__":
    sys.exit(main())
