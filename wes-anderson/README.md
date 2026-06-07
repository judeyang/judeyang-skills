# 韦斯安德森

[English](README_EN.md) | 中文

![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-d86f64)
![Workflow](https://img.shields.io/badge/Workflow-AI%20Short%20Video-243447)
![Output](https://img.shields.io/badge/Output-Excel%20%2B%20PDF%20%2B%20Prompts-f7d98c)
![Status](https://img.shields.io/badge/Status-Production%20Workflow-d86f64)

![韦斯安德森 banner](assets/banner.svg)

把 AI 短剧/短视频脚本变成可确认、可执行、可归档的制作包。

韦斯安德森不是抽象影评工具，而是面向真实交付的 Agent Skill：它把客户脚本拆成脚本审核、客户确认总表、设定资产制作、Prompt 表、最终确认 PDF 和逐镜内部制作表。

```text
客户脚本 → 脚本审核 → 客户确认 → 设定资产 → 逐镜Prompt → 最终归档
```

![韦斯安德森 animated preview](assets/hero.gif)

---

## 适用场景

- AI 短剧、短视频脚本审核
- 客户脚本修改意见整理
- 人物、场景、产品、道具、特效资产提取
- 脚本审核后生成内部设定资产制作表
- 大头照、全身照、三视图、场景设定图 Prompt
- 客户确认 Excel 和最终确认 PDF
- 内部逐镜图像/视频 Prompt 表

## 不适用场景

- 只需要普通文案润色的任务
- 只需要单张图片提示词的轻量任务
- 未经客户确认就直接生成最终资产的流程
- 把内部 Prompt 工程细节直接发给客户确认的流程

---

## 工作流

![Workflow](assets/workflow.svg)

1. **建项目**：生成项目目录和 `项目名_脚本与资产确认表_v01.xlsx`。
2. **脚本审核**：把脚本审核、资产方向、用户修改意见维护在客户确认总表。
3. **内部资产制作**：生成 `05_内部制作执行/设定资产制作表_v01.xlsx`。
4. **资产回填确认**：把实际人物、场景、道具图片文件名和确认项回填给客户看图确认。
5. **最终确认归档**：生成客户可读的确认 PDF。
6. **内部制作执行**：生成逐镜首帧、尾帧、关键帧和视频内容 Prompt 表。

---

## 输出目录

```text
02_用户确认文件/
03_设定资产/
04_最终确认归档/
05_内部制作执行/
```

---

## 安装

把本目录放到支持 Agent Skills 的 skills 目录下：

```bash
~/.codex/skills/wes-anderson/
```

或使用支持 GitHub 安装的 skills runtime：

```bash
npx skills add judeyang/wes-anderson-skill
```

---

## 触发示例

```text
帮我审核这个 AI 短剧脚本
把这个短视频脚本做成客户确认表
生成人物设定图和场景设定图 Prompt
根据客户确认总表生成逐镜视频 Prompt 表
```

---

## 质量门槛

![Quality gate](assets/quality-gate.svg)

- 客户表格必须使用客户能理解的语言。
- 不在客户确认文件中暴露内部 Prompt 工程细节。
- 不把 `工作量`、`计费`、`结算` 等内部商业语言写进客户归档。
- 每个阶段必须明确当前确认状态和阻塞项。
- 每完成一个阶段，必须主动说明下一步该确认或提供什么。
- 缺少客户素材时标记为 `待提供`，不写成已经确认。
- 不生成额外命名示例文档；命名说明统一维护在 `00_项目说明_文件夹与命名规则.md`。

---

## 🔴 检查点

以下情况必须先确认再继续：

- 把脚本视为已确认前，客户脚本审核意见还没有确认。
- 把角色、场景、产品、道具或特效图片提交给用户前，图片还没有回填到 `项目名_脚本与资产确认表_v01.xlsx`。
- 创建最终确认 PDF 前，脚本、视觉方向和资产图还没有确认。
- 修改 `镜头设计师` 的 `references/prompt_standard.md` 或 Prompt 脚本前，用户没有明确同意。
- 需要公开发布、发送客户或写入生产目录。

---

## 文件结构

```text
wes-anderson/
├── SKILL.md
├── README.md
├── README_EN.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── audit_checklist.md
│   └── client_facing_doc_standard.md
└── scripts/
    ├── audit_script.py
    ├── build_client_confirmation_pdf.py
    ├── create_project.py
    └── validate_client_facing_text.py
```

Prompt 标准、Prompt 表生成和 Prompt 校验已迁移到 `镜头设计师` skill。

---

## License

MIT License. See [LICENSE](LICENSE).
