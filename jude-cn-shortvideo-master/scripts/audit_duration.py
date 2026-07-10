#!/usr/bin/env python3
"""Estimate Chinese short-video script durations from teleprompter or shooting Markdown."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TELEPROMPTER_SECTION_RE = re.compile(r"^###\s+((?:\d{2})|(?:T\d{2})|(?:V\d{2}))\s+(.+)$")
SHOOTING_SECTION_RE = re.compile(r"^##\s+((?:\d{2})|(?:T\d{2})|(?:V\d{2}))\s+(.+)$")


def spoken_chars(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", text))


def parse_teleprompter(text: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    cur: dict[str, str] | None = None
    body: list[str] = []
    for line in text.splitlines():
        m = TELEPROMPTER_SECTION_RE.match(line)
        if m:
            if cur:
                cur["speech"] = "\n".join(body)
                sections.append(cur)
            sid = m.group(1).replace("T", "")
            cur = {"id": sid, "title": m.group(2).strip()}
            body = []
            continue
        if cur and line.strip() and not line.startswith("#") and not line.startswith("- "):
            body.append(line.strip())
    if cur:
        cur["speech"] = "\n".join(body)
        sections.append(cur)
    return sections


def parse_shooting(text: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    cur: dict[str, str] | None = None
    chunks: list[str] = []
    for line in text.splitlines():
        m = SHOOTING_SECTION_RE.match(line)
        if m:
            if cur:
                cur["speech"] = "\n".join(chunks)
                sections.append(cur)
            sid = m.group(1).replace("T", "")
            cur = {"id": sid, "title": m.group(2).strip()}
            chunks = []
            continue
        if cur and line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and re.fullmatch(r"\d+", cells[0]):
                chunks.append(cells[2])
    if cur:
        cur["speech"] = "\n".join(chunks)
        sections.append(cur)
    return sections


def classify(sid: str, seconds: float) -> str:
    if sid.startswith("V"):
        if seconds < 35:
            return "Vlog偏短，建议补空镜/动作/旁白"
        if seconds > 90:
            return "Vlog偏长，建议拆条或压缩"
        return "适中"
    if seconds < 20:
        return "偏短，适合超短切"
    if seconds <= 45:
        return "适中"
    if seconds <= 75:
        return "偏长，适合小红书/视频号"
    return "过长，建议拆条"


def fmt_seconds(seconds: float) -> str:
    minutes = int(seconds // 60)
    rem = int(round(seconds % 60))
    if rem == 60:
        minutes += 1
        rem = 0
    return f"{minutes}:{rem:02d}" if minutes else f"{rem}s"


def build_report(path: Path, sections: list[dict[str, str]], cpm: int, slow: int, fast: int) -> str:
    total_chars = sum(spoken_chars(s["speech"]) for s in sections)
    lines = [
        "# 时长审计",
        "",
        f"- 来源文件：`{path}`",
        f"- 条目数：{len(sections)}",
        f"- 总字数：{total_chars}",
        f"- 基准速度：{cpm} 字/分钟",
        f"- 估算总时长：{fmt_seconds(total_chars / cpm * 60)}",
        f"- 慢速/快速区间：{fmt_seconds(total_chars / slow * 60)} / {fmt_seconds(total_chars / fast * 60)}",
        "",
        "| 编号 | 标题 | 字数 | 基准时长 | 慢-快区间 | 判断 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for s in sections:
        chars = spoken_chars(s["speech"])
        base = chars / cpm * 60
        slow_sec = chars / slow * 60
        fast_sec = chars / fast * 60
        lines.append(
            f"| {s['id']} | {s['title']} | {chars} | {fmt_seconds(base)} | "
            f"{fmt_seconds(slow_sec)}-{fmt_seconds(fast_sec)} | {classify(s['id'], base)} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit estimated spoken duration for Chinese scripts.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--format", choices=["auto", "teleprompter", "shooting"], default="auto")
    parser.add_argument("--cpm", type=int, default=280, help="Baseline spoken Chinese chars per minute.")
    parser.add_argument("--slow-cpm", type=int, default=240)
    parser.add_argument("--fast-cpm", type=int, default=320)
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8", errors="ignore")
    if args.format == "teleprompter":
        sections = parse_teleprompter(text)
    elif args.format == "shooting":
        sections = parse_shooting(text)
    else:
        shooting = parse_shooting(text)
        teleprompter = parse_teleprompter(text)
        sections = shooting if sum(spoken_chars(s["speech"]) for s in shooting) >= sum(spoken_chars(s["speech"]) for s in teleprompter) else teleprompter

    report = build_report(args.input, sections, args.cpm, args.slow_cpm, args.fast_cpm)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
