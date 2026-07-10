#!/usr/bin/env python3
"""Audit role purity, platform specificity, source claims, and cross-file sync."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


SECTION_RE = re.compile(r"^###\s+([TV]\d{2})\s+(.+)$", re.MULTILINE)
ROLE_03_METADATA_MARKERS = (
    "- 结构模型：",
    "- 改写口径：",
    "- 参考原视频：",
    "- 热度依据：",
    "复刻度",
)
REQUIRED_EXECUTION_HEADINGS = (
    "## 拍摄与交付规范",
    "## 发布前检查",
    "## 发布后回收",
)
MAIN_XHS_LABELS = (
    "适合谁：",
    "先看什么：",
    "面诊前准备：",
    "避坑：",
    "收藏点：",
    "评论引导：",
)
VLOG_XHS_LABELS = (
    "适合谁：",
    "观众能看到什么：",
    "拍摄观察点：",
    "隐私边界：",
    "收藏点：",
    "评论引导：",
)
GENERIC_SHOT_PHRASES = (
    "切白板、眼部模型、空白资料夹或手势清单",
    "模型、白板或问题卡特写",
)
TEMPLATE_PHRASES = (
    "正在纠结",
    "自然光正面、侧面、闭眼、睁眼照片先准备好",
    "逐项自查，沟通会更清楚",
)
PERSONAL_SOLICITATION_PHRASES = (
    "评论写：想改哪里",
    "评论区写想改哪里",
    "留言说说你的情况",
    "评论区发照片",
    "发照片我帮你看",
)


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def parse_sections(text: str) -> dict[str, dict[str, str]]:
    matches = list(SECTION_RE.finditer(text))
    sections: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = {
            "title": match.group(2).strip(),
            "body": text[match.end() : end],
        }
    return sections


def table_field(body: str, field: str) -> str:
    pattern = re.compile(rf"^\|\s*{re.escape(field)}\s*\|\s*(.*?)\s*\|$", re.MULTILINE)
    match = pattern.search(body)
    return match.group(1).strip() if match else ""


def first_speech_line(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", "- ", "|")):
            return stripped
    return ""


def normalize_speech(text: str) -> str:
    return re.sub(r"\s+", "", text)


def shot_table_speech(body: str) -> str:
    chunks: list[str] = []
    for line in body.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"\d+", cells[0]):
            chunks.append(cells[2])
    return "".join(chunks)


def add_count_findings(
    findings: list[Finding],
    execution_sections: dict[str, dict[str, str]],
    speaker_sections: dict[str, dict[str, str]],
    expected_main: int | None,
    expected_vlog: int | None,
) -> None:
    if set(execution_sections) != set(speaker_sections):
        findings.append(Finding("SECTION_ID_MISMATCH", "02 与 03 的条目编号不一致。"))

    if expected_main is not None:
        actual_main = sum(section_id.startswith("T") for section_id in speaker_sections)
        if actual_main != expected_main:
            findings.append(
                Finding("MAIN_COUNT_MISMATCH", f"主视频应为 {expected_main} 条，03 实际为 {actual_main} 条。")
            )
    if expected_vlog is not None:
        actual_vlog = sum(section_id.startswith("V") for section_id in speaker_sections)
        if actual_vlog != expected_vlog:
            findings.append(
                Finding("VLOG_COUNT_MISMATCH", f"Vlog 应为 {expected_vlog} 条，03 实际为 {actual_vlog} 条。")
            )


def add_sync_findings(
    findings: list[Finding],
    execution_sections: dict[str, dict[str, str]],
    speaker_sections: dict[str, dict[str, str]],
) -> None:
    mismatches: list[str] = []
    shot_mismatches: list[str] = []
    for section_id in sorted(set(execution_sections) & set(speaker_sections)):
        execution_speech = table_field(execution_sections[section_id]["body"], "口播全文")
        speaker_speech = first_speech_line(speaker_sections[section_id]["body"])
        if not execution_speech or execution_speech != speaker_speech:
            mismatches.append(section_id)
        shot_speech = shot_table_speech(execution_sections[section_id]["body"])
        if shot_speech and normalize_speech(shot_speech) != normalize_speech(execution_speech):
            shot_mismatches.append(section_id)
    if mismatches:
        findings.append(
            Finding("SPEECH_SYNC_MISMATCH", f"02/03 口播不一致：{', '.join(mismatches)}。")
        )
    if shot_mismatches:
        findings.append(
            Finding(
                "SHOT_SPEECH_SYNC_MISMATCH",
                f"02 的口播全文与逐镜头台词不一致：{', '.join(shot_mismatches)}。",
            )
        )


def add_speaker_findings(
    findings: list[Finding], speaker_text: str, speaker_sections: dict[str, dict[str, str]]
) -> None:
    markers = [marker for marker in ROLE_03_METADATA_MARKERS if marker in speaker_text]
    if markers:
        findings.append(
            Finding(
                "ROLE_03_METADATA",
                "03 含主编元数据，应移出余教授文件：" + "、".join(markers) + "。",
            )
        )
    if "## 不能说" not in speaker_text:
        findings.append(Finding("ROLE_03_FORBIDDEN_MISSING", "03 缺少明确的“不能说”清单。"))

    speeches = [first_speech_line(section["body"]) for section in speaker_sections.values()]
    repeated_cta = sum("评论写：" in speech for speech in speeches)
    if len(speeches) >= 3 and repeated_cta / len(speeches) > 0.5:
        findings.append(
            Finding(
                "CTA_PATTERN_OVERUSE",
                f"{repeated_cta}/{len(speeches)} 条使用同一“评论写”收尾，仍有明显模板感。",
            )
        )
    personal_items = [
        section_id
        for section_id, section in speaker_sections.items()
        if any(phrase in first_speech_line(section["body"]) for phrase in PERSONAL_SOLICITATION_PHRASES)
    ]
    if personal_items:
        findings.append(
            Finding(
                "CTA_PERSONAL_SOLICITATION",
                "评论引导正在收集个人诉求或照片，应改为问题分类或选题投票："
                + ", ".join(personal_items)
                + "。",
            )
        )


def add_execution_findings(
    findings: list[Finding], execution_text: str, execution_sections: dict[str, dict[str, str]]
) -> None:
    missing_headings = [heading for heading in REQUIRED_EXECUTION_HEADINGS if heading not in execution_text]
    if missing_headings:
        findings.append(
            Finding("EXEC_CHECKLIST_MISSING", "02 缺少：" + "、".join(missing_headings) + "。")
        )

    xhs_bodies: dict[str, str] = {}
    missing_xhs: list[str] = []
    main_schema_errors: list[str] = []
    vlog_schema_errors: list[str] = []
    missing_source_relation: list[str] = []
    generic_shot_sections: set[str] = set()

    for section_id, section in execution_sections.items():
        body = section["body"]
        xhs = table_field(body, "小红书正文")
        xhs_bodies[section_id] = xhs
        if not xhs:
            missing_xhs.append(section_id)
        elif section_id.startswith("V"):
            if any(label not in xhs for label in VLOG_XHS_LABELS) or "面诊前准备：" in xhs:
                vlog_schema_errors.append(section_id)
        elif any(label not in xhs for label in MAIN_XHS_LABELS):
            main_schema_errors.append(section_id)

        relation = table_field(body, "来源关系")
        if "内容参考" not in relation or "结构参考" not in relation:
            missing_source_relation.append(section_id)

        if any(phrase in body for phrase in GENERIC_SHOT_PHRASES):
            generic_shot_sections.add(section_id)

    if missing_xhs:
        findings.append(Finding("XHS_COPY_MISSING", "缺少小红书正文：" + ", ".join(missing_xhs) + "。"))
    if main_schema_errors:
        findings.append(
            Finding("XHS_MAIN_SCHEMA_MISSING", "主视频小红书字段不完整：" + ", ".join(main_schema_errors) + "。")
        )
    if vlog_schema_errors:
        findings.append(
            Finding(
                "XHS_VLOG_WRONG_SCHEMA",
                "Vlog 不应套用面诊模板，应使用场景/观察点/隐私边界：" + ", ".join(vlog_schema_errors) + "。",
            )
        )

    if xhs_bodies:
        overused = []
        for phrase in TEMPLATE_PHRASES:
            count = sum(phrase in body for body in xhs_bodies.values())
            if count / len(xhs_bodies) > 0.5:
                overused.append(f"“{phrase}” {count}/{len(xhs_bodies)}")
        if overused:
            findings.append(Finding("XHS_TEMPLATE_OVERUSE", "小红书正文批量套句：" + "；".join(overused) + "。"))

    if execution_sections and len(generic_shot_sections) / len(execution_sections) > 0.25:
        findings.append(
            Finding(
                "SHOT_GENERIC_OVERUSE",
                f"{len(generic_shot_sections)}/{len(execution_sections)} 条使用通用分镜占位语，必须改成主题专属动作。",
            )
        )

    if missing_source_relation:
        execution_text_has_unqualified_claim = bool(
            re.search(r"(?:贴合度|覆盖率).*100%|38/38\s*=\s*100%", execution_text)
        )
        if execution_text_has_unqualified_claim:
            findings.append(
                Finding(
                    "SOURCE_FIT_UNSUPPORTED",
                    "声称来源贴合 100%，但条目缺少“内容参考/结构参考”关系证据。",
                )
            )


def audit(
    chief_text: str,
    execution_text: str,
    speaker_text: str,
    expected_main: int | None,
    expected_vlog: int | None,
) -> list[Finding]:
    execution_sections = parse_sections(execution_text)
    speaker_sections = parse_sections(speaker_text)
    findings: list[Finding] = []

    add_count_findings(findings, execution_sections, speaker_sections, expected_main, expected_vlog)
    add_sync_findings(findings, execution_sections, speaker_sections)
    add_speaker_findings(findings, speaker_text, speaker_sections)
    add_execution_findings(findings, execution_text, execution_sections)

    if re.search(r"(?:贴合度|覆盖率).*100%|38/38\s*=\s*100%", chief_text):
        missing_relation = [
            section_id
            for section_id, section in execution_sections.items()
            if "内容参考" not in table_field(section["body"], "来源关系")
            or "结构参考" not in table_field(section["body"], "来源关系")
        ]
        if missing_relation and not any(f.code == "SOURCE_FIT_UNSUPPORTED" for f in findings):
            findings.append(
                Finding(
                    "SOURCE_FIT_UNSUPPORTED",
                    "01 声称来源贴合 100%，但 02 未逐条区分内容参考与结构参考。",
                )
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit three-file Chinese short-video delivery quality.")
    parser.add_argument("--chief", required=True, type=Path)
    parser.add_argument("--execution", required=True, type=Path)
    parser.add_argument("--speaker", required=True, type=Path)
    parser.add_argument("--expected-main", type=int)
    parser.add_argument("--expected-vlog", type=int)
    args = parser.parse_args()

    findings = audit(
        args.chief.read_text(encoding="utf-8", errors="ignore"),
        args.execution.read_text(encoding="utf-8", errors="ignore"),
        args.speaker.read_text(encoding="utf-8", errors="ignore"),
        args.expected_main,
        args.expected_vlog,
    )

    counts = Counter(finding.code for finding in findings)
    for finding in findings:
        print(f"[ERROR] {finding.code}: {finding.message}")
    if findings:
        print(f"QUALITY_GATE_FAIL: {len(findings)} findings across {len(counts)} checks")
        return 1

    print("QUALITY_GATE_PASS: role purity, platform copy, source evidence, shots, counts, and sync passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
