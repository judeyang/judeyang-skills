import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = SKILL_DIR / "scripts" / "audit_delivery_quality.py"
CHECKLIST_SCRIPT = SKILL_DIR / "scripts" / "make_prepublish_checklist.py"
SYNC_SCRIPT = SKILL_DIR / "scripts" / "sync_teleprompter_to_shooting.py"


GOOD_CHIEF = """# 01 主编总控

状态：待人工审查

## 来源与复刻证据

| 编号 | 内容参考 | 结构参考 | 来源关系 |
|---|---|---|---|
| T01 | 原片 A | 原片 A | 内容与结构均匹配 |
| T02 | 原片 B | 原片 C | 内容参考与结构参考已分开 |
| V01 | 门诊日常 D | 日常 Vlog E | 内容与场景均匹配 |
"""


GOOD_EXECUTION = """# 02 执行团队拍摄发布脚本

状态：待人工审查

## 拍摄与交付规范

- 竖屏 9:16，主机位与收音检查后再开拍。

## 发布前检查

- [ ] 封面、字幕、正文和置顶评论已逐项核对。

## 发布后回收

- 记录前三秒、完播、收藏和评论问题类型。

### T01 面诊先分清问题

| 项目 | 内容 |
|---|---|
| 来源关系 | 内容参考：原片 A；结构参考：原片 A |
| 口播全文 | 面诊先别急着问能不能做。先分清皮肤、组织和功能，再谈方向。留言只选一个词：皮肤、组织、功能。 |
| 小红书正文 | 适合谁：准备面诊但不知道先问什么的人。<br>先看什么：先区分皮肤、组织和功能。<br>面诊前准备：整理自然光照片和既往记录。<br>避坑：不要用一张照片替代面诊。<br>收藏点：把三个判断维度记下来。<br>评论引导：只选一个问题类型。 |

| 镜头 | 时间 | 口播 | 画面 | 字幕 | 注意 |
|---|---:|---|---|---|---|
| 1 | 0-3s | 面诊先别急着问能不能做。 | 正面近景，手中不拿道具 | 面诊先分清 | 第一秒进入正文 |
| 2 | 3-12s | 先分清皮肤、组织和功能，再谈方向。 | 白板依次写下三个判断词 | 皮肤 / 组织 / 功能 | 每个词对应一个停顿 |
| 3 | 12-16s | 留言只选一个词：皮肤、组织、功能。 | 回到正面近景 | 只选一个词 | 不判断个人方案 |

### T02 恢复期先看时间

| 项目 | 内容 |
|---|---|
| 来源关系 | 内容参考：原片 B；结构参考：原片 C |
| 口播全文 | 恢复期先看时间，不要每天换一个结论。记录同角度变化，再按复诊要求判断。想看下一期，投票：时间、记录、复诊。 |
| 小红书正文 | 适合谁：恢复期容易被每日变化影响的人。<br>先看什么：先看时间线和变化趋势。<br>面诊前准备：带上同角度照片和复诊记录。<br>避坑：不要自行增加刺激性护理。<br>收藏点：固定角度、固定光线、固定日期。<br>评论引导：只投票问题类型。 |

| 镜头 | 时间 | 口播 | 画面 | 字幕 | 注意 |
|---|---:|---|---|---|---|
| 1 | 0-4s | 恢复期先看时间，不要每天换一个结论。 | 正面中景，桌面摆日历 | 恢复期先看时间 | 语速放慢 |
| 2 | 4-14s | 记录同角度变化，再按复诊要求判断。 | 日历翻页并展示空白记录卡 | 同角度记录 | 不展示真实病例 |
| 3 | 14-18s | 想看下一期，投票：时间、记录、复诊。 | 手指三张关键词卡 | 投票选一类 | 不判断个人方案 |

### V01 门诊问题怎么变成选题

| 项目 | 内容 |
|---|---|
| 来源关系 | 内容参考：门诊日常 D；结构参考：日常 Vlog E |
| 口播全文 | 我会先记录反复出现的问题，再决定下一条讲什么。问题越集中，科普越容易讲清。你更想看哪一类：面诊、恢复、修复？ |
| 小红书正文 | 适合谁：想了解医生如何整理科普选题的人。<br>观众能看到什么：从空白问题卡到选题白板的整理过程。<br>拍摄观察点：只展示分类词，不展示真实资料。<br>隐私边界：患者信息和聊天记录不入镜。<br>收藏点：重复问题比临时灵感更值得记录。<br>评论引导：只投票面诊、恢复或修复。 |

| 镜头 | 时间 | 口播 | 画面 | 字幕 | 注意 |
|---|---:|---|---|---|---|
| 1 | 0-5s | 我会先记录反复出现的问题，再决定下一条讲什么。 | 诊室门牌空镜转空白问题卡 | 重复问题先记录 | 避开人员信息 |
| 2 | 5-18s | 问题越集中，科普越容易讲清。 | 手写分类卡并贴到白板 | 面诊 / 恢复 / 修复 | 只拍手部和空白道具 |
| 3 | 18-24s | 你更想看哪一类：面诊、恢复、修复？ | 正面口播收束 | 选一类 | 不判断个人方案 |
"""


