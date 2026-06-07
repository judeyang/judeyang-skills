# Internal Shot Prompt Standard

Use this structure in the final `内部执行脚本与Prompt表.xlsx`.

One row = one shot. Keep execution logistics and actual video prompt separate:
- `生成前执行说明`: what to generate/upload/select before video generation.
- `视频内容Prompt（含声音/负面）`: what the video should look and sound like.

## Prompt Template

```text
核心主题：用一句话写清本镜头的视觉任务，不写空泛宣传语。说明本镜头到底是在完成表演、产品露出、动作转化、空间建立还是情绪反应。

【全片连续性/空间关系】
State any locked scene geography, seating/blocking, left-right relationships, product position, prop position, and shot-to-shot handoff rules that must remain consistent.

【基础设定】
Describe locked characters, product, props, and continuity rules.

【氛围与画质】
Describe global visual quality, genre, texture, lens feel, color tone, and brand tone.

【运镜规则】
State whether the shot is a stable reaction shot, long dialogue performance, product reveal, continuous transformation, or cuttable multi-beat action. Then state camera path, movement speed, focus rule, axis rule, and allowed/forbidden cuts.

基础镜头：
景别：
机位：
构图：
运镜：

【首帧画面】
Describe the first frame/keyframe precisely: subject position, pose, scene layout, visible product, and action starting state.

【中间关键帧画面】
When needed, describe the strongest mid-shot reference frame separately from the true first frame. If no separate middle keyframe image is generated, keep the workbook cell blank and let `生成前执行说明` state the skip.

【结尾帧画面】
Describe the visible end result, final subject position, product state, and handoff to the next shot. If no separate end-frame image is generated, keep the workbook cell blank and let `生成前执行说明` state the skip.

【光线/色彩/质感】
Describe lighting source, color palette, contrast, atmosphere, texture, and visibility.

【画面内容】
Use time-coded sub-shots when a shot lasts more than 2 seconds or contains multiple actions/effects. Follow this structure:

分镜一：00:00-00:02 景别：... 机位：... 构图：... 运镜手法：... 画面内容：...
分镜二：00:02-00:05 景别：... 机位：... 构图：... 运镜手法：... 画面内容：...

For continuous transformation / appearance / product-generation shots, use staged time blocks:

00:00-00:02 · 阶段名
动作：...
镜头：...
特效：...
声音：...

For simple 1-2 second shots, one segment is enough. For product entrances, transformations, fights, or effect transitions, split the prompt into clear time ranges.

【声音/台词】
台词/旁白:
音效/同期声:
音乐/BGM: 不生成，后期单独配。

【负面要求】
State all forbidden deviations.
For non-product images, always include: 画面为无文字纯图片。禁止生成字幕、标题、角标、水印、说明文字、乱码、伪Logo、排版边框和UI界面。
For product images, official product logos or official screen text may remain only when they come from client-provided official assets: 仅保留官方产品素材中已有的品牌Logo和官方屏显信息，Logo位置、比例和拼写必须与官方素材一致。禁止新增任何文字、伪Logo或屏幕文案。
```

## Detail Requirements

Every shot prompt should answer:
- who/what is the subject
- where the shot takes place
- what continuity rule from previous/next shots must be preserved
- where each recurring character sits/stands if the scene has a seating map or fixed blocking
- shot size
- camera height and angle
- subject position in frame
- foreground/midground/background
- camera movement
- action start and end
- VFX start and end
- product/logo visibility
- line delivery and timing
- audio boundary
- negative constraints

After writing a prompt, prune it by shot relevance:
- Remove product/Logo/screen/outlet rules from shots where no product appears and no product state changes.
- Remove full seating-map prose from product-only shots unless the camera still shows the banquet geography.
- Keep off-screen spatial anchors only when they guide eyelines, movement direction, or shot handoff.
- Keep negative requirements specific: non-product performance shots need no-text, face/hand/costume/period-setting constraints; product shots additionally need product-shape, Logo, screen, outlet, and invented-UI constraints.
- For 1-2 second shots, keep one concrete time block and avoid full whole-film memos.

