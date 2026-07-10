#!/usr/bin/env python3
"""Lightweight Chinese medical-beauty content risk scanner."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PATTERNS = {
    "absolute_or_promise": r"(?<!不)一定|必须做|你必须|保证|绝对|永久|无痕|零风险|一次修好|恢复快|安全有效|必做",
    "authority_or_superlative": r"最厉害|行业第一|全国第一|顶级|神手|大师|别人做不了|名气|很难约|排很久|很多外地",
    "patient_testimonial": r"患者说|老患者|真爱粉|朋友说|听别人说|跨城|飞过来|从外地",
    "privacy": r"病历|聊天记录|手机号|付款|身份证|真实姓名|未打码",
    "appearance_shaming": r"畸形|丑|像猴|像老虎|尖嘴猴腮|毁了|残了",
    "diagnosis_to_viewer": r"你就是|你必须做|你适合做|你不适合做|你这个必须",
}


def scan(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    total = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        for category, pattern in PATTERNS.items():
            if re.search(pattern, line):
                print(f"{path}:{lineno}: [{category}] {line.strip()}")
                total += 1
    return total


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Scan Chinese medical-beauty scripts for obvious risk terms.")
    parser.add_argument("files", nargs="+", type=Path, help="Markdown files to scan.")
    args = parser.parse_args(argv[1:])

    total = 0
    for path in args.files:
        total += scan(path)
    print(f"Total findings: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