GOOD_SPEAKER = """# 03 余教授本人提词表演稿

状态：待人工审查

## 不能说

- 不说效果保证，不根据评论区照片判断个人方案。

### T01 面诊先分清问题
面诊先别急着问能不能做。先分清皮肤、组织和功能，再谈方向。留言只选一个词：皮肤、组织、功能。

### T02 恢复期先看时间
恢复期先看时间，不要每天换一个结论。记录同角度变化，再按复诊要求判断。想看下一期，投票：时间、记录、复诊。

### V01 门诊问题怎么变成选题
我会先记录反复出现的问题，再决定下一条讲什么。问题越集中，科普越容易讲清。你更想看哪一类：面诊、恢复、修复？
"""


BAD_CHIEF = """# 01 主编总控

| 指标 | 目标 | 本轮结果 |
|---|---:|---:|
| 热度素材贴合度 | >=90% | 38/38 = 100% |
"""


BAD_EXECUTION = """# 02 执行团队拍摄发布脚本

### T01 主题一
| 项目 | 内容 |
|---|---|
| 口播全文 | 主题一正文。评论写：想改哪里。 |
| 小红书正文 | 适合谁：正在纠结主题一的人。<br>先看什么：先看关键词。<br>面诊前准备：自然光正面照片先准备好。<br>避坑：不要发照片。<br>收藏点：逐项自查，沟通会更清楚。 |
| 镜头 | 时间 | 口播 | 画面 | 字幕 | 注意 |
|---|---:|---|---|---|---|
| 1 | 0-5s | 主题一正文。 | 切白板、眼部模型、空白资料夹或手势清单 | 主题一 | 无 |

### T02 主题二
| 项目 | 内容 |
|---|---|
| 口播全文 | 主题二正文。评论写：时间、记录。 |
| 小红书正文 | 适合谁：正在纠结主题二的人。<br>先看什么：先看关键词。<br>面诊前准备：自然光正面照片先准备好。<br>避坑：不要发照片。<br>收藏点：逐项自查，沟通会更清楚。 |
| 镜头 | 时间 | 口播 | 画面 | 字幕 | 注意 |
|---|---:|---|---|---|---|
| 1 | 0-5s | 主题二正文。 | 切白板、眼部模型、空白资料夹或手势清单 | 主题二 | 无 |

### V01 内容复盘
| 项目 | 内容 |
|---|---|
| 口播全文 | 内容复盘正文。评论写：完播、收藏。 |
| 小红书正文 | 适合谁：正在纠结内容复盘的人。<br>先看什么：先看完播和收藏。<br>面诊前准备：自然光正面照片先准备好。<br>避坑：不要发照片。<br>收藏点：逐项自查，沟通会更清楚。 |
| 镜头 | 时间 | 口播 | 画面 | 字幕 | 注意 |
|---|---:|---|---|---|---|
| 1 | 0-5s | 内容复盘正文。 | 切白板、眼部模型、空白资料夹或手势清单 | 内容复盘 | 无 |
"""


