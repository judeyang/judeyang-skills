#!/usr/bin/env python3
"""Build a chief-editor-only source trace table for short-video rewrites."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TP_SECTION_RE = re.compile(r"^###\s+((?:\d{2})|(?:V\d{2}))\s+(.+)$")
SH_SECTION_RE = re.compile(r"^##\s+((?:\d{2})|(?:V\d{2}))\s+(.+)$")


def parse_teleprompter(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    items: dict[str, dict[str, str]] = {}
    cur: str | None = None
    body: list[str] = []
    for line in text.splitlines():
        m = TP_SECTION_RE.match(line)
        if m:
            if cur:
                items[cur]["summary"] = compact(body)
            cur = m.group(1)
            items[cur] = {"title": m.group(2).strip(), "summary": ""}
            body = []
            continue
        if cur and line.strip() and not line.startswith("#"):
            body.append(line.strip())
    if cur:
        items[cur]["summary"] = compact(body)
    return items


def compact(lines: list[str], max_chars: int = 90) -> str:
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= max_chars else text[: max_chars - 1] + "…"


def parse_shooting(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    items: dict[str, dict[str, str]] = {}
    cur: str | None = None
    for line in text.splitlines():
        m = SH_SECTION_RE.match(line)
        if m:
            cur = m.group(1)
            items[cur] = {"title": m.group(2).strip(), "source": "待补", "beat": "待补"}
            continue
        if cur and line.startswith("- 原参考："):
            items[cur]["source"] = line.split("：", 1)[1].strip()
        elif cur and line.startswith("- 复刻重点："):
            items[cur]["beat"] = line.split("：", 1)[1].strip()
    return items


def build(teleprompter: Path, shooting: Path | None) -> str:
    tp = parse_teleprompter(teleprompter)
    sh = parse_shooting(shooting) if shooting else {}
    lines = [
        "# 主编专用：逐条溯源表",
        "",
        "> 仅供主编审核素材来源、改写边界和合规取舍。不得发给拍摄团队、剪辑团队、发布团队或外部合作方。",
        "",
        f"- 提词稿：`{teleprompter}`",
    ]
    if shooting:
        lines.append(f"- 拍摄稿：`{shooting}`")
    lines.extend(
        [
            "",
            "| 编号 | 标题 | 原参考 | 复刻重点 | 当前台词摘要 | 主编判断 |",
            "|---|---|---|---|---|---|",
        ]
    )
    for sid, item in tp.items():
        source = sh.get(sid, {}).get("source", "待补")
        beat = sh.get(sid, {}).get("beat", "待补")
        lines.append(
            f"| {sid} | {item['title']} | {source} | {beat} | {item['summary']} | 待主编确认：保留/重写/弃用 |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create chief-editor-only source trace table.")
    parser.add_argument("--teleprompter", required=True, type=Path)
    parser.add_argument("--shooting", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build(args.teleprompter, args.shooting), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
