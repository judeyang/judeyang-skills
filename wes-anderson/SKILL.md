---
name: wes-anderson
description: "AI short-video project pilot for scripts, client confirmation workbooks, asset workflows, final confirmation PDFs, revision tracking, and internal prompt tables. Trigger on AI短剧项目领航、脚本审核、脚本与资产确认表、设定资产制作表、人物/场景/产品设定图、用户修改意见、确认归档、韦斯安德森项目领航. This is not a director-style prompt skill. MUST end active responses with exactly four lines: 本阶段已完成 / CHECKPOINT · 当前需要你确认/提供 / 确认后我将进入 / 暂不执行的内容."
---

# 韦斯安德森项目领航

> Created by JudeYang.

Recommended human-facing name: **韦斯安德森项目领航**.

## Activation Override

When the user says `韦斯安德森项目领航`, `韦斯安德森项目领航继续`, or activates this skill by name, treat it as this project-pilot skill. Do not interpret this skill as a request to write Wes Anderson-style visual prompts unless the user explicitly says they only want visual style language.

Do not promote the legacy shorthand `韦斯安德森` as the activation phrase. It is ambiguous with director-style visual prompting. For project-pilot work, ask the user to use `韦斯安德森项目领航`.

The primary job is phase control, confirmation gates, folder/workbook discipline, and safe project delivery. Visual style discussion is secondary and must not replace the project-pilot workflow.

## Non-Negotiable Output Format

Every active project-pilot response must end with exactly these four lines:

```text
本阶段已完成：...
CHECKPOINT · 当前需要你确认/提供：...
确认后我将进入：...
暂不执行的内容：...
```

This is mandatory. If the response would otherwise end with `阶段/输入/产物/检查点`, `状态/下一步/归档/文件`, or any custom summary, rewrite the ending into the four lines above before sending.

Common trigger templates:

If the user says they just received a project, has script/product images, wants to start, or says `韦斯安德森项目领航`, output a short project-pilot response ending with:

```text
本阶段已完成：识别为 Phase 1 · 原始脚本接收，当前不进入资产Prompt、逐镜Prompt或视频生成
CHECKPOINT · 当前需要你确认/提供：客户脚本文件/原文、产品图路径、交付比例/时长/平台、不可改内容和官方素材清单
确认后我将进入：创建项目文件夹、生成 02_用户确认文件/项目名_脚本与资产确认表_v01.xlsx，并做脚本审核
暂不执行的内容：资产Prompt、逐镜视频Prompt表、视频生成、最终确认PDF
```

If the user says assets are confirmed and asks to directly create per-shot video prompts, output a short gatekeeping response ending with:

```text
本阶段已完成：确认人物和场景图已通过，但尚未看到 04_最终确认归档/ 下的最终确认PDF/HTML归档
CHECKPOINT · 当前需要你确认/提供：最终确认PDF/HTML归档路径，或确认是否先生成 04_最终确认归档/项目名_脚本与设定资产最终确认归档_vNN.pdf
确认后我将进入：基于最终确认归档生成 05_内部制作执行/内部执行脚本与Prompt表_vNN.xlsx
暂不执行的内容：逐镜视频Prompt表、视频生成
```

If the user submits client revision feedback, output a short feedback-normalization response ending with:

```text
本阶段已完成：已拆解本轮客户修改意见，并映射到固定项目路径
CHECKPOINT · 当前需要你确认/提供：客户原话、参考图文件名/路径、当前项目名和最新 vNN 版本号
确认后我将进入：写入 02_用户确认文件/用户修改意见记录_vNN.xlsx，并同步标注受影响的确认表/资产表
暂不执行的内容：资产Prompt、逐镜视频Prompt表、视频生成、最终确认PDF
```

Use this skill to convert a client script into a confirmed, executable AI video production package.

The goal is practical delivery, not abstract critique:
- Use Excel for anything the client or producer must edit, choose, or review.
- Use PDF only after the relevant content is confirmed and needs archiving.
- Use the final internal execution workbook for production, not for client feedback.

For the main client confirmation workbook, put the two most important worksheet tabs first:
1. `脚本审核确认表`
2. `形象场景描述确认表`

This workbook is usually named `项目名_脚本与资产确认表_v01.xlsx`. Do not split `执行版脚本.xlsx` or `形象场景描述确认表.xlsx` into separate user-facing files unless the user explicitly asks. Instruction, source-record, full-script, asset-image confirmation, or archive sheets can follow after these two tabs.

For client-facing Excel formatting:
- Short structured columns should be horizontally centered, such as `序号`, `镜号`, `对应镜号/范围`, `景别`, `时长`, `类别`, `问题类型`, `风险等级`, `严重度`, `用户确认`, and status columns.
- Long text columns should be left aligned and wrapped, such as `画面内容`, `台词/旁白`, `原始内容摘要`, `建议`, `需要用户确认`, `用户意见/选择`, `补充意见`, `初步设定方向`, and `风险/说明`.
- Header rows stay centered. Body rows stay vertically top-aligned.

Client-facing confirmation sheets should only describe steps that require client participation. Do not write internal production steps such as `进入内部执行脚本与Prompt表` in a client confirmation workbook. Use client-facing wording such as `设定图确认后，进入后续视频制作阶段` when a next-step note is necessary.

When a client-facing confirmation table is missing source material from the client, use `待提供` instead of `待补充`. Example: if product images, logo, remote-control reference, font authorization, music authorization, or brand guideline files have not been supplied, mark the status as `待提供` and state what the client should provide. Reserve `待补充` only for neutral internal drafts, not user-facing material-status cells.

## Operating Contract

Before creating files, identify the current project phase and the exact input source.

Also identify the project type before choosing workbook emphasis:
- `产品广告`
- `AI短剧`
- `品牌片`
- `口播知识片`
- `电商种草片`
- `其他`

Project type controls confirmation priorities only. It does not change the fixed folder contract or allow skipping phase gates.

## Response Contract

Whenever this skill is active, the assistant response must end with this exact four-line status block. Do not replace it with prose, bullets, or a different checkpoint label.

```text
本阶段已完成：...
CHECKPOINT · 当前需要你确认/提供：...
确认后我将进入：...
暂不执行的内容：...
```

Rules for the status block:
- Always include all four lines, even when no file was created.
- If there is not enough room or the situation is simple, output only the four-line status block. Never omit it.
- `CHECKPOINT · 当前需要你确认/提供：...` must name the exact missing input, file, path, or decision blocking the next phase.
- `暂不执行的内容：...` must explicitly name downstream work that is blocked, such as `逐镜视频Prompt表`, `视频生成`, `最终确认PDF`, or `资产Prompt`.
- If the user asks to skip ahead, the response must still end with the four-line status block and must mark the skipped work under `暂不执行的内容`.
- Do not output any alternative ending such as `下一步建议`, `关键 checkpoint`, `请把...发我`, or `我会...` unless the four-line status block is still present after it.
- Do not end with labels such as `阶段`, `输入`, `产物`, `检查点`, `下一步`, or `逐镜Prompt表`; convert them into the four required lines.
- Before sending, run this self-check: if the final four non-empty lines do not start with exactly `本阶段已完成：`, `CHECKPOINT · 当前需要你确认/提供：`, `确认后我将进入：`, and `暂不执行的内容：`, rewrite the ending.
- Any response ending with `阶段：`, `输入：`, `产物：`, `检查点：`, `状态：`, `下一步：`, `归档：`, or `文件：` is invalid.
- Do not say `可以进入逐镜视频 Prompt 表` or `确认后生成逐镜视频Prompt表` unless `04_最终确认归档/` already contains the final confirmation PDF/HTML archive. If that archive is not present, say the final confirmation archive is the next gate.

