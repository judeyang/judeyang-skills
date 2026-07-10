#!/usr/bin/env python3
"""Generate platform-specific pre-publish checklists."""

from __future__ import annotations

import argparse
from pathlib import Path


CHECKLISTS = {
    "douyin": [
        "前三秒是否直接给冲突句，不寒暄",
        "标题和封面是否只讲一个判断",
        "字幕是否突出关键词，且没有遮挡脸和道具",
        "是否已加医疗边界小字",
        "置顶评论是否只收集问题类型，不做线上诊断",
        "是否没有效果承诺、稀缺营销、患者背书和隐私画面",
    ],
    "xhs-main": [
        "标题是否像用户会搜索的问题",
        "正文是否包含适合谁、先看什么、面诊前准备",
        "面诊前准备是否针对本条主题，而不是复制通用照片清单",
        "是否有收藏清单而不是成交导向",
        "是否避免焦虑化外貌评价",
        "评论引导是否只收集问题类型，不判断个人方案",
        "是否没有私信导流、价格、预约暗示",
    ],
    "xhs-main-nonmedical": [
        "标题是否明确这是内容复盘、制作方法或运营判断",
        "正文是否包含适合谁、先看什么、执行要点、避坑、收藏点、评论引导",
        "是否没有为了套模板强写面诊前准备",
        "执行要点是否给出可操作的时间、指标或步骤",
        "是否没有展示后台账号、用户资料、私信或未公开数据",
        "评论引导是否为主题投票，不延伸个人医疗判断",
    ],
    "xhs-vlog": [
        "标题是否明确这是医生日常、科普制作或场景观察",
        "正文是否包含适合谁、观众能看到什么、拍摄观察点、隐私边界",
        "是否没有把内容复盘、拍摄道具或选题流程写成面诊前准备",
        "是否只展示空白道具、脱敏空镜和类别词",
        "是否有可收藏的方法或观察点",
        "评论引导是否为主题投票或问题分类",
        "是否没有私信导流、价格、预约暗示",
    ],
    "weibo": [
        "第一句是否是可转发观点",
        "正文是否控制在 120-220 字",
        "话题是否少而准",
        "是否保留观点但不攻击外貌或人群",
        "是否没有广告化导流",
    ],
    "wechat": [
        "标题是否是科普问题而不是营销标题",
        "结构是否包含问题、误区、判断维度、准备清单、风险边界",
        "医学建议是否写清适用边界",
        "未确认事实是否标为待确认",
        "文末是否有非诊疗声明",
    ],
}


def build(platforms: list[str]) -> str:
    lines = ["# 发布前 Checklist", "", "发布前只做人工核验，不自动发布。", ""]
    for platform in platforms:
        lines.append(f"## {platform}")
        lines.append("")
        for item in CHECKLISTS[platform]:
            lines.append(f"- [ ] {item}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create platform pre-publish checklist.")
    parser.add_argument(
        "--platform",
        choices=["douyin", "xhs", "xhs-main", "xhs-vlog", "weibo", "wechat", "all"],
        default="all",
    )
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if args.platform == "all":
        platforms = list(CHECKLISTS)
    elif args.platform == "xhs":
        platforms = ["xhs-main", "xhs-main-nonmedical", "xhs-vlog"]
    else:
        platforms = [args.platform]
    report = build(platforms)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
