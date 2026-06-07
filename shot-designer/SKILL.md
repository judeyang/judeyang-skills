---
name: 镜头设计师
description: Use when the user needs AI video shot design and production prompts: asset image prompts, per-shot first-frame/end-frame/keyframe planning, video generation prompts, Seedance/LibTV prompt workbooks, continuity locking, camera/action/sound design, prompt QA, and keyframe necessity review. Triggers on 镜头设计、分镜Prompt、视频Prompt、首帧Prompt、结尾帧Prompt、中间关键帧、关键帧规划、运镜、Seedance、LibTV、逐镜执行表、设定资产制作表.
---

# 镜头设计师

Use this skill to design production-ready image/video prompts from an approved script, client confirmation workbook, storyboard, or asset plan.

This skill owns prompt generation. Upstream producer skills such as `韦斯安德森` should call this skill instead of carrying prompt-writing rules directly.

## Inputs

Use the most complete available sources:
- approved client confirmation workbook, such as `项目名_脚本与资产确认表_v01.xlsx`
- internal asset production workbook, such as `设定资产制作表_v01.xlsx`
- confirmed character, scene, product, prop, and effect assets under `03_设定资产/`
- user-provided prompt reference or approved style sample
- picture ratio, such as `9:16竖屏` or `16:9横屏`
- platform/tool target, such as Seedance, LibTV, or a generic image/video model

If required source facts are missing, mark them as `待提供` or `待确认`. Do not invent product appearance, official logo details, screen text, character approvals, or client decisions.

## Outputs

Typical outputs:
- internal asset image prompts inside `设定资产制作表_v01.xlsx`
- `05_内部制作执行/内部执行脚本与Prompt表_v01.xlsx`
- first-frame, optional middle-keyframe, and end-frame prompts
- `生成前执行说明`
- `视频内容Prompt（含声音/负面）`
- keyframe generation task list or visual QC notes

Python scripts may create workbook scaffolds, extract source fields, and validate finished prompts. They must not generate final prompt prose by template.

## Video Prompt Output Contract

When writing `视频内容Prompt（含声音/负面）`, copy this exact top-level structure. Do not rename, translate, reorder, or replace these three headings with alternatives such as `视频类型`、`产品一致性`、`声音要求`、`三段式结构`、`第一段/第二段/第三段`.

```text
【基础设定】
镜头任务：
参考素材：
人物/产品/道具/场景：
连续性：
声音：
文字策略：默认画面为无文字纯图片。禁止生成字幕、标题、角标、水印、说明文字、乱码、伪Logo、排版边框和UI界面。产品镜头仅保留官方素材中已有的品牌Logo和官方屏显信息；剧情道具文字只允许最小必要大字或后期替换占位。

【氛围与画质】
风格核心：
视觉基调：
色彩与影调：
质量边界：

【画面内容】
分镜一：00:00-00:00
景别：
机位：
构图：
运镜手法：
画面内容：
特效：
声音：
结束状态：
衔接要求：
```

If a field is not relevant, write a concrete negative or boundary such as `特效：无新增特效` or `参考素材：未提供实际文件，按文字设定执行；不得写成已上传参考图`. Do not omit fields.

All per-shot final video prompts must pass this contract before delivery:
- exact top-level headings: `【基础设定】` → `【氛围与画质】` → `【画面内容】`
- no extra top-level headings
- `【基础设定】` must include explicit `文字策略：`; non-product shots still need no-subtitle/no-watermark/no-garbled-text rules
- every time-coded block contains all nine detail labels
- BGM/music generation is explicitly forbidden inside `声音：`

## Core Workflow

1. Read the approved source from beginning to end.
2. Lock continuity before writing prompts:
   - scene geography and camera axis
   - character positions, eyelines, seating/blocking, left/right relationships
   - product position/state and official-material constraints
   - prop/effect state changes
   - shot-to-shot handoff
3. Decide reference roles for each shot:
   - character identity
   - costume/body silhouette
   - background/scene lock
   - product appearance
   - prop/effect appearance
   - first/end/keyframe state
4. Write the video prompt first.
5. Decide the keyframe plan from the video prompt.
6. Write only the needed frame prompts.
7. Validate and fix before delivery.

## Checkpoints

Use these explicit checkpoints to avoid generating the wrong production layer:

- `CHECKPOINT 1 · Source lock`: before writing any prompt, confirm the script or workbook is the approved source. If the source is draft, missing, or contradicted by newer user feedback, stop prompt writing and ask for the latest source.
- `CHECKPOINT 2 · Asset lock`: before writing video prompts that bind references, confirm which character, scene, product, prop, first-frame, and end-frame assets actually exist. If a reference is only described in text and not available as a file, mark it `待提供` or `待生成`; do not write it as uploaded.
- `CHECKPOINT 3 · Keyframe decision`: after the video prompt is drafted and before frame prompts are written, decide which of `首帧 / 中间关键帧 / 结尾帧` are needed. Skip blank or unnecessary keyframe cells.
- `CHECKPOINT 4 · Pre-generation QC`: before connecting assets to Seedance, LibTV, or another video node, validate the workbook and visually inspect generated frames. Failed frames must be regenerated or marked unusable before video generation.

