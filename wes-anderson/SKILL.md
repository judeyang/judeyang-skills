---
name: 韦斯安德森
description: Use when the user wants to turn an AI short video script into a practical production workflow: script audit, client confirmation workbook, internal asset production workbook, asset/character/scene extraction, final confirmation PDF, user revision tracking, and internal per-shot image/video prompt tables. Triggers on AI short drama, short video script review, storyboard/video prompt generation, character setting references, face close-up/full-body assets, scene assets, client confirmation workflow, user modification tracking, or Chinese phrases like AI短剧、脚本审核、脚本与资产确认表、设定资产制作表、分镜提示词、人物设定图、大头照、全身照、三视图、场景设定图、用户修改意见.
---

# 韦斯安德森

Recommended human-facing name: **韦斯安德森**.

Use this skill to convert a client script into a confirmed, executable AI video production package.

Regression resources:
- `examples/`: sample script and expected workbook structure.
- `test-prompts.json`: Darwin/人工评估 prompts for client audit, internal asset production, and client revision tracking.
- `scripts/validate_workbook_structure.py`: validates client, internal-asset, and internal-prompt workbook structure before delivery.

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
5. Before changing `references/prompt_standard.md` or any script under `scripts/`: require explicit user approval that the supplied prompt reference should become the new standard.

If a checkpoint is missing, create or update only the relevant workbook and clearly state which confirmation is blocking the next phase. The internal asset production branch may create prompts for the producer before client approval, but it is not user-facing and must not be treated as final approval.

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

Do not create a separate `执行版脚本.xlsx` by default. If it is not directly shown to the client, it adds an extra file with little value. Keep the confirmed script changes, visual direction, asset image references, and user modification records inside `项目名_脚本与资产确认表_v01.xlsx`.

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

When the user submits client modification feedback during any phase, record it immediately before continuing downstream work. Prefer a worksheet named `用户修改意见记录` in the current confirmation workbook, or a separate workbook named `用户修改意见记录_vNN.xlsx` under `02_用户确认文件/` when the feedback spans multiple files.

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

After recording feedback, tell the user which downstream files are affected and the next action. Example:
`已记录本轮修改意见，影响镜头03-05和角色服装设定，预计需重新制作8秒；下一步我会更新项目名_脚本与资产确认表_v01.xlsx和内部设定资产制作表，暂不生成新图，等你确认。`

Do not merge multiple feedback rounds into one vague note. Keep each round as a separate row with timestamp, source, affected shots/assets, original client wording, required action, status, and next file to update.

At the start of each new project, create or update a simple project receipt/execution record. At minimum, record:
- `资料接收时间`
- `资料名称`
- `资料类型`
- `来源路径/来源说明`
- `处理动作`
- `当前状态`

The final user-facing archive should reuse this record so the client can see when the original script was received and what was done at each stage. Use neutral names such as `项目执行过程与修改确认归档` or `项目执行总结归档`; avoid naming user-facing files with `工作量说明`.

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
- Output: a PDF under `04_最终确认归档/` named with neutral wording such as `项目执行总结与调整影响说明_用户版_v01.pdf`.
- Use the `tujinpdf` skill for the final user-facing `项目执行总结与调整影响说明` PDF unless the user specifies another style. Generate and keep both the styled HTML source and the PDF, so later revisions can update the existing HTML instead of recreating the layout from scratch.
- Do not force the report into a fixed two-page length. Use as many A4 pages as the content needs. Prefer readability, correct table alignment, and comfortable spacing over compressing the document to fewer pages. Short summaries can be 1-2 pages; medium reports can be 3-5 pages; longer tables should paginate naturally.
- Include: project timeline, final submitted file, confirmed adjustment rounds, affected shots/assets, user-visible reasons, `需重新制作时长`, and `已生成内容受影响时长合计`.
- Include the final submitted video's actual runtime when the file is available, such as `最终成片文件：6月6日.mp4；最终成片时长：约74.2秒`. Keep this separate from affected-duration totals; do not imply that final runtime and affected duration use the same calculation basis.
- Keep the closeout PDF simple and evidence-based. The user should immediately understand what the total affected duration consists of, why each item changed, what changed, and what result was delivered. Avoid overbuilding extra archive sections when a two-page summary is enough.
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
2. Build the PDF with `scripts/build_client_confirmation_pdf.py` when the project matches the
   standard confirmation archive structure.