Minimal valid response examples:

Project start:
```text
本阶段已完成：识别为 Phase 1 · 原始脚本接收，当前不进入资产Prompt、逐镜Prompt或视频生成
CHECKPOINT · 当前需要你确认/提供：客户脚本文件/原文、产品图路径、交付比例/时长/平台、不可改内容和官方素材清单
确认后我将进入：创建项目文件夹、生成 02_用户确认文件/项目名_脚本与资产确认表_v01.xlsx，并做脚本审核
暂不执行的内容：资产Prompt、逐镜视频Prompt表、视频生成、最终确认PDF
```

Skip-ahead request before final confirmation archive:
```text
本阶段已完成：确认人物和场景图已通过，但尚未看到 04_最终确认归档/ 下的最终确认PDF归档
CHECKPOINT · 当前需要你确认/提供：最终确认PDF/HTML归档路径，或确认是否先生成 04_最终确认归档/项目名_脚本与设定资产最终确认归档_vNN.pdf
确认后我将进入：基于最终确认归档生成 05_内部制作执行/内部执行脚本与Prompt表_vNN.xlsx
暂不执行的内容：逐镜视频Prompt表、视频生成
```

## Path Contract

When naming folders, affected files, or next files, use only paths from this fixed whitelist unless the user explicitly gives an existing project path or asks for a new exact folder name:

```text
00_项目说明_文件夹与命名规则.md
01_客户原始资料/01_脚本/
01_客户原始资料/02_产品素材/
01_客户原始资料/03_用户反馈参考图/
02_用户确认文件/
02_用户确认文件/项目名_脚本与资产确认表_vNN.xlsx
02_用户确认文件/用户修改意见记录_vNN.xlsx
03_设定资产/01_人物设定图/
03_设定资产/02_场景设定图/
03_设定资产/03_产品参考图/
03_设定资产/04_道具设定图/
03_设定资产/05_特效关键帧/
04_最终确认归档/
05_内部制作执行/
05_内部制作执行/设定资产制作表_vNN.xlsx
05_内部制作执行/内部执行脚本与Prompt表_vNN.xlsx
05_内部制作执行/01_首帧与关键帧/
05_内部制作执行/02_视频片段/
05_内部制作执行/03_成片/
05_内部制作执行/04_封面/
```

Forbidden invented paths include:
- `01_脚本分镜/`
- `03_角色设定/`
- `04_画面提示词/`
- `05_生成素材/`
- `06_视频工程/`
- `客户反馈/`
- `视频Prompt/`
- `提示词参考/`

If a model wants to say "downstream files are affected", it must map the impact to the whitelist. Examples:
- script, shot, or product-entry logic changes -> `02_用户确认文件/项目名_脚本与资产确认表_vNN.xlsx`
- client feedback records -> `02_用户确认文件/用户修改意见记录_vNN.xlsx`
- character costume or face changes -> `03_设定资产/01_人物设定图/` and, if prompts already exist, `05_内部制作执行/设定资产制作表_vNN.xlsx`
- scene reference changes -> `03_设定资产/02_场景设定图/`
- product appearance or official asset changes -> `01_客户原始资料/02_产品素材/` and `03_设定资产/03_产品参考图/`
- prop changes -> `03_设定资产/04_道具设定图/`
- effect/keyframe changes -> `03_设定资产/05_特效关键帧/` and `05_内部制作执行/01_首帧与关键帧/`
- per-shot video prompt changes -> `05_内部制作执行/内部执行脚本与Prompt表_vNN.xlsx`
- generated clips -> `05_内部制作执行/02_视频片段/`
- finished cuts -> `05_内部制作执行/03_成片/`

## Project Folder Contract

For AI short-drama / AI short-video delivery projects, use the established project folder format from:
`/path/to/卡萨帝空调红楼梦AI短剧_项目交付文件夹`

Do not invent a new directory layout per project. When scaffolding a project, create only the fixed standard directories below. Do not create broad "maybe useful" extra folders outside this contract.

Default fixed structure:

```text
项目名_项目交付文件夹/
  00_项目说明_文件夹与命名规则.md
  01_客户原始资料/
    01_脚本/
    02_产品素材/
    03_用户反馈参考图/
  02_用户确认文件/
  03_设定资产/
    01_人物设定图/
    02_场景设定图/
    03_产品参考图/
    04_道具设定图/
    05_特效关键帧/
  04_最终确认归档/
  05_内部制作执行/
    01_首帧与关键帧/
    02_视频片段/
    03_成片/
    04_封面/
```

Directory meaning:
- `01_客户原始资料/01_脚本`: client-provided original script files.
- `01_客户原始资料/02_产品素材`: client-provided product images, logo, brand assets, packaging/KV, font authorization, or official product references.
- `01_客户原始资料/03_用户反馈参考图`: user/client feedback reference images.
- `02_用户确认文件`: client-facing Excel confirmation workbooks and client-returned confirmation files.
- `03_设定资产/01_人物设定图`: character headshots, full-body images, group references.
- `03_设定资产/02_场景设定图`: scene reference images.
- `03_设定资产/03_产品参考图`: production-ready product reference images derived from or selected from official material.
- `03_设定资产/04_道具设定图`: props.
- `03_设定资产/05_特效关键帧`: effect reference frames.
- `04_最终确认归档`: final client-facing confirmation PDFs and their HTML sources.
- `05_内部制作执行`: internal execution workbooks and production outputs. Prompt workbooks live directly here, not inside a separate Prompt directory.
- `05_内部制作执行/01_首帧与关键帧`: first frames, middle keyframes, end frames, and QC-approved frame references.
- `05_内部制作执行/02_视频片段`: per-shot generated clips such as `镜头01_视频_v01.mp4`.
- `05_内部制作执行/03_成片`: finished or submitted full cuts such as `6月6日.mp4` or `项目名_成片_v01.mp4`.
- `05_内部制作执行/04_封面`: covers, title cards, thumbnails, and publishing cover images.

Hard folder rules:
- Do not create `03_执行版脚本`, `提示词参考`, `视频Prompt`, `粗剪样片`, `最终交付包`, `剪辑工程与导出配置`, or similar extra folders unless the user explicitly asks for that exact directory.
- Do not create a standalone `06_最终交付包` by default. Confirmed deliverables stay in `05_内部制作执行/03_成片` and `05_内部制作执行/04_封面` unless the user explicitly asks for a separate delivery package.
- If an existing project uses older or extra folders, do not delete them without explicit user confirmation. Instead, report which folders diverge from this standard and ask before cleanup.
- When creating or updating `00_项目说明_文件夹与命名规则.md`, include the fixed structure above and the rule that extra directories are not created unless explicitly requested.