## Failure Handling

| Failure | Required action |
|---|---|
| Approved script/workbook is missing | Stop prompt writing; ask for the approved source path. |
| Asset reference is named but file is missing | Mark `待提供` or `待生成`; do not claim it is uploaded or bound. |
| Product official asset is missing | Do not invent product shape, logo, screen text, outlet, or material; request official material. |
| Prompt contains BGM/music generation wording | Remove it from the model-facing video prompt; keep only `不需要配乐，不生成BGM，音乐后期单独配。` |
| Text strategy conflicts with product/story text | Default to no subtitles/watermarks/garbled text; allow only confirmed product text or story-critical prop text. |
| `景别/机位/构图/运镜手法` are mixed | Rewrite the time block before delivery; do not leave mixed fields for production. |
| Negative list is broad or copied across shots | Prune to the current shot's 3-6 relevant quality boundaries, maximum 8. |
| Keyframe cell conflicts with `生成前执行说明` | The execution note wins; blank skipped keyframe cells and update the video prompt reference roles. |
| Visual QC fails | Do not connect the failed frame to video generation; regenerate or revise the prompt first. |

## Asset Image Prompt Rules

For asset still images, use structured sections such as:
- `【核心主题】`
- `【基础设定】`
- `【画面构图】`
- `【氛围与画质】`
- `【细节要求】`
- `【负面要求】`
- `【输出要求】`

Character assets:
- recurring characters need a clean no-text headshot and a clean no-text full-body image
- three-view sheets are useful for visual confirmation and archives, but should not be the default main video reference
- do not ask the image model to draw labels, arrows, captions, page borders, or `正面/侧面/背面` text inside the image

For all generated asset/frame images, add:
`画面为无文字纯图片。禁止生成字幕、标题、角标、水印、说明文字、乱码、伪Logo、排版边框和UI界面。`

Product exception:
`仅保留官方产品素材中已有的品牌Logo和官方屏显信息，Logo位置、比例和拼写必须与官方素材一致。禁止新增任何文字、伪Logo或屏幕文案。`

Story-prop exception:
If a newspaper, letter, sign, package, or screen is story-critical, allow only the minimum visible text needed for the story. Prefer large simple text or post-production replacement. Still forbid subtitles, watermarks, random labels, garbled text, and UI captions.

If product screen text is hard to generate accurately, generate a clean product image first and add exact text in post-production.

## Video Prompt Requirements

Each `视频内容Prompt（含声音/负面）` must include:
- `【基础设定】`
- `【氛围与画质】`
- `【画面内容】`

Do not use the old long heading stack as the default video prompt:
- no standalone `核心主题：`
- no standalone `【运镜规则】`
- no standalone `【关键帧调用】`
- no standalone `【声音/台词】`
- no standalone `【负面要求】`

Use this three-part architecture:
- `【基础设定】`: shot task, reference roles, characters/products/props/scenes, continuity, global sound boundary, text strategy, product/logo/story-prop text boundary
- `【氛围与画质】`: `风格核心`、`视觉基调`、`色彩与影调`、visual quality boundaries
- `【画面内容】`: time-coded beats, shot size, camera angle, composition, camera movement, action/story effect, VFX, per-beat sound, end state, transition

For live-action or photoreal shots, `风格核心` must include:
`电影级质感、超写实、极致逼真、Photorealism、真人实景拍摄`
Then add the project-specific genre/style and concise boundaries such as `杜绝游戏CG感、杜绝动作僵硬`. Use `Photorealism`; do not misspell it as `Photirealism`.

Negative requirements must not sit inside the shot task. Put text strategy, product/logo limits, and story-prop text exceptions in `【基础设定】`; put short shot-relevant quality negatives in `【氛围与画质】`; put action-specific forbidden behavior in the relevant `【画面内容】` beat. Keep quality negatives to 3-6 items by default and no more than 8. If the user explicitly requires a longer blacklist, put the extra rules in `生成前执行说明`, not in the model-facing video prompt.

Text strategy is mandatory for every video prompt, including non-product shots. For non-product shots, write the full no-text boundary instead of only mentioning it near the ending beat.

Product and commercial-effect policy:
- product, logo, official screen, face, hand, and key prop visibility outrank decorative effects
- effects must be visible enough to explain the story or selling point, but must not cover product structure, face identity, hands, logo, or official screen
- for product ads, use clean controllable effects such as transparent airflow, soft light trace, fine particles, glass reflection, water vapor, or restrained energy lines
- avoid over-conservative prompts that make the product effect invisible; describe the effect path, density, start/end state, and what it must not obscure

For `【画面内容】`, do not summarize the whole shot only. Use time-coded beats when the shot has multiple actions, product entrances, transformations, VFX, or lasts more than 2 seconds.

Every time-coded beat must state:
- `景别`
- `机位`
- `构图`
- `运镜手法`
- `画面内容`
- `特效`
- `声音`
- `结束状态`
- `衔接要求`