Seedance-fit self-audit:
- Use a prompt as a shot brief, not a production memo. It should tell the model what to see and hear, not repeat internal process rules.
- Make each reference purposeful: `人物@...控制脸和服装`, `背景@...锁定宴会厅`, `产品@...锁定机身比例/Logo/出风口`, `首帧@...作为00:00起始状态`.
- Character consistency should not rely on three-view sheets. Default character video references are a clean no-text face close-up/headshot for facial identity plus a clean no-text full-body image for costume, body proportion, and silhouette.
- Avoid direct video-generation use of three-view sheets, labeled contact sheets, UI screenshots, or text-heavy references. Multi-view assets can guide internal asset prep only; do not connect them as the final video node's main character reference because the model may treat multiple views as multiple subjects.
- Describe movement with body part + direction + speed + degree + transition. Example: `右手从桌沿缓慢抬起到胸前，停半拍后用团扇指向产品`.
- Express emotion as visible behavior, not adjectives. Example: replace `很得意` with `嘴角上扬、眼神向镜头停半拍、下巴微抬`.
- Match complexity to duration. A 2-second shot should normally have one visual task; long dialogue, effect transformation, product state change, or camera switch needs separate time blocks and, if useful, middle keyframes.
- For Seedance-facing prompts, mark spoken lines with `{}` and key sound effects with `< >` where practical, while still keeping the workbook's `台词/旁白` and `音效/同期声` labels for human scanning. Example: `黛玉用中文轻声说道{我身子怯...}` and `音效/同期声：<团扇轻响><衣袖摩擦>`.
- After any video prompt edit, update keyframe prompts and `【关键帧调用】` immediately. Keyframe calls must name the actual visible state, not a generic phrase.

Video prompts only control production sound: dialogue, voiceover, foley, action sound effects, product sound effects, room tone, wind, cloth, footsteps, cups, button clicks, and clean audio in/out. Do not ask the video tool to generate music, BGM, underscore, score, or background music. Music direction from the client script belongs in a post-production note outside the video prompt; inside the video prompt write `音乐/BGM：不生成，后期单独配。`

## First Frame vs Middle Keyframe

Do not confuse the true first frame with a middle keyframe.

The true first frame is the video starting state:
- before the main action completes
- before a product fully appears, unless the shot starts with product display
- before a character has fully transformed, disappeared, or been absorbed
- useful for image-to-video generation as frame 0

The middle keyframe is the shot's strongest reference image:
- product fully or mostly visible
- transformation / absorption / fight / magic effect already in progress
- used to lock visual quality, product structure, action path, and VFX direction

In execution workbooks, if both are useful, keep them as separate columns:
- `参考资产`
- `首帧Prompt`
- `中间关键帧Prompt`
- `结尾帧Prompt`
- `视频内容Prompt（含声音/负面）`

Do not create a separate transition column. Put `衔接要求：` inside the time-coded video Prompt blocks.

Also keep `原始脚本内容` in the same row as the execution prompt. It should include original shot size, picture, duration, dialogue/voiceover, sound/music, notes, and later user change instructions when applicable.

## Time-Coded Shot Segments

When writing `【画面内容】`, the reference creator's core method is: every important second range has its own visual job. Do not write only a paragraph summary.

### Mandatory Detail Gate

Every time-coded segment must contain these production-visual labels:

```text
景别：
机位：
构图：
运镜手法：
动作：
特效：
声音：
结束状态：
衔接要求：
```

This applies even to simple 1-2 second shots. Use `特效：无新增特效` when no effect is needed. Use `声音：无` or a specific sound boundary when silent. Do not omit fields.

Do not put raw upload bookkeeping inside every time-coded video segment. Put upload/selection operations in `生成前执行说明`. The actual video prompt still needs a compact `【关键帧调用】` section near the top so image-to-video tools know which uploaded image controls the first frame, middle state(s), and end frame. This is model-facing instruction, not a production checklist. In the video prompt, if an asset identity matters visually, mark it inline in the relevant visual sentence using `类别@文件名`, e.g. `人物@角色_贾母_设定图_预览_v02.png`, `场景@场景_贾母C位座次_预览_v02.png`, `背景@场景_大观园宴会厅全景_预览_v02.png`, `道具@道具_团扇绢帕宴席器物_设定_预览_v02.png`, `产品@官方产品图.png`, `特效@特效_170度环抱送风_关键帧_预览_v02.png`.

