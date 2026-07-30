# JudeYang Skills

<p align="center">
  <img src="assets/collection-banner.svg" alt="JudeYang Skills banner">
</p>

<p align="center">
  <strong>Production-grade Agent Skills for document delivery, AI video workflows, prompt design, and FCPXML timelines.</strong>
</p>

<p align="center">
  <a href="#中文">中文</a> · <a href="#english">English</a>
</p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/Skills-5-111827">
  <img alt="Runtime" src="https://img.shields.io/badge/Runtime-SKILL.md-334155">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-0f766e">
</p>

---

## 中文

JudeYang 自用并开源的 Agent Skills 合集。每个目录都是一个可独立安装的 skill，来自真实交付流程，不是演示样例。

### Skill 目录

| Skill | 用途 | 入口 |
|---|---|---|
| [`tujinpdf`](tujinpdf/) | 把现有文档排版成土金色系 A4 杂志风 PDF。 | [`SKILL.md`](tujinpdf/SKILL.md) |
| [`wes-anderson`](wes-anderson/) | AI 短剧/短视频脚本审核、客户确认、资产确认、项目归档。 | [`SKILL.md`](wes-anderson/SKILL.md) |
| [`shot-designer`](shot-designer/) | 视频 Prompt、首尾帧/关键帧规划、参考素材绑定、逐秒镜头控制。 | [`SKILL.md`](shot-designer/SKILL.md) |
| [`fcpx-timeline`](fcpx-timeline/) | 把本地视频、照片、Live Photo 按拍摄时间生成 FCPXML 时间线。 | [`SKILL.md`](fcpx-timeline/SKILL.md) |
| [`jude-cn-shortvideo-master`](jude-cn-shortvideo-master/) | 把医生知识库和逐字稿变成经过角色、平台、来源与可执行性硬审计的三文件短视频交付。 | [`SKILL.md`](jude-cn-shortvideo-master/SKILL.md) |

### 推荐安装

```bash
git clone https://github.com/judeyang/judeyang-skills.git
cp -R judeyang-skills/tujinpdf ~/.codex/skills/
cp -R judeyang-skills/wes-anderson ~/.codex/skills/
cp -R judeyang-skills/shot-designer ~/.codex/skills/
cp -R judeyang-skills/fcpx-timeline ~/.codex/skills/
cp -R judeyang-skills/jude-cn-shortvideo-master ~/.codex/skills/
```

### 组合关系

`wes-anderson` 是视频项目总流程；到 Prompt 生产阶段会调用 `shot-designer`。  
`tujinpdf` 可用于把最终确认材料和项目归档做成用户版 PDF。  
`fcpx-timeline` 是独立工具，用于把本地媒体整理成 Final Cut Pro 时间线。
`jude-cn-shortvideo-master` 负责医生 IP 的素材锁定、平台与数量确认、三角色交付和质量硬门槛。

通用项目执行、普通审查和 Skill 创建不再作为独立 Skill 分发，分别由全局规则、模型原生判断和系统 `skill-creator` 处理。

### 校验命令

```bash
python shot-designer/scripts/validate_prompt_detail.py --input workbook.xlsx
python wes-anderson/scripts/validate_workbook_structure.py workbook.xlsx --type client
python3 fcpx-timeline/scripts/validate-fcpxml.py timeline.fcpxml --fps 30
node tujinpdf/scripts/validate-output.mjs output.html output.pdf preview.png
python3 -m unittest jude-cn-shortvideo-master/tests/test_audit_delivery_quality.py -v
```

---

## English

JudeYang's open-source Agent Skills collection. Each subdirectory is independently installable and comes from real delivery workflows.

### Catalog

| Skill | Best For | Entry |
|---|---|---|
| [`tujinpdf`](tujinpdf/) | Turning existing documents into earthy-gold A4 magazine-style PDFs. | [`SKILL.md`](tujinpdf/SKILL.md) |
| [`wes-anderson`](wes-anderson/) | AI short-video script audit, client confirmation, asset confirmation, and project archives. | [`SKILL.md`](wes-anderson/SKILL.md) |
| [`shot-designer`](shot-designer/) | Video prompts, first/end/keyframe planning, reference binding, and time-coded camera control. | [`SKILL.md`](shot-designer/SKILL.md) |
| [`fcpx-timeline`](fcpx-timeline/) | Generating capture-time ordered Final Cut Pro FCPXML timelines from local media. | [`SKILL.md`](fcpx-timeline/SKILL.md) |
| [`jude-cn-shortvideo-master`](jude-cn-shortvideo-master/) | Turning doctor knowledge bases and transcripts into role-pure, platform-specific, source-audited short-video delivery files. | [`SKILL.md`](jude-cn-shortvideo-master/SKILL.md) |

### Install

```bash
git clone https://github.com/judeyang/judeyang-skills.git
cp -R judeyang-skills/tujinpdf ~/.codex/skills/
cp -R judeyang-skills/wes-anderson ~/.codex/skills/
cp -R judeyang-skills/shot-designer ~/.codex/skills/
cp -R judeyang-skills/fcpx-timeline ~/.codex/skills/
cp -R judeyang-skills/jude-cn-shortvideo-master ~/.codex/skills/
```

### How They Work Together

`wes-anderson` owns the overall AI video production workflow and delegates prompt production to `shot-designer`.  
`tujinpdf` can turn final confirmations and project archive material into user-facing PDFs.  
`fcpx-timeline` is a standalone utility for building Final Cut Pro timelines from local media folders.
`jude-cn-shortvideo-master` governs doctor-IP source intake, platform/count checkpoints, three-role delivery, and hard quality gates.

General project execution, ordinary reviews, and Skill creation are no longer distributed as standalone Skills. They are handled by global rules, native model judgment, and the system `skill-creator`.

### Validation

```bash
python shot-designer/scripts/validate_prompt_detail.py --input workbook.xlsx
python wes-anderson/scripts/validate_workbook_structure.py workbook.xlsx --type client
python3 fcpx-timeline/scripts/validate-fcpxml.py timeline.fcpxml --fps 30
node tujinpdf/scripts/validate-output.mjs output.html output.pdf preview.png
python3 -m unittest jude-cn-shortvideo-master/tests/test_audit_delivery_quality.py -v
```

---

## License

MIT License. See [LICENSE](LICENSE).