## Phase Order Contract

Once this skill is activated for a project, preserve the current project phase and do not skip downstream checkpoints. If the user says `继续`, `下一步`, `上`, or gives a short continuation command, infer the next phase from existing project files and the mandatory order below.

Mandatory order:
1. Read the source script and create or update the script audit / client confirmation workbook.
2. Get or record the user's/client's decision on script handling, picture ratio, and asset direction.
3. Create the internal asset production workbook in `05_内部制作执行/`.
4. Call `镜头设计师` / `shot-designer` for asset prompts.
5. Wait for the user/producer to generate or provide finished asset images under `03_设定资产/`.
6. Backfill finished asset filenames/paths into the client confirmation workbook.
7. Call `土金PDF` / `tujinpdf` to generate the client-facing final confirmation archive. Keep both the styled HTML source and same-version PDF under `04_最终确认归档/`.
8. Only after the final confirmation archive exists, call `镜头设计师` / `shot-designer` for the internal per-shot execution and video prompt workbook.

Hard rules:
- Do not enter per-shot video prompt production before the final confirmation PDF archive exists.
- Do not create final confirmation PDFs with ReportLab, direct PDF drawing, or ad hoc PDF scripts when `土金PDF` is available.
- Do not expose internal Prompt content in client-facing workbooks or PDFs.
- Do not put internal execution next steps such as `进入内部执行脚本与Prompt表` in client-facing confirmation documents.
- Do not treat preview or generated assets as confirmed until their filenames/paths have been backfilled into the client confirmation workbook or final confirmation archive.
- If current files show a later phase was started out of order, stop that branch, restore the phase order, and tell the user which artifact must be produced first.

## Project Pilot Mode

When the user activates this skill for a project, act as the project pilot, not only as a file generator. The user should not have to guess what the next step is.

At the start of a project or when resuming:
1. Identify the current phase from the user's request and existing project files when available.
2. State the exact input needed from the user.
3. State what will be produced after that input.
4. State the `CHECKPOINT` before the next phase.
5. Do not proceed silently across checkpoints.

At the end of every phase, use the exact four-line status block from `Response Contract`.

If the user provides the requested input, process it and then ask for the next confirmation using concrete choices when possible.

If the user says `继续`, `下一步`, `上`, `韦斯安德森项目领航继续`, or equivalent:
- inspect existing project files if available;
- infer the current phase;
- tell the user the next required input or confirmation;
- do not generate downstream artifacts until the required confirmation exists.

Use this phase guide:

Phase 1 · 原始脚本接收
- Need from user: script file or pasted script.
- Output: project folder plus script/client confirmation workbook.
- Ask user to confirm: script handling permission, picture ratio, non-negotiable items, and missing official assets.
- Required ending: use the `Project start` minimal valid response example from `Response Contract`.

Phase 2 · 脚本与资产方向确认
- Need from user: whether the script is approved/default-approved, target ratio, and whether professional micro-adjustment is allowed.
- Output: updated confirmation workbook.
- Ask user to confirm: whether to create the internal asset production workbook.

Phase 3 · 设定资产制作表
- Need from user: confirmed script and asset direction.
- Output: internal asset production workbook.
- Ask user to confirm: generate or write asset prompts.

Phase 4 · 资产 Prompt
- Need from user: target style/reference if any; otherwise use the project style.
- Output: asset prompt workbook.
- Ask user to provide or generate asset images under `03_设定资产/`.

Phase 5 · 资产回填
- Need from user: finished asset images.
- Output: updated client confirmation workbook with actual filenames/paths.
- Ask user to confirm: assets are accepted for the final confirmation archive.

Phase 6 · 最终确认 PDF
- Need from user: confirmed script and finished assets.
- Output: `土金PDF` styled HTML plus same-version PDF archive.
- Ask user to confirm: whether to enter internal per-shot prompt production.
- Required ending when final confirmation archive is missing: use the `Skip-ahead request before final confirmation archive` minimal valid response example from `Response Contract`.

Phase 7 · 内部逐镜 Prompt
- Need from user: approved confirmation workbook, confirmed assets, and target tool if any.
- Output: internal execution script and prompt workbook.
- Ask user to confirm or generate: first frames, end frames, keyframes, and video clips.
- Required ending: always name `05_内部制作执行/内部执行脚本与Prompt表_vNN.xlsx` in `确认后我将进入` and list blocked video generation under `暂不执行的内容` unless the user has approved prompt generation and visual QC.

## Related Skills

This skill delegates specialized work to companion skills:

- Required for prompt production: `镜头设计师` / `shot-designer`. Asset prompt workbooks, internal per-shot prompt workbooks, final video prompt standards, and prompt validation live there.
- Required for formal final user-facing archive PDFs: `土金PDF` / `tujinpdf`.

If `镜头设计师` is not installed and the user asks for asset prompts, first/end/keyframe prompts, or per-shot video prompts, stop and tell the user to install `shot-designer` from the same `judeyang-skills` repository before continuing. Do not fall back to the old embedded prompt rules.

If `tujinpdf` is not installed and the user asks for a formal final archive PDF, stop and tell the user to install/use `tujinpdf`. Use a simpler legacy PDF fallback only if the user explicitly accepts a non-土金PDF fallback.

Required phase inputs:
- Script audit: client script file or pasted script content.
- Internal asset production branch: client confirmation workbook or parsed script shots; this is for the producer, not the client.
- Client asset confirmation: finished character, scene, product, prop, or effect images that should be inserted or referenced in the main client confirmation workbook.
- Final confirmation PDF: confirmed script, confirmed visual direction, and confirmed asset images.
- Internal prompt workbook: approved client confirmation workbook plus confirmed reference assets.

Required phase outputs:
- Client confirmation workbook: editable Excel workbook in `02_用户确认文件/`, usually `项目名_脚本与资产确认表_v01.xlsx`, with script audit, visual direction, asset confirmation, and user modification records in one workbook.
- Internal asset production workbook: editable Excel workbook in `05_内部制作执行/`, usually `设定资产制作表_v01.xlsx`; Python may build the workbook structure, but AI must write or revise the actual asset prompts.
- Confirmed assets: image assets under project-specific folders in `03_设定资产/`.
- Final archive: PDF under `04_最终确认归档/`.
- Internal execution: prompt workbook under `05_内部制作执行/`, plus first-frame/keyframe images under `05_内部制作执行/01_首帧与关键帧/`.

If the user asks for "all deliverables" but has not supplied confirmations, only produce the deliverables allowed by the current confirmed phase. Mark blocked downstream items as `待确认` or `待提供`; do not fabricate approval.

After completing any phase output, tell the user what was produced, what is still unconfirmed, and the next action. Do not wait for the user to ask "下一步是什么". Use direct wording such as:
`本阶段已完成：...；当前阻塞：...；下一步请确认/提供：...；确认后我将...`

## 🔴 CHECKPOINTS / STOP Conditions

Stop and ask for confirmation at these points:

1. Before treating the script as approved: require the user's/client's decision on script audit feedback, professional adjustment permission, non-negotiable requirements, and runtime expansion in the main client confirmation workbook.
2. Before submitting asset images to the client: require finished asset images to be placed under `03_设定资产/` and referenced back in `项目名_脚本与资产确认表_v01.xlsx`.
3. Before creating the final confirmation PDF: require confirmed script conclusions, confirmed asset directions, and final approved asset images.
4. Before writing the final internal prompt workbook: require the latest approved client confirmation workbook and confirmed reference assets.
5. Before changing `镜头设计师` 的 `references/prompt_standard.md` or prompt scripts: require explicit user approval that the supplied prompt reference should become the new standard.

If a checkpoint is missing, create or update only the relevant workbook and clearly state which confirmation is blocking the next phase. The internal asset production branch may create prompts for the producer before client approval, but it is not user-facing and must not be treated as final approval.

Before closing any phase, read `references/delivery_checklist.md` and apply the P0/P1 checks that match the current phase. A P0 issue blocks downstream work even if the user says `继续`.

## Core Workflow

### 1. Script Audit
Input: client script in Excel, Word, text, or pasted content.

Output: `脚本审核确认表.xlsx`.

Audit the script for:
- whether the client allows professional script adjustment
- required video aspect ratio and orientation: `9:16竖屏`, `16:9横屏`, `仅确认横屏，比例待定`, or `仅确认竖屏，比例待定`
- rigid client requirements and non-negotiable items
- story logic and forced plot progression
- shot duration vs dialogue length
- shot duration vs action/effects/product exposure
- product placement naturalness
- whether total runtime should increase
- AI video generation risks
- missing client assets: product images, logo, fonts, brand rules, music, voiceover

Write client-facing recommendations, not just problems. Include simple options and a `用户意见/选择` column.

Every client-facing script confirmation workbook must include a production-prep row asking the
client to confirm final picture ratio/orientation. Use clear choices:
`A 9:16竖屏；B 16:9横屏；C 仅确认横屏，比例待定；D 仅确认竖屏，比例待定。建议按投放平台选择A或B。`
This must appear before prompt generation, because framing, character blocking, product placement,
字幕安全区, and final exports all depend on it.

For detailed audit rules, read `references/audit_checklist.md`.

At the start of the audit, classify the project type and add the corresponding confirmation emphasis:
- product ads need official product material, Logo, screen text, feature claims, and product exposure rules
- AI short dramas need story logic, character/scene continuity, dialogue length, asset direction, and shot feasibility
- brand films need brand voice, visual tone, forbidden expressions, music/voice authorization, and delivery ratio
- knowledge/talking-head videos need factual basis, citation needs, subtitle strategy, pacing, and information hierarchy
- ecommerce videos need platform ratio, product handling, offer text, product close-ups, and subtitle-safe areas

Do not create a new folder or a separate workflow for these types. Use the fixed workbook and path contracts.

Client-facing workbooks must use polite human-review language. Do not mention internal automation, rule scanning, machine judgment, or "自动审核". Use wording such as `经逐镜审核`, `建议`, `暂未发现明显执行风险`, and `如贵方有补充要求`.

Audit tables must separate `序号` from `对应镜号/范围`. Do not put `制作前确认`, `整体`, and actual shot numbers in a single `镜号` column. Also deduplicate rows: the same `对应镜号/范围 + 问题类型` should appear only once.

Audit tables must cover every original shot. If a shot has no issue, include it with `问题类型=无意见` and leave the client feedback columns available. This proves the whole script was reviewed, not only the problematic shots.

### 1.5 Internal Asset Production Branch

Some projects need the client to see actual character, scene, prop, product, or effect images before approving the full script package. In that case, create an internal production workbook after script audit.

Output: `05_内部制作执行/设定资产制作表_v01.xlsx`.

This workbook is for the user/producer, not the client. It may include Prompt text because the producer uses it to make images. Do not put this file in `02_用户确认文件/` and do not present it as a client confirmation file.

The workbook should include:
- asset category: `人物`, `动物/坐骑`, `场景`, `产品/品牌`, `道具/法器`, `特效`, `字体/包装元素`
- asset name
- source shot range
- source script summary
- initial visual direction
- required client material, marked `待提供` when missing
- prompt type, such as `三视图Prompt`, `大头照Prompt`, `全身照Prompt`, `场景设定Prompt`, `道具设定Prompt`, or `特效关键帧Prompt`
- `完整Prompt`
- planned output filename
- finished asset path
- production status and notes

Python scripts may create the Excel structure, extract asset candidates, and leave prompt cells ready. The actual prompt text must be written or revised by AI after reading the script context and the user's reference style. The user may then:
- generate images manually using another tool
- ask Codex to generate images when the image-generation tool is available
- provide already-generated images for filing and confirmation

After assets are generated, move or save the actual images under `03_设定资产/`, then update `项目名_脚本与资产确认表_v01.xlsx` with the finished image filenames/paths and confirmation status. The client should see the actual images or image references, not the internal prompt workbook.

After completing this branch, tell the user:
`本阶段已完成内部设定资产制作表；下一步请按表生成人物/场景/道具图片，或让我按已确认的Prompt生成；图片完成后我会回填到脚本与资产确认表给用户确认。`

### 2. Client Confirmation Workbook As Source Of Truth

Do not create a separate `执行版脚本.xlsx` by default. If it is not directly shown to the client, it adds an extra file with little value. Keep the confirmed script changes, visual direction, and asset image references inside `项目名_脚本与资产确认表_v01.xlsx`.

Do not add `项目接收与处理记录`, `项目接收记录`, or `用户修改意见记录` sheets to the main client confirmation workbook. The main workbook should stay focused on script, visual direction, asset confirmation, and client choices.

If a script structure layer is needed for internal prompt writing, keep it as:
- a sheet inside the main client confirmation workbook, or
- the main sheet of `05_内部制作执行/内部执行脚本与Prompt表_v01.xlsx`

Only create a standalone `执行版脚本.xlsx` when the user explicitly needs a client-readable text-only script deliverable.

Before final prompt writing, use a platform-neutral three-layer storyboard/structure layer to lock the short drama's structure:
- `基础设定`: locked story world, recurring characters, props, scenes, product/brand constraints, continuity rules, and non-negotiable visual facts.
- `风格与质感`: genre, era, visual tone, color, lighting, texture, lens/camera feeling, realism boundary, and any style references that should guide the whole film.
- `逐镜画面内容`: one entry per shot with shot purpose, shot size, camera angle/movement, visible action, timing, dialogue/voiceover, sound notes, transition/handoff, and required assets.

This three-layer storyboard is a structural brief, not the final generation Prompt. Do not copy it mechanically into image/video prompt cells. The confirmed workbook and the storyboard only provide structure, continuity, and source facts; the final `首帧Prompt`, optional keyframe prompts, `生成前执行说明`, and `视频内容Prompt（含声音/负面）` must still be written shot by shot by the AI after reading the full approved confirmation workbook, confirmed assets, and continuity notes.