Use `背景@文件名` whenever a repeated background must stay unified across shots. This is separate from `场景@文件名`: `场景` can describe the space, while `背景` tells tools such as SeedDance to lock the same visible background/environment rather than merely borrowing atmosphere.

## Reference-style structure

The user's reference prompts use this practical structure:

```text
核心主题：...

【人物与基础设定 / 基础设定】
人物/产品/道具/场景/声音边界。

【氛围与画质】
风格核心、摄影机/镜头质感、色彩影调、光线、材质、真实感边界。

【运镜规则 / 镜头规则】
单镜头或切镜方式、开场角度、镜头路径、呼吸感、是否允许反打/跳切。

【关键帧调用】  # image-to-video projects only
首帧/中间关键帧/结尾帧的文件名和可见状态。

【画面内容】
0-2秒 · 动作阶段名
景别：
机位：
构图：
运镜手法：
动作：
特效：
声音：
结束状态：
衔接要求：

【声音/台词】
...

【负面要求】
...
```

Do not mistake this for a rigid heading list. The reference style works because every time block contains concrete visual facts: body parts, expression, prop position, product state, effect material/path, camera movement, and sound boundary. Generated prompts should not read like a spreadsheet template.

Forbidden filler in final video prompts:

```text
围绕本段动作组织画面
关键人物、手部动作、道具和视线方向完整入画
视线或运动方向预留空间
按9:16竖屏组织前景、中景、背景层次
固定机位，仅保留轻微呼吸感
只生成只保留
```

Replace each filler phrase with the shot's actual subject and camera behavior.

Keyframe columns are not automatic generation instructions. They are status slots. The actual generation list must come from the video prompt's action structure plus the `生成前执行说明` column:
- If `生成前执行说明` says the middle keyframe is skipped, the `中间关键帧Prompt` cell must be blank.
- If `生成前执行说明` says the end frame is skipped, the `结尾帧Prompt` cell must be blank.
- Do not write a full image prompt in a keyframe column that `生成前执行说明` says should not be generated.
- Before generating images, skip blank keyframe cells and follow `生成前执行说明`.

In the final workbook, the keyframe decision should be visible through `生成前执行说明`, not through extra process worksheets. The video prompt must then repeat the usable frame roles in `【关键帧调用】`, using the final image filenames and their visible purpose:

```text
【关键帧调用】
首帧：镜头NN_首帧_vXX.png，作为00:00起始状态。
中间关键帧：不使用单独中间关键帧，以分镜动作和运镜控制中段。
结尾帧：镜头NN_结尾帧_vXX.png，锁定镜头结束状态；末段动作收束到该画面。
```

After keyframe images are generated, run visual QC before using them in video generation:
- Check actual shot size against the requested one. A generated image that remains a full view fails if the prompt/end state requires medium shot.
- Check actual pixel dimensions against the confirmed delivery ratio. For `9:16竖屏` production keyframes, use a 4K vertical working copy such as `2160x3840` PNG when possible. If the approved generated image is lower resolution, keep the original and create a sibling `_4K.png` copy before connecting it to video-generation nodes.
- Check actual action state against the role: first frame = start, middle keyframe = mid-performance/mid-action, end frame = final stable state.
- Check scene geography and seating continuity against the continuity map.
- Check identity and product state against reference assets.
- Check no text/no labels/no watermark/no UI/no garbled characters.

If visual QC fails, regenerate the image and update both `生成前执行说明` and `【关键帧调用】` with the new filename/version before building or running video nodes. Do not connect failed keyframes to LibTV/SeedDance nodes just because the file exists.

When the video action changes shot size, write the keyframe prompt with explicit positive and negative size constraints. Example:

```text
结尾帧必须是贾母与C位空座的中景/中近景，不是全宴席全景；不要保留完整圆桌和整间大厅。
```

The order of work is video first, frames second:
1. Write the video prompt from the original/confirmed script.
2. Use the video prompt's time blocks, action states, end states, and transition handoff to decide which frame images are actually needed.
3. Only then write the frame prompts.