Field discipline:
- `景别` only describes shot size, such as `大全景`、`全景`、`中景`、`中近景`、`近景`、`特写`; do not write `电影感` or `史诗感` there.
- `机位` describes camera position/angle/height, such as `无人机高空俯拍`、`低机位仰拍`、`平视正面30度`.
- `构图` describes frame layout, subject placement, foreground/midground/background, guide lines, and negative space.
- `运镜手法` describes camera movement and rhythm, such as fixed shot, push-in, follow shot, pan, tilt, orbit, handheld, drone follow, and cut rules.

Avoid placeholders such as `按本镜头需要选择`, `根据主体动作采用`, `按画面执行`, `保持可识别`, `适当`, or `根据实际情况`. Replace them with concrete subject, body part, prop, product state, effect path, composition, and camera path.

Do not ask the video tool to generate music, BGM, underscore, score, or background music. Always keep music as post-production guidance outside generation. In the model-facing video prompt, explicitly write `不需要配乐，不生成BGM，音乐后期单独配。`

For Seedance-oriented prompts, write explicit reference roles in `【基础设定】`, such as:
`首帧@镜头03_首帧_v02.png作为00:00起始状态；中间关键帧不使用，以分镜动作和运镜控制中段；结尾帧@镜头03_结尾帧_v02.png锁定镜头结束状态。`

## Keyframe Policy

Keyframe columns are status slots, not obligations.

Default approach:
- `首帧Prompt`: usually required for independently generated clips
- `结尾帧Prompt`: generate when the final state is materially different or must hand off to the next shot
- `中间关键帧Prompt`: skip by default; generate only for a materially different middle state

Prefer a simpler plan when it gives better control:
- use only `首帧`
- use `首帧 + 结尾帧`
- skip middle frames when they only differ by mouth shape, tiny expression, gaze, small hand height, or minor dialogue timing

Generate middle keyframes only for material differences:
- product state change
- transformation midpoint
- visible VFX path
- large blocking or position change
- camera-axis/shot-size change
- long multi-beat action that cannot be controlled by first/end alone

Pure black, pure white, solid-color, fade-only, and no-subject transition frames are not AI keyframes. Keep those as video or post-production instructions.

## Keyframe Reuse

If one continuous action is split into two rows and the previous shot's final visible state exactly equals the next shot's starting state, generate the image once.

Prefer:
`复用上一镜头结尾帧：镜头NN_结尾帧_vXX.png`

Reuse is allowed only when subject, pose/state, camera angle, shot size, composition, scene geography, and product/prop state are the same.

## Visual QC

Before connecting any keyframe to Seedance, LibTV, or another video node:
- compare the generated image to its own prompt
- compare it to the video prompt and `生成前执行说明`
- check character face, costume, body type, hair ornaments, props
- check official product shape, logo, screen, outlet, proportions, and official material constraints
- check shot size and composition
- check start/middle/end action state
- check spatial continuity and camera axis
- check no captions, labels, UI, watermark, garbled text, or unintended logo

If a reference image was only mentioned in text and not actually uploaded/bound, say so. Claim visual-reference use only for files that are actually uploaded or selected.

## Workbook Rules

Internal prompt workbooks should include separate columns for:
- `参考素材`
- `首帧Prompt`
- `中间关键帧Prompt`
- `结尾帧Prompt`
- `生成前执行说明`
- `视频内容Prompt（含声音/负面）`

Keep `生成前执行说明` for production bookkeeping:
- which frames to generate or skip
- which assets to upload/select
- reuse decisions
- visual QC requirements
- production-only notes

Keep `视频内容Prompt（含声音/负面）` model-facing:
- scene
- action
- camera
- composition
- effect
- sound/dialogue
- end state
- transition/handoff
- reference and keyframe roles inside `【基础设定】`

## Scripts

Use these scripts when useful:

```bash
python /Users/jude/.codex/skills/shot-designer/scripts/build_asset_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Creates `05_内部制作执行/设定资产制作表_v01.xlsx` for internal asset prompt writing and image production.

```bash
python /Users/jude/.codex/skills/shot-designer/scripts/build_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Creates a blank internal prompt workbook scaffold. Prompt cells are intentionally blank for AI writing.

```bash
python /Users/jude/.codex/skills/shot-designer/scripts/validate_prompt_detail.py \
  --input "/path/to/内部执行脚本与Prompt表_v01.xlsx"
```

Run validation before delivery. Treat missing three-part prompt sections, missing `风格核心/视觉基调/色彩与影调`, placeholder filler, keyframe mismatch, full local paths, missing text strategy, and music-generation wording as blocking issues.

## Call From 韦斯安德森

When `韦斯安德森` reaches internal asset prompt writing or final per-shot video prompt writing, it should pass this skill:
- approved confirmation workbook path
- project directory
- confirmed asset directory
- target ratio
- tool target
- any user-approved prompt style
- whether the output is asset still prompts or per-shot video prompts

After this skill finishes, return the workbook path, validation result, skipped keyframe decisions, and next required confirmation.