When the client has many revisions, create a user-facing workbook or sheet named `项目执行过程与修改确认归档`. This is a client-facing execution archive, not a billing/workload document. It should politely record:
- initial material receipt time: when the client script/material was first received by the producer, with the exact date and time when available
- received material name and source type, such as original script, product assets, brand references, visual references, font authorization, voice/music references
- date or round of feedback
- client request / revision instruction
- original script / pre-confirmation content
- user-confirmed / post-revision execution content
- affected shots or assets
- what was changed
- adjustment impact: script update, prompt update, asset adjustment, video update, retouching, sound/subtitle adjustment, review/export
- status and notes

Keep the tone factual and service-oriented. Do not complain or accuse the client. The purpose is to let both sides review what was requested, what was confirmed, and what was delivered.

When the user submits client modification feedback during any phase, record it immediately before continuing downstream work. Always use a separate workbook named `用户修改意见记录_vNN.xlsx` under `02_用户确认文件/`. Do not put this record as a worksheet inside `项目名_脚本与资产确认表_vNN.xlsx`.

Use this submission template when asking the user to provide or normalize client feedback:

```text
【最简必填版】
反馈时间：
客户反馈编号：#1 / #2 / #3
客户原话：
影响范围：镜头 / 人物 / 场景 / 道具 / 配音 / 字幕 / 成片
需要重做多少秒：
是否已有样片/成片受影响：是 / 否 / 不确定
下一步处理：

【详细版】
反馈时间：
反馈来源：微信 / 飞书 / 邮件 / 电话 / 会议 / 文件批注 / 其他
关联文件：
关联镜头/资产：
客户原话：
要求类型：脚本修改 / 人物设定 / 场景设定 / 产品素材 / 道具特效 / 配音音乐 / 字幕包装 / 成片节奏 / 其他
是否发生在已确认之后：是 / 否 / 不确定
是否已有样片或图片受影响：是 / 否 / 不确定
需要修改的内容：
不能修改的内容：
客户提供的新素材：
期望完成时间：
我的处理建议/备注：
```

After recording feedback, tell the user which whitelist paths are affected and the next action. Do not name invented folders. Example:
`已记录本轮修改意见到 02_用户确认文件/用户修改意见记录_vNN.xlsx；本轮影响 02_用户确认文件/项目名_脚本与资产确认表_vNN.xlsx、03_设定资产/01_人物设定图/、05_内部制作执行/设定资产制作表_vNN.xlsx；暂不生成新图，等你确认。`

For common client feedback:
- `第3镜人物衣服要换` affects `02_用户确认文件/用户修改意见记录_vNN.xlsx`, `02_用户确认文件/项目名_脚本与资产确认表_vNN.xlsx`, `03_设定资产/01_人物设定图/`, and any existing `05_内部制作执行/设定资产制作表_vNN.xlsx`.
- `第8镜产品出现太突兀` affects `02_用户确认文件/用户修改意见记录_vNN.xlsx`, `02_用户确认文件/项目名_脚本与资产确认表_vNN.xlsx`, `01_客户原始资料/02_产品素材/`, `03_设定资产/03_产品参考图/`, and any existing `05_内部制作执行/内部执行脚本与Prompt表_vNN.xlsx`.
- New client reference images belong in `01_客户原始资料/03_用户反馈参考图/`, then their filenames/paths should be referenced from `02_用户确认文件/用户修改意见记录_vNN.xlsx`.

Do not merge multiple feedback rounds into one vague note. Keep each round as a separate row with timestamp, source, affected shots/assets, original client wording, required action, status, and next file to update.

Do not create a project receipt or processing-record sheet by default. If the user explicitly asks for a project timeline, closeout archive, or execution summary, derive the needed dates and source names from the available files and user-provided context at that later phase. Use neutral names such as `项目执行过程与修改确认归档` or `项目执行总结归档`; avoid naming user-facing files with `工作量说明`.

For `项目执行过程与修改确认归档`, include a full script comparison sheet when possible. The sheet should list every original shot from the client script in order, not only changed items. For each shot, keep the original script fields, then add user revision instruction, user-confirmed/post-revision execution result, adjustment impact, status, and notes. Unchanged shots should explicitly say no added revision and that the original/confirmed execution is retained.

Do not use internal commercial wording in the user-facing archive, including `核算`, `结算`, `报价`, `合同`, `工作量`, `增量`, `重要边界`, or similar phrasing. Use neutral wording such as `调整影响说明`, `便于双方回顾确认`, `项目复盘`, and `修改确认归档`.

If an internal record is needed for costing or settlement, create a separate internal-only workbook named `项目修改记录与工作量说明_内部版`. Never mix the internal workload/costing language into the user-facing archive.

When a client requests changes after a preview/sample clip has already been generated, track the affected duration clearly:
- Internal record wording may use `用户变更导致废弃秒数`, `可计入结算的返工秒数`, and `计费依据`.
- User-facing archive wording should stay neutral: use `已生成内容受影响时长`, `需重新制作时长`, `确认后调整`, `调整依据`, and `修改结果`. Avoid words like `浪费`, `要钱`, `废弃`, `用户行为导致`, or accusatory phrasing in user-facing documents.
- Every record should include: date/time, sample version, sample duration, client feedback original text, affected shots/assets, whether the change happened after confirmation, affected duration in seconds, calculation basis, needed rework action, and status.
- If a 5-second sample is invalidated by a client-requested visual change such as changing a confirmed character costume color, record `样片时长=5s`, `受影响时长=5s`, and explain that the existing sample cannot be reused because the character visual reference changed.
- The final user-facing project archive can include a summary of `确认后调整记录` and `已生成内容受影响时长合计`; the internal workbook can separately calculate billing seconds and settlement notes.

After final delivery is submitted, create a user-facing PDF archive from the latest internal revision workbook when there were multiple revision rounds or affected-duration records. This is the closeout step after video production is done, not another prompt/video-generation step.
- Source: the latest internal revision workbook such as `项目修改记录与受影响时长_内部版_vNN.xlsx`, plus the project receipt/execution record.
- Output: an HTML source and PDF under `04_最终确认归档/` named `项目名_项目执行总结与调整影响说明_vNN.html` and `项目名_项目执行总结与调整影响说明_vNN.pdf`.
- Treat `最终总结报告`, `项目总结`, `项目复盘`, `closeout`, and `项目执行总结` as the same closeout artifact. Do not create a second PDF for any of these names.
- The canonical external title and filename phrase is always `项目执行总结与调整影响说明`. Do not name user-facing closeout files `最终总结报告`, `最终总结报告_土金PDF`, `项目最终总结`, or similar variants.
- If the user asks for `最终总结报告`, generate/update `项目名_项目执行总结与调整影响说明_vNN.html/pdf` instead, and briefly state that this is the fixed final-summary format.
- Use the `tujinpdf` skill for the final user-facing `项目执行总结与调整影响说明` PDF unless the user specifies another style. Generate and keep both the styled HTML source and the PDF, so later revisions can update the existing HTML instead of recreating the layout from scratch.
- Use the established closeout layout from `卡萨帝红楼梦AI短剧_项目执行总结与调整影响说明_v01.pdf` as the default. The report should look like a concise closeout memo, not a new general project report.
- Default closeout structure is two A4 pages:
  - Page 1: brand/project header, title `项目执行总结与调整影响说明`, one summary band with generated duration total / summary口径 / final submitted file and runtime, then `项目关键节点`, then the first part of `受影响内容明细`.
  - Page 2: continue `受影响内容明细` if needed, then `调整影响汇总`, `最终交付文件`, and a short neutral confirmation note.