BAD_SPEAKER = """# 03 余教授本人提词表演稿

### T01 主题一
主题一正文。评论写：想改哪里。
- 结构模型：真相清单；复刻度 90%。
- 参考原视频：原片 A。
- 热度依据：高热视频。

### T02 主题二
主题二正文。评论写：时间、记录。
- 改写口径：保留爆款节奏。
- 参考原视频：原片 B。

### V01 内容复盘
内容复盘正文。评论写：完播、收藏。
- 结构模型：Vlog 结构。
- 热度依据：高热视频。
"""


class DeliveryQualityAuditTest(unittest.TestCase):
    @staticmethod
    def compact_shot_tables(text: str) -> str:
        lines = []
        for line in text.splitlines():
            if line == "| 镜头 | 时间 | 口播 | 画面 | 字幕 | 注意 |":
                lines.append("| 镜头 | 时间 | 口播 | 画面 |")
            elif line == "|---|---:|---|---|---|---|":
                lines.append("|---|---:|---|---|")
            elif line.startswith("|"):
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) == 6 and cells[0].isdigit():
                    lines.append("| " + " | ".join(cells[:4]) + " |")
                else:
                    lines.append(line)
            else:
                lines.append(line)
        return "\n".join(lines) + "\n"

    def run_audit(self, chief: str, execution: str, speaker: str):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = {
                "chief": root / "01.md",
                "execution": root / "02.md",
                "speaker": root / "03.md",
            }
            paths["chief"].write_text(chief, encoding="utf-8")
            paths["execution"].write_text(execution, encoding="utf-8")
            paths["speaker"].write_text(speaker, encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(AUDIT_SCRIPT),
                    "--chief",
                    str(paths["chief"]),
                    "--execution",
                    str(paths["execution"]),
                    "--speaker",
                    str(paths["speaker"]),
                    "--expected-main",
                    "2",
                    "--expected-vlog",
                    "1",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_rejects_template_heavy_role_mixed_delivery(self):
        result = self.run_audit(BAD_CHIEF, BAD_EXECUTION, BAD_SPEAKER)

        self.assertNotEqual(result.returncode, 0)
        for code in (
            "ROLE_03_METADATA",
            "ROLE_03_FORBIDDEN_MISSING",
            "CTA_PATTERN_OVERUSE",
            "CTA_PERSONAL_SOLICITATION",
            "XHS_TEMPLATE_OVERUSE",
            "XHS_VLOG_WRONG_SCHEMA",
            "SHOT_GENERIC_OVERUSE",
            "SHOT_SPEECH_SYNC_MISMATCH",
            "EXEC_CHECKLIST_MISSING",
            "SOURCE_FIT_UNSUPPORTED",
        ):
            self.assertIn(code, result.stdout)

    def test_accepts_role_clean_platform_specific_delivery(self):
        result = self.run_audit(GOOD_CHIEF, GOOD_EXECUTION, GOOD_SPEAKER)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("QUALITY_GATE_PASS", result.stdout)

    def test_compact_shot_table_still_checks_spoken_line_sync(self):
        compact = self.compact_shot_tables(GOOD_EXECUTION)
        broken = compact.replace(
            "| 1 | 0-3s | 面诊先别急着问能不能做。 |",
            "| 1 | 0-3s | 这句被错误改写。 |",
            1,
        )

        good_result = self.run_audit(GOOD_CHIEF, compact, GOOD_SPEAKER)
        broken_result = self.run_audit(GOOD_CHIEF, broken, GOOD_SPEAKER)

        self.assertEqual(good_result.returncode, 0, good_result.stdout + good_result.stderr)
        self.assertNotEqual(broken_result.returncode, 0)
        self.assertIn("SHOT_SPEECH_SYNC_MISMATCH", broken_result.stdout)

    def test_rejects_unconfirmed_publish_time_and_redundant_execution_tables(self):
        execution = GOOD_EXECUTION.replace(
            "## 拍摄与交付规范",
            "## 总拍摄发布表\n\n| 发布时间 | 编号 |\n|---|---|\n"
            "| 2026-07-13 周一 20:30 | T01 |\n\n"
            "## 原视频参考与节奏复刻依据\n\n重复总表。\n\n"
            "## 拍摄与交付规范",
            1,
        )

        result = self.run_audit(GOOD_CHIEF, execution, GOOD_SPEAKER)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("UNCONFIRMED_PUBLISH_TIME", result.stdout)
        self.assertIn("EXEC_REDUNDANT_AGGREGATE", result.stdout)

    def test_accepts_nonmedical_main_video_without_fake_consultation_prep(self):
        medical_xhs = (
            "| 小红书正文 | 适合谁：恢复期容易被每日变化影响的人。<br>"
            "先看什么：先看时间线和变化趋势。<br>"
            "面诊前准备：带上同角度照片和复诊记录。<br>"
            "避坑：不要自行增加刺激性护理。<br>"
            "收藏点：固定角度、固定光线、固定日期。<br>"
            "评论引导：只投票问题类型。 |"
        )
        operational_xhs = (
            "| 小红书正文 | 适合谁：负责首批内容复盘的主编和运营。<br>"
            "先看什么：分开看前三秒、完播、收藏和评论。<br>"
            "执行要点：按 24 小时和 72 小时回收同一组指标。<br>"
            "避坑：不要用单个点赞数代替全部判断。<br>"
            "收藏点：保存四类指标与下一轮选题的对应关系。<br>"
            "评论引导：只投票下一期想看的指标。 |"
        )
        execution = GOOD_EXECUTION.replace(medical_xhs, operational_xhs)

        result = self.run_audit(GOOD_CHIEF, execution, GOOD_SPEAKER)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("QUALITY_GATE_PASS", result.stdout)

    def test_xiaohongshu_checklist_separates_main_video_and_vlog(self):
        result = subprocess.run(
            [sys.executable, str(CHECKLIST_SCRIPT), "--platform", "xhs"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("## xhs-main", result.stdout)
        self.assertIn("## xhs-main-nonmedical", result.stdout)
        self.assertIn("## xhs-vlog", result.stdout)
        vlog_block = result.stdout.split("## xhs-vlog", 1)[1]
        self.assertIn("观众能看到什么", vlog_block)
        self.assertNotIn("正文是否包含适合谁、先看什么、面诊前准备", vlog_block)
        self.assertIn("是否没有把内容复盘、拍摄道具或选题流程写成面诊前准备", vlog_block)

    def test_sync_scaffold_reads_t_ids_and_excludes_speaker_metadata(self):
        teleprompter = """# 03 提词稿

### T01 主视频
这句才是主视频口播。
- 表演提示：停半拍。
- 参考原视频：不应进入拍摄台词。

### V01 日常
这句才是 Vlog 口播。
- 热度依据：不应进入拍摄台词。
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "03.md"
            output = root / "02.md"
            source.write_text(teleprompter, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SYNC_SCRIPT),
                    str(source),
                    "--out",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            scaffold = output.read_text(encoding="utf-8")
            self.assertIn("## T01 主视频", scaffold)
            self.assertIn("## V01 日常", scaffold)
            self.assertIn("这句才是主视频口播。", scaffold)
            self.assertIn("这句才是 Vlog 口播。", scaffold)
            self.assertNotIn("参考原视频：不应进入拍摄台词", scaffold)
            self.assertNotIn("热度依据：不应进入拍摄台词", scaffold)


if __name__ == "__main__":
    unittest.main()
