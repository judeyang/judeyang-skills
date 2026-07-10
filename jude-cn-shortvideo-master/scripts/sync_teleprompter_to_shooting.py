#!/usr/bin/env python3
"""Generate a team shooting script from a final teleprompter Markdown file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SECTION_RE = re.compile(r"^###\s+((?:T\d{2})|(?:V\d{2})|(?:\d{2}))\s+(.+)$")


def parse_teleprompter(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    items: list[dict[str, object]] = []
    cur: dict[str, object] | None = None
    body: list[str] = []
    for line in text.splitlines():
        m = SECTION_RE.match(line)
        if m:
            if cur:
                cur["lines"] = body
                items.append(cur)
            cur = {"id": m.group(1), "title": m.group(2).strip()}
            body = []
            continue
        if cur and line.strip() and not line.startswith(("#", "- ", "|")):
            body.append(line.strip())
    if cur:
        cur["lines"] = body
        items.append(cur)
    return items


def chunk_lines(lines: list[str], target_chars: int = 70) -> list[str]:
    chunks: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for line in lines:
        n = len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", line))
        if cur and cur_len + n > target_chars:
            chunks.append(" ".join(cur))
            cur = []
            cur_len = 0
        cur.append(line)
        cur_len += n
    if cur:
        chunks.append(" ".join(cur))
    return chunks


def props_for(title: str) -> str:
    if "纸" in title or "宽双改窄" in title:
        return "A4 白纸、马克笔、透明胶带"
    if "冰敷" in title or "护理" in title:
        return "冰袋、干净纱布、棉签、护理清单卡"
    if "快问快答" in title or "正确示范" in title:
        return "问题卡、正确/错误卡、白板"
    if "Vlog" in title or "一天" in title or "下午" in title:
        return "空白资料夹、诊室空镜、复盘笔记"
    return "眼部模型、眉眼示意图、空白资料夹、风险清单卡"


def visual_for(index: int, total: int, title: str) -> str:
    if index == 1:
        return "正脸开场"
    if index == total:
        return "正脸收束并抛评论问题"
    if "纸" in title:
        return "手部俯拍道具演示"
    if "冰敷" in title or "护理" in title:
        return "手部示范护理动作"
    return "模型、白板或问题卡特写"


def subtitle(text: str) -> str:
    clean = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", text)
    return clean[:22] if clean else "字幕重点"


def build_markdown(items: list[dict[str, object]], source_name: str) -> str:
    out = [
        "# 余教授执行团队拍摄脚本",
        "",
        f"同步来源：`{source_name}`",
        "",
        "## 使用边界",
        "",
        "- 台词同步自最终提词稿，不得脱离提词稿单独改写。",
        "- 现场如调整医学表达，必须先更新最终提词稿，再重新同步本文件。",
        "- 只拍模型、白板、空白资料夹、空镜或完全脱敏道具。",
        "- 结尾小字统一：`内容仅作面诊沟通参考，具体需结合基础、恢复时间、功能和风险判断。`",
        "",
        "## 拍摄总规则",
        "",
        "1. 竖屏 9:16，正脸、手部、道具、空镜交替。",
        "2. 每 5-8 秒换一次画面或字幕重点。",
        "3. 开头第一句直接出，不加问候。",
        "4. 评论区只收集问题类型，不线上诊断，不收照片和私人资料。",
        "",
    ]
    for item in items:
        sid = str(item["id"])
        title = str(item["title"])
        chunks = chunk_lines(item["lines"])  # type: ignore[arg-type]
        props = props_for(title)
        out.extend(
            [
                f"## {sid} {title}",
                "",
                "- 原参考：待主编溯源表确认",
                "- 复刻重点：保留原素材结构功能，按目标账号和合规边界改写。",
                f"- 镜头数：{len(chunks)} 个",
                f"- 封面字：{title[:14]}",
                f"- 统一道具：{props}",
                "- 结尾动作：评论只写问题类型，不做线上诊断。",
                "",
                "| 镜头 | 画面 | 台词 | 字幕重点 | 道具 | 注意事项 |",
                "|---|---|---|---|---|---|",
            ]
        )
        for i, chunk in enumerate(chunks, 1):
            out.append(
                f"| {i} | {visual_for(i, len(chunks), title)} | {chunk} | {subtitle(chunk)} | {props.split('、')[0]} | "
                "只拍模型、白板、空白资料夹或完全脱敏道具。本镜头 5-8 秒内完成，字幕先出关键词。 |"
            )
        out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync final teleprompter into team shooting script.")
    parser.add_argument("teleprompter", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.out.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {args.out}")
    items = parse_teleprompter(args.teleprompter)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_markdown(items, str(args.teleprompter)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