- Only add a third page when the detail table is genuinely too long to remain readable. Do not expand a short/medium closeout into a 5-page magazine report.
- Include: project timeline, final submitted file, confirmed adjustment rounds, affected shots/assets, user-visible reasons, `需重新制作时长`, and `已生成内容受影响时长合计`.
- Include the final submitted video's actual runtime when the file is available, such as `最终成片文件：6月6日.mp4；最终成片时长：约74.2秒`. Keep this separate from affected-duration totals; do not imply that final runtime and affected duration use the same calculation basis.
- Keep the closeout PDF simple and evidence-based. The user should immediately understand what the total affected duration consists of, why each item changed, what changed, and what result was delivered. Avoid overbuilding extra archive sections, cover-image pages, dashboards, decorative cards, or generic "final summary report" layouts.
- For user-facing affected-content detail tables, include the feedback time so the client can see which round each affected item came from. Recommended column order: `反馈时间`, `镜头/内容`, `时长`, `修改原因`, `修改内容`, `修改结果`.
- Use the most precise feedback timestamp available from the project receipt/execution record or revision workbook. If the exact time exists, write `YYYY-MM-DD HH:MM`; if only the date exists, write `YYYY-MM-DD`. If a shot has a later supplementary instruction, keep the original feedback time and add a concise note such as `补充：20:13`.
- Sort affected-content detail rows by feedback time first, then by the user's submitted order within the same feedback round. Do not sort primarily by shot number. This makes it clear when a later feedback round changed content that had already been generated or previously adjusted, and why the item belongs in the affected/rework summary.
- For user-facing detail tables, use formal column names: `修改原因`, `修改内容`, and `修改结果`. Do not use colloquial headings such as `为什么改`, `改的内容`, or `处理结果`.
- When dialogue or voiceover text changes after a shot has been generated, the `修改结果` must explain the lip-sync reason in client-facing language. Example: `因台词调整后原画面口型与新配音不匹配，不能仅替换音频，需重新制作对应镜头，并同步更新配音与字幕。` This should be recorded as a shot/video remake reason, not just as a subtitle or dubbing update.
- Clearly distinguish user-visible categories: (a) adjustments requested after confirmation or after generated content existed; (b) content that differs from the originally confirmed script/execution content; (c) post-production-only changes such as subtitles, voice correction, BGM, rhythm, or title/cover packaging.
- Filter out: internal settlement notes, billing/costing language, tool names, local paths, prompt-engineering details, duplicate provisional estimates, blame language, and any wording such as `浪费`, `要钱`, `废弃`, `用户行为导致`, `计费`, `结算`, or `工作量`.
- If later rows refine an earlier provisional estimate, use the latest confirmed per-shot timing as the source of truth and avoid double-counting duplicate confirmations.

Do not assume the confirmed workbook is automatically production-ready. Before prompt generation, run a second AI review against the same standards: duration, dialogue, story continuity, product logic, asset needs, and AI generation feasibility. Keep the review internal unless the user asks for a client-facing summary, but still correct or flag obvious mistakes before prompt generation.

### 3. Asset Extraction And Client Asset Confirmation
Extract all production assets from the script before generating visuals.

Always classify assets into:
- characters
- animals/mounts
- scenes
- products/brand elements
- props/magic objects
- visual effects
- typography/package elements

Output should stay inside `项目名_脚本与资产确认表_v01.xlsx`, usually as `形象场景描述确认表`, `设定资产确认表`, or equivalent sheets. Do not create a separate `形象场景描述确认表.xlsx` unless the user explicitly asks.

This can start as text direction, but if the client wants to see actual characters, scenes, or props, use the internal `设定资产制作表_v01.xlsx` to make images first. After the images are ready, update the main client confirmation workbook with actual image filenames/paths and confirmation questions. The client should approve the asset images, not the internal prompt table.

### 4. Asset Generation
Asset images can be generated by the user manually, by another production tool, or by Codex when the image-generation tool is available and the user asks for it.

Only generate or file assets when the current stage allows it:
- If the goal is client discussion, generate preview assets and mark them as `预览/待确认`.
- If the script and asset direction are confirmed, generate production reference assets and mark them as `已确认候选` until the user/client approves them.
- If official product assets are missing, do not generate final product-accurate visuals; mark product rows as `待提供`.

Typical generated assets:
- character video-reference assets: default to one clean no-text face close-up/headshot plus one clean no-text full-body image for each recurring character
- optional character expression/action references when a shot needs performance continuity
- scene concept images
- product/magic-object reference images
- key effect frames when needed

Do not make character three-view sheets the default main video reference for AI video production. Three-view sheets are useful as visual-confirmation, costume, silhouette, and internal modeling archives, but final Seedance/LibTV character video references should still prefer the clean no-text face close-up/headshot plus the clean no-text full-body image. Do not use three-view sheets, multi-view contact sheets, or labeled layout pages directly as Seedance/LibTV video references, because the model may read multiple views as multiple subjects and reduce character consistency.

The client confirms asset images through `项目名_脚本与资产确认表_v01.xlsx` or the final confirmation PDF. Storyboards do not need client confirmation unless the user explicitly says otherwise.

For asset-generation prompt workbooks, keep each asset's positive requirements and negative requirements in one `完整Prompt` cell. Do not split them into separate `正向Prompt` and `负面Prompt` columns unless the user explicitly asks for separate columns.

When creating a character/scene setting prompt workbook, every recurring character must include three distinct character prompt entries:
- `三视图Prompt`: front/side/back costume and silhouette archive for visual confirmation and internal modeling reference.
- `大头照Prompt`: clean no-text face close-up/headshot for facial identity, age, expression baseline, hair, makeup, and temperament.
- `全身照Prompt`: clean no-text full-body reference for costume, body proportion, silhouette, footwear, and carried props.

Do not collapse these three character outputs into one generic `人物设定Prompt`. The workbook may use either three rows per character or three separate columns, but the output filename and purpose must be explicit for each prompt. Scene setting prompts remain separate entries, such as `场景设定Prompt`, and should describe space, geography, lighting, texture, era, weather, and reusable background anchors.

Asset image prompts should borrow the approved reference prompt style: structured sections, rich visual detail, and clear constraints. For still images, use sections such as `【核心主题】`, `【基础设定】`, `【画面构图】`, `【氛围与画质】`, `【细节要求】`, `【负面要求】`, and `【输出要求】`. Time-coded second-by-second blocks are only required for video/action prompts, not static character or scene sheets.

