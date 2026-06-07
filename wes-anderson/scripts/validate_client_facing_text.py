#!/usr/bin/env python3
"""Validate text intended for a client-facing AI short-video document."""

from __future__ import annotations

import argparse
from pathlib import Path


BLOCKED_TERMS = {
    "内部制作": "不要向客户暴露内部制作流程",
    "内部统计": "不要向客户暴露内部统计信息",
    "Prompt": "客户归档不应出现内部 Prompt 表述",
    "promote": "客户归档不应出现内部 Prompt 表述",
    "工作量": "客户归档不应出现工作量或结算语言",
    "核算": "客户归档不应出现工作量或结算语言",
    "结算": "客户归档不应出现工作量或结算语言",
    "报价": "客户归档不应出现工作量或结算语言",
    "计费": "客户归档不应出现工作量或结算语言",
    "自动审核": "不要向客户暴露自动审核机制",
    "机器审核": "不要向客户暴露机器审核机制",
    "规则扫描": "不要向客户暴露规则扫描机制",
    "AI自由生成": "请改为官方素材优先的客户友好表述",
    "浪费": "不要使用带有指责色彩的表述",
    "废弃秒数": "不要使用内部返工统计语言",
    "要钱": "不要使用内部商业沟通语言",
}

REVIEW_TERMS = {
    "建立项目文件夹": "建议改写为客户可理解的交付动作",
    "整理为用户已确认版本": "建议改写为确认脚本与形象场景方向",
    "空白项按默认无意见处理": "建议改写为未提出调整的内容按当前方案执行",
    "全部默认无意见": "建议改写为已确认按当前方案执行",
    "制作口径": "建议改写为后续制作依据",
}


def validate(text: str) -> tuple[list[str], list[str]]:
    blocked = [f"`{term}`：{reason}" for term, reason in BLOCKED_TERMS.items() if term in text]
    review = [f"`{term}`：{reason}" for term, reason in REVIEW_TERMS.items() if term in text]
    return blocked, review


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="UTF-8 text manifest containing customer-visible text")
    args = parser.parse_args()

    path = Path(args.input).expanduser()
    text = path.read_text(encoding="utf-8")
    blocked, review = validate(text)

    if blocked:
        print("FAIL: 检测到客户文档禁用措辞")
        print("\n".join(f"- {item}" for item in blocked))
        return 1
    if review:
        print("FAIL: 检测到需要改写的客户文档措辞")
        print("\n".join(f"- {item}" for item in review))
        return 1

    print(f"PASS: {path.name} 已通过客户文档措辞验收")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