Decision criteria:
- 首帧: required for independently generated clips unless it explicitly reuses the previous shot's end frame.
- 中间关键帧: required only for long/multi-beat dialogue, emotional change, movement across frame, product state change, transformation, VFX path, complex camera move, or other middle state that first/end frames cannot lock.
- Multiple middle keyframes: required when one shot contains long dialogue with clear acting beats, a camera switch, picture switch, jump cut, or several materially different middle states. Name them with suffixes such as `中间关键帧A` and `中间关键帧B`.
- 结尾帧: required only when the ending state is materially different, must be controlled for generation, or will be reused as the next shot's first frame.
- Pure black, pure white, solid-color, empty fade-in/fade-out, or no-subject transition frames are not AI keyframes. Do not write image prompts for them and do not spend image-generation compute on them. Express black-screen/fade requirements in `视频内容Prompt（含声音/负面）` or post-production notes instead.
- Reuse adjacent frames only when the previous end and next first are exactly the same visible state: same subject, pose/state, shot size, camera angle, composition, scene geography, and product/prop state. Same location alone does not count.
- If reused, the next shot's `首帧Prompt` should start with `复用上一镜头结尾帧：...` and should not contain another full prompt.

Forbidden placeholder wording:

```text
按本镜头需要选择
根据主体动作采用
按画面执行
保持可识别
适当
根据实际情况
```

Replace placeholders with concrete instructions before delivering the workbook.

Passing the label check is not enough. Do not mechanically repeat a generic sentence such as `主体位于画面中心` across every segment. Tie each field to the actual shot: name the character or product, state the foreground/midground/background relationship, and describe what state must be visible at the end of the time range.

## Whole-Film Continuity Pass

Before writing shot prompts, read the full approved execution script from start to finish and produce a continuity note. This is mandatory for recurring scenes and character relationship scenes.

The continuity note should answer:
- What is the stable scene geography?
- What is the camera axis?
- Where are the important seats, props, products, doors, windows, light sources, or airflow sources?
- Which characters sit or stand together?
- Which left/right relationship is locked from the viewer's perspective?
- Which object or product state changes over time?
- Which shots intentionally break the axis or change position, and how is that justified?

For banquet, family-table, court, meeting, classroom, vehicle, or any repeated group scene, define the seating map before writing prompts. If shot 1 establishes character A beside character B, shot 2 must not put character A beside character C unless the script explicitly shows movement, a cutaway, or a changed camera angle that explains it.

Put a short continuity section into each affected prompt:

```text
【全片连续性/空间关系】
本场景沿用统一座次/空间轴线：……
本镜头不得改变：……
本镜头允许变化：……
```

The continuity section should be concise but concrete. It should not be a generic sentence such as `保持连续性`.

Do not confuse continuity with visibility. A locked seat/person/prop can be outside the frame in a local close-up or medium shot if the camera has cropped in logically. In that case, state the off-screen position explicitly and use eyeline/body direction to preserve geography. Example: `C位空座和贾母在画外左侧，本镜头只拍黛玉、宝玉、宝钗三人；三人视线偶尔向画外左侧回应贾母与C位方向。`

Use either of these two practical structures according to the shot:

### A. Multi-Shot / Cuttable Segment Structure

Use this for shots that can be understood as several visual beats, product display, action progression, or camera changes:

```text
分镜一：00:00-00:02
景别：近景。
机位：贴近地面低机位。
构图：主体位于画面中心，背景保留场景信息。
运镜手法：固定机位。
动作：主体执行一个清晰动作。
特效：无。
声音：环境声持续。
结束状态：主体动作完成第一阶段，停留在可衔接状态。
画面锚点：人物@角色设定图文件名；背景@场景设定图文件名。
衔接要求：动作连续进入下一阶段；最后一个时间段写清与下一镜头的切换方式。
```

### B. Continuous Transformation / One-Take Stage Structure

Use this for single-take transformation, character entrance, magic-object/product generation,消散,吸入,爆发,生长,变身等镜头。It should look like the user's supplied creator template:

```text
00:00-00:02 · 凝视/显化/启动
动作：主体保持明确动作起点，视线、姿态和道具位置清楚。
镜头：固定或缓慢推进，说明景别、机位和主体位置。
特效：第一层效果出现，不要一次性完成变化。
声音：环境声或能量声进入。

00:02-00:05 · 生成/转化/收束
动作：主体动作继续，变化路径和方向明确。
镜头：跟随动作或轻微推近，保证关键物体不出画。
特效：说明材质、粒子、烟雾、水流、光源的运动轨迹。
声音：音效增强，但不盖过台词。

00:05-00:07 · 完成/定格/产品露出
动作：结果稳定，角色或产品进入可识别状态。
镜头：给最终主体或产品一个清晰可用的广告画面。
特效：效果减弱或定格，避免遮挡产品结构和Logo。
声音：结束点干净，给剪辑留余量。
```

This is required for:
- shots longer than 2 seconds
- any shot with multiple beats
- product entrance
- character transformation
- VFX transition
- camera move plus dialogue
- before/after state changes

Selection rule:
- If the shot is mainly a sequence of visible beats or camera changes, use structure A.
- If the shot is one continuous generation, transformation, absorption, appearance, or magic/product reveal, use structure B.
- If both apply, use structure B and still include 景别、机位、构图、运镜 inside each time block.

## Common Negative Requirements

Use and adapt:

```text
避免卡通Q版，避免现代城市背景，避免人物脸部漂移，避免服装变化，
避免产品结构变形，避免Logo错误，避免多余文字，避免低清，
避免畸形手指，避免重复角色，避免恐怖血腥，
避免腐烂病菌和医学化符号，避免画面过脏或过暗。
画面为无文字纯图片。禁止生成字幕、标题、角标、水印、说明文字、乱码、伪Logo、排版边框和UI界面。
```

## Product Rules

If a real product is involved:
- Official product references override prompt imagination.
- Put product filenames in `【参考素材】`.
- In `【基础设定】`, state that product shape, logo, screen text, and proportions must not change.
- In `【负面要求】`, explicitly forbid logo errors, product deformation, and invented UI.
- If the official product asset contains a real brand logo or screen UI that must appear, state that only official existing text may remain and no new text may be invented.
- If accurate product screen text cannot be guaranteed by generation, generate a clean image and add the exact screen text in post.

## Text In Reference Images

Reference images containing labels, notes, title text, subtitles, watermarks, UI panels, or layout borders can contaminate generation results. Prefer clean `无文字` image-only references for characters, scenes, first frames, middle keyframes, and end frames.

When a setting sheet with text is already approved, create a separate generation-reference export named like:

```text
角色_林黛玉_视频生成参考版_无文字_v01.png
场景_大观园宴会厅_视频生成参考版_无文字_v01.png
```

Use the clean version in production prompts while keeping the original confirmed sheet in the archive.

## Dialogue Timing

Keep prompt dialogue aligned with duration:
- 1-2 seconds: only a reaction word or short line.
- 3 seconds: one short line.
- 4 seconds: one clean product line.
- Longer explanation requires longer shot or voiceover.

## Prompt Writing Style

The final prompt is a director-writing task, not a spreadsheet automation task. Use scripts only for structure, extraction, consistency checks, and validation. Scripts must not generate, draft, prefill, or template-fill prompt cells. `首帧Prompt`, `中间关键帧Prompt`, `结尾帧Prompt`, `生成前执行说明`, and `视频内容Prompt（含声音/负面）` should be blank in the script-generated scaffold and then written shot by shot by the AI after the whole-film continuity pass.

For each shot, write from intent to execution:
1. What is this shot's visual purpose?
2. What must stay continuous from previous and next shots?
3. Which reference assets must be locked?
4. What image frames are actually needed?
5. What happens in each second range?
6. What must the video tool avoid?

If the text still reads like a reusable template, it is not finished.

Prefer complete visual instructions over vague adjectives.

Weak:
```text
画面很高级，悟空很帅，风很大。
```

Better:
```text
景别：悟空中近景。机位：略低角度，强调警觉和主角气势。
构图：悟空脸部先占画面主体，随后露出唐三藏在后方。
悟空猛地抬头，火眼金睛微亮，随后回身护在唐三藏前。
```