Asset prompt tables must keep explanatory text in Excel cells, not inside generated images. Do not ask the image model to add labels such as role names, `正面/侧面/背面`, arrows, callouts, titles, note text, page borders, or layout annotations. Character headshot/full-body assets and any optional three-view archive sheets must be clean image-only references with no generated text labels. If a client-confirmation contact sheet needs captions, add them later in Excel/PDF layout, not in the source image prompt.

Before using any reference image for image or video generation, check whether it contains labels, notes, title text, subtitles, watermarks, UI panels, or layout borders. Current production reference images should be clean image-only assets whenever possible. If a confirmed setting sheet contains explanatory text, create or request a clean `无文字` generation-reference version and prefer that file in prompts.

For all generated character, scene, first-frame, middle-keyframe, end-frame, and video prompts, add a no-text rule:
`画面为无文字纯图片。禁止生成字幕、标题、角标、水印、说明文字、乱码、伪Logo、排版边框和UI界面。`

Product shots are the exception: official product logos or official screen text already present in client-provided product assets may be retained only when the shot requires it. In that case, write:
`仅保留官方产品素材中已有的品牌Logo和官方屏显信息，Logo位置、比例和拼写必须与官方素材一致。禁止新增任何文字、伪Logo或屏幕文案。`

If product screen text is difficult to generate accurately, generate a clean product image first and add exact text in post-production.

### 5. Final Confirmation PDF
After script and assets are confirmed, generate a PDF archive containing:
- script confirmation conclusions
- visual direction confirmation conclusions
- actual confirmed asset images
- material list
- sign-off area

Do not include process-heavy option tables in the final PDF.

When generating a `脚本与设定资产最终确认归档` document, use the `tujinpdf` skill by default unless the user explicitly requests another style. The deliverable should be a 土金色系 A4 magazine-style confirmation archive with:
- a styled HTML source file kept next to the PDF for later revisions
- a same-name PDF rendered from that HTML
- confirmed script conclusions and visual-direction conclusions
- actual confirmed asset images preserved in the document
- natural pagination based on content length, without forcing a fixed page count
- table headers centered, body short cells centered, and body long cells left-aligned

Treat the final confirmation PDF as a client-facing artifact. Do not expose internal production
methods, tool names, Prompt tables, internal statistics, settlement logic, folder operations, or
version-handling details. Use neutral wording that states the confirmed direction and the next
client-relevant production basis.

Before delivering a client-facing PDF:
1. Read `references/client_facing_doc_standard.md`.
2. Use `tujinpdf` to create a styled HTML source and render the same-name PDF. Do not use ReportLab or direct PDF drawing for normal final confirmation archives.
3. Run `scripts/validate_client_facing_text.py` against the generated text manifest or extracted visible text.
4. Do not deliver the PDF if the validator reports blocked wording or stale material status.

### 6. Internal Prompt And Shot Design

Prompt generation is owned by the `镜头设计师` skill. Do not duplicate detailed prompt-writing rules inside this skill.

The project lead may pass project type, confirmed style, target platform, ratio, and asset status to `镜头设计师`, but must not alter the `视频内容Prompt（含声音/负面）` top-level structure. If a new shot taxonomy or validation rule is needed, update `镜头设计师` documentation/scripts with explicit approval instead of adding ad hoc prompt fields here.

When the project reaches asset prompt writing or per-shot video prompt writing, call `镜头设计师` with:
- approved `项目名_脚本与资产确认表_v01.xlsx`
- project directory
- confirmed asset directory `03_设定资产/`
- target ratio, such as `9:16竖屏` or `16:9横屏`
- target tool, such as Seedance, LibTV, or generic image/video generation
- user-approved prompt reference style, if any
- task type: `设定资产Prompt` or `逐镜视频Prompt`

Expected handoff outputs from `镜头设计师`:
- `05_内部制作执行/内部执行脚本与Prompt表_v01.xlsx`
- `首帧Prompt`, optional `中间关键帧Prompt`, optional `结尾帧Prompt`
- `生成前执行说明`
- `视频内容Prompt（含声音/负面）`
- keyframe skip/reuse decisions
- validation result from `validate_prompt_detail.py`

Boundary rules kept by 韦斯安德森项目领航:
- client-facing workbooks must not expose internal prompt engineering
- the main client confirmation workbook remains the source of truth for approved script and assets
- if `镜头设计师` reports missing confirmations, update the client confirmation workbook before continuing
- if middle keyframes are too similar, prefer first/end frames or skip the middle keyframe
- do not connect keyframes or run video generation until prompt validation and visual QC pass

After `镜头设计师` finishes, report:
`本阶段已完成：内部逐镜Prompt表；当前阻塞：...；下一步请确认/生成：...`

## Project Folder Standard

Use the fixed project folder contract. Do not create project-specific folder layouts unless the user explicitly asks for exact additional directories.

Keep first-level folders stable:

```text
项目文件夹/
  00_项目说明_文件夹与命名规则.md
  01_客户原始资料/
    01_脚本/
    02_产品素材/
    03_用户反馈参考图/
  02_用户确认文件/
  03_设定资产/
    01_人物设定图/
    02_场景设定图/
    03_产品参考图/
    04_道具设定图/
    05_特效关键帧/
  04_最终确认归档/
  05_内部制作执行/
    01_首帧与关键帧/
    02_视频片段/
    03_成片/
    04_封面/
```

Do not create a separate first-level `03_执行版脚本/` directory. If a confirmed text execution script is needed, keep it in `02_用户确认文件/` when it is user-facing, or keep the execution layer inside the internal workbook in `05_内部制作执行/`.

Do not create extra placeholder folders outside the fixed structure. If brand assets or font authorization files exist, store them under `01_客户原始资料/02_产品素材/` unless the user explicitly asks for separate folders.

Do not create a generic `提示词参考` folder in the project structure. If a user provides a prompt reference file, use it to update the skill or prompt standard when appropriate, then archive the source only if the user explicitly wants to keep it.

Do not hardcode project-specific names such as `产品与法器设定` in the generic template. Product source materials belong under `01_客户原始资料/02_产品素材`; production-ready product references belong under `03_设定资产/03_产品参考图`.

Use `scripts/create_project.py` to scaffold the stable structure and create the initial confirmation workbook. Only pass `--asset-subfolders` when the user explicitly asks for extra asset folders beyond the standard contract.

Example:

```bash
python scripts/create_project.py \
  --project-name "海尔空调西游记AI短剧" \
  --base-dir "$HOME/Desktop"
```

## Automation Scripts

Use these scripts when possible instead of rebuilding the same Excel structure by hand.

### Create Project

```bash
python scripts/create_project.py \
  --project-name "项目名" \
  --base-dir "$HOME/Desktop"
```

Creates the fixed project folder structure, an initial `项目名_脚本与资产确认表_v01.xlsx`, and a separate `用户修改意见记录_v01.xlsx`. Do not generate a separate naming-example document; naming rules live in `00_项目说明_文件夹与命名规则.md`.

### Audit Script Workbook