3. Run `scripts/validate_client_facing_text.py` against the generated PDF text manifest.
4. Do not deliver the PDF if the validator reports blocked wording or stale material status.

### 6. Internal Execution Workbook With Prompts

Output: `05_内部制作执行/内部执行脚本与Prompt表_v01.xlsx`.

This workbook is for production execution after client confirmation. It must preserve source script facts, confirmed revisions, reference asset paths, first-frame/keyframe planning, and video prompts in one auditable table.

Before writing, validating, or delivering this workbook, read `references/prompt-workbook-rules.md`. That file is the source of truth for prompt columns, keyframe rules, QC, filename conventions, and anti-hallucination constraints.

## Project Folder Standard

Keep first-level project folders stable, create optional folders only when the project actually needs them, and derive asset subfolders from the script instead of hardcoding project-specific categories.

Before scaffolding a project folder, read `references/project-folder-standard.md`.

## Automation Scripts

Use these scripts when possible instead of rebuilding the same Excel structure by hand.

### Create Project

```bash
python scripts/create_project.py \
  --project-name "项目名" \
  --base-dir "/path/to/output-root" \
  --asset-subfolders "人物设定图,场景设定图,道具设定图,特效关键帧"
```

Creates the project folder structure and an initial `项目名_脚本与资产确认表_v01.xlsx`. Omit `--asset-subfolders` when the script has not been reviewed yet; add or create asset subfolders after asset extraction. Do not generate a separate naming-example document; naming rules live in `00_项目说明_文件夹与命名规则.md`.

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
python scripts/build_asset_prompt_table.py \
  --input "/path/to/脚本审核确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Creates `05_内部制作执行/设定资产制作表_v01.xlsx` from the asset-direction sheet inside the client confirmation workbook. The script creates the workbook structure and asset rows only. The AI must then fill or revise the actual `完整Prompt` cells based on the script, confirmed direction, and approved prompt style.

Use this right after script audit when the user wants to make actual character, scene, prop, product, or effect images before submitting the final client confirmation workbook. This workbook is internal; after images are made, write the finished image filenames/paths back into `项目名_脚本与资产确认表_v01.xlsx`.

### Build Internal Prompt Table

```bash
python scripts/build_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Creates `内部执行脚本与Prompt表_v01.xlsx`: one worksheet, one row per shot, with source script fields and extracted reference assets. Prompt-related cells are intentionally blank for the AI director pass.

### Validate Workbook Structure

```bash
python scripts/validate_workbook_structure.py \
  "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --type client
```

Use `--type internal-asset` for `设定资产制作表_v01.xlsx` and `--type internal-prompt` for `内部执行脚本与Prompt表_v01.xlsx`.

### Build Client Confirmation PDF

```bash
python scripts/build_client_confirmation_pdf.py \
  --project-dir "/path/to/项目交付文件夹" \
  --project-name "项目名" \
  --output "/path/to/04_最终确认归档/项目名_脚本与设定资产最终确认归档_v01.pdf"
```

Creates a client-facing PDF and a sibling `.manifest.txt` file. The generator validates the
manifest before rendering. Run `scripts/validate_client_facing_text.py` again before delivery.

## Failure Modes And Recovery

When source material is incomplete, client confirmation is missing, official product assets are absent, prompt standards conflict, or generated workbooks cannot be validated, follow the explicit recovery branches in `references/failure-recovery.md`.

Do not guess, silently continue, or treat unconfirmed downstream deliverables as approved.

## Delivery Rules Reference

For detailed filename examples, client-facing language rules, anti-patterns, and hard delivery rules, read `references/delivery-rules.md` before creating final workbooks, PDFs, or production assets.
