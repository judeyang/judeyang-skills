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

SAFEGUARD_RE = re.compile(
    r"不说|不写|不用|不承诺|不(?:临时)?添加|不展示|不拍(?:摄)?|不出现|不保存|不转发|"
    r"不放|不包含|不含|不提供|不根据|不判断|不索要|不发送|不比较|不得|禁止|"
    r"别公开|别展示|避免(?:使用|展示|出现|泄露|拍摄|写)|未(?:展示|包含|使用)|"
    r"只用空白|素材隔离|扫描"
)


def is_safeguard_line(line: str, first_risk_index: int) -> bool:
    """Return true when every matched term sits after an explicit prohibition marker."""
    return any(match.end() <= first_risk_index for match in SAFEGUARD_RE.finditer(line))


def scan(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    total = 0
    safeguard_lines = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        matches = []
        for category, pattern in PATTERNS.items():
            match = re.search(pattern, line)
            if match:
                matches.append((category, match))
        if not matches:
            continue
        first_risk_index = min(match.start() for _, match in matches)
        if is_safeguard_line(line, first_risk_index):
            safeguard_lines += 1
            continue
        for category, _ in matches:
            print(f"{path}:{lineno}: [{category}] {line.strip()}")
            total += 1
    return total, safeguard_lines


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Scan Chinese medical-beauty scripts for obvious risk terms.")
    parser.add_argument("files", nargs="+", type=Path, help="Markdown files to scan.")
    args = parser.parse_args(argv[1:])

    total = 0
    safeguard_lines = 0
    for path in args.files:
        path_total, path_safeguards = scan(path)
        total += path_total
        safeguard_lines += path_safeguards
    print(f"Safeguard-only lines: {safeguard_lines}")
    print(f"Total findings: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