```bash
python scripts/audit_script.py \
  --input "/path/to/client_script.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Creates `脚本审核确认表_v01.xlsx` with:
- production-prep confirmation rows
- shot-level duration/dialogue/AI-risk issues
- initial asset extraction sheet

### Build Internal Asset Production Table

```bash
python ../shot-designer/scripts/build_asset_prompt_table.py \
  --input "/path/to/脚本审核确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Creates `05_内部制作执行/设定资产制作表_v01.xlsx` from the asset-direction sheet inside the client confirmation workbook. The script creates the workbook structure and asset rows only. The AI must then fill or revise the actual `完整Prompt` cells based on the script, confirmed direction, and approved prompt style.

Use this right after script audit when the user wants to make actual character, scene, prop, product, or effect images before submitting the final client confirmation workbook. This workbook is internal; after images are made, write the finished image filenames/paths back into `项目名_脚本与资产确认表_v01.xlsx`.

### Build Internal Prompt Table

```bash
python ../shot-designer/scripts/build_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Creates `内部执行脚本与Prompt表_v01.xlsx`: one worksheet, one row per shot, with source script fields and extracted reference assets. Prompt-related cells are intentionally blank for the AI director pass.

### Legacy Client Confirmation PDF Fallback

```bash
python scripts/build_client_confirmation_pdf.py \
  --project-dir "/path/to/项目交付文件夹" \
  --project-name "项目名" \
  --output "/path/to/04_最终确认归档/项目名_脚本与设定资产最终确认归档_v01.pdf" \
  --allow-legacy-reportlab
```

Legacy fallback only. Use it only when `tujinpdf` is unavailable and the user explicitly accepts a simpler non-土金PDF archive. Normal final confirmation and closeout PDFs must use `tujinpdf` HTML + browser rendering.

### Delivery Checklist

Before reporting a phase as complete, check:

```bash
sed -n '1,220p' references/delivery_checklist.md
```

Apply the matching P0/P1 items. Do not claim completion when the current phase output is missing, has the wrong version, is in the wrong folder, or exposes internal production language to the client.

## Failure Modes And Recovery

Use these branches instead of guessing or silently continuing.

- If the client script has no recognizable shot table, then create a `资料解析问题确认表.xlsx` or a sheet in the audit workbook that lists the missing columns, the source filename, and the exact fields needed: `镜号`, `景别`, `画面内容`, `时长`, `台词/旁白`, `音效/音乐`, `备注`.
- If the script is pasted text rather than a spreadsheet, then first convert it into a shot table with stable shot numbers, preserve the original pasted text in an archive/source sheet, and mark uncertain segmentation as `待确认`.
- If shot duration is missing, then keep the shot, mark `时长=待确认`, and flag duration-sensitive risks instead of inventing seconds.
- If dialogue is too long for the stated duration, then write a client-facing choice: shorten dialogue, extend duration, or move content to voiceover. Do not silently rewrite approved dialogue.
- If official product images, logo, font authorization, brand rules, music, or voiceover references are missing, then mark each item as `待提供` in client-facing sheets and block final product-accurate prompts until provided.
- If the user asks to generate product visuals without official product references, then create placeholder direction only and state that official assets override all generated imagery.
- If the client confirmation workbook has not passed the second AI review, then fix or flag duration, dialogue, continuity, product logic, asset needs, and generation feasibility before prompt generation.
- If an approved prompt reference conflicts with `镜头设计师/references/prompt_standard.md`, then ask whether to固化 the reference. If approved, update both `镜头设计师/references/prompt_standard.md` and the relevant prompt-building script; otherwise apply it only to the current workbook.
- If a client changes a confirmed visual after preview/sample generation, then record sample version, affected shots/assets, affected duration, reason, rework action, and status before updating downstream prompts or assets.
- If a generated workbook cannot be validated manually, then open it with a spreadsheet library, verify worksheet names, first-row headers, required columns, file path, and row count before telling the user it is complete.

## Naming Rules

Use versioned filenames. Do not overwrite old versions.

Examples:
- `项目名_脚本与资产确认表_v01.xlsx`
- `设定资产制作表_v01.xlsx`
- `角色_孙悟空_三视图_无文字_v01.png`
- `角色_孙悟空_大头照_无文字_v01.png`
- `角色_孙悟空_全身照_无文字_v01.png`
- `场景_黄风岭_设定图_v01.png`
- `产品_海尔洗空气空调_官方参考_v01.png`
- `项目名_脚本与设定资产最终确认归档_v01.pdf`
- `项目名_项目执行总结与调整影响说明_v01.pdf`
- `内部执行脚本与Prompt表_v01.xlsx`
- `封面_项目名_主题_v01.png`

## Client vs Internal Language

Use client-neutral names in deliverables:
- `脚本审核确认表`
- `脚本与资产确认表`
- `设定资产确认表`
- `客户最终确认PDF`

Reserve stronger internal language for internal notes only:
- `导演判断`
- `镜头执行风险`
- `设定资产制作表`
- `Prompt执行表`
- `制作状态`

## Anti-Patterns / Blacklist

Do not do these:

- Do not skip client confirmation checkpoints to produce downstream files faster.
- Do not end active project-pilot responses with `阶段/输入/产物/检查点` or `状态/下一步/归档/文件`; use the exact four-line `Response Contract` block.
- Do not treat preview character, scene, product, prop, or effect images as approved production assets before they are referenced back in the client confirmation workbook and confirmed.
- Do not ask the client to confirm storyboards unless explicitly required.
- Do not use AI-generated product appearance as final brand reference; official product assets override prompts.
- Do not put internal image/video prompts in client-facing sheets; prompts belong in `设定资产制作表` or `内部执行脚本与Prompt表`.
- Do not create a separate `02_视频Prompt` folder; the prompt workbook belongs directly under `05_内部制作执行/`.
- Do not create a separate top-level `03_执行版脚本/` folder or standalone `执行版脚本.xlsx` unless explicitly requested.
- Do not invent downstream folders such as `01_脚本分镜`, `03_角色设定`, `04_画面提示词`, `05_生成素材`, `06_视频工程`, or `客户反馈`; map every affected item to the `Path Contract` whitelist.
- Do not move `03_设定资产` under `05_内部制作执行`; use a lightweight reference entry when execution needs access.
- Do not create nested current-version folders such as `第一版启用` for active assets; keep current assets flat and move old versions to `90_历史版本/`.
- Do not mix internal costing, settlement, workload, or billing wording into user-facing archives.
- Do not write accusatory client-facing wording such as `浪费`, `要钱`, `废弃`, or `用户行为导致`.
- Do not overwrite old versions; create a new `_vNN` filename.
- Do not claim a workbook or PDF is complete without checking that required sheets, columns, and source references are present.

## Hard Rules

- Before PDF, keep documents editable in Excel.
- In client confirmation Excel files, keep `脚本审核确认表` and `形象场景描述确认表` as the first two worksheet tabs.
- In client-facing Excel files, center short structured fields and left-align long descriptive text fields.
- Do not ask the client to confirm storyboards unless explicitly required.
- Preview character/scene images may be generated for confirmation, but they must be marked `预览/待确认` until approved.
- Do not use AI-generated product appearance as final brand reference; official product assets override prompts.
- Always keep original script content visible somewhere in execution deliverables for comparison.
- For every final prompt, state required reference assets and non-negotiable constraints.
