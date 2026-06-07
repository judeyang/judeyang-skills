# Internal Execution Prompt Workbook Rules

Final output for production: `内部执行脚本与Prompt表.xlsx`.

Use one worksheet when possible. One row = one shot. Include:
- shot number
- original shot number
- original script content
- confirmed execution content
- dialogue/voiceover
- duration
- one complete generation prompt
- production status
- output filename
- change note

Save this workbook directly in `05_内部制作执行/`. Do not create a separate `02_视频Prompt` folder because the prompt content belongs in the Excel workbook.

For internal execution Prompt workbooks, keep the workbook readable rather than dumping text into one oversized table:
- Put project metadata, usage notes, version notes, picture ratio, and execution instructions in a separate worksheet named `项目说明`.
- The main worksheet should start directly with the table header row, usually named `执行脚本与Prompt表` or `内部执行脚本与Prompt表`.

Video prompts must follow the user's approved reference-prompt writing style, not only the workbook column structure. Each `视频内容Prompt（含声音/负面）` must include `核心主题：` and `【运镜规则】`, then use time-coded action blocks with concrete camera, composition, action, effect, sound, end state, and transition requirements. Do not deliver prompts that only repeat generic production rules.

Prompt-writing quality has priority over speed. Automation scripts may create workbook structure, extract source fields, prepare reference assets, and run validation after prompts are written, but scripts must not generate, draft, prefill, or template-fill any Prompt content. The final `首帧Prompt`, `中间关键帧Prompt`, `结尾帧Prompt`, `生成前执行说明`, and `视频内容Prompt（含声音/负面）` must be written shot by shot by the AI after reading the approved script, continuity notes, available assets, user references, and the sample prompt style.

Every final video prompt must pass a relevance-pruning pass. Keep only the continuity, assets, product rules, negative rules, and style details that affect that specific shot. Product shape, Logo, screen, outlet, and official-material constraints belong only in shots where the product is visible or directly changes state. Seating rules belong only where seat geography, eyelines, or character blocking matters. Do not copy the same whole-film memo into every row; long repeated global text dilutes the video model's attention and makes the prompt harder to check.

Before delivering any final prompt workbook, run a Seedance-fit self-audit and fix the workbook yourself before the user reviews it:
- Reference roles: every uploaded image/video/audio reference used in the actual video prompt must say what it controls, such as character identity, product appearance, background, first frame, end frame, action, camera, sound, or effect. Do not merely list files.
- Reference economy: upload only references that affect the shot. Too many weak references dilute control. For repeated characters, prefer the cleanest current single-character video reference over full setting sheets.
- Character references: do not rely on three-view sheets to control video identity. For recurring characters, prefer a clean no-text face close-up/headshot for facial identity plus a clean no-text full-body image for costume, body proportion, and silhouette. If a character asset is a three-view sheet, contact sheet, labeled design page, or contains several angles of the same person, do not use it directly as the main video reference; create or request the headshot/full-body video-reference pair first.
- Action detail: describe body part, direction, speed, degree, and handoff. Prefer low, continuous, physically plausible actions unless the script explicitly needs high-impact movement.
- Emotion detail: translate abstract emotion into visible face/body behavior, such as eyes, mouth corner, shoulders, fingers, breath, posture, gaze, or pause.
- Dialogue/sound markup: for Seedance-facing prompts, wrap spoken dialogue in `{}` and key sound effects in `< >` where practical. Keep the human-readable labels too, but do not rely on labels alone when the line must be spoken in the generated clip.
- Shot duration fit: do not put several large actions into a 1-3 second shot; either split the shot or simplify the action.
- Keyframe sync: after changing the video prompt, rewrite `【关键帧调用】`, `生成前执行说明`, and all nonblank keyframe prompt cells so they describe the same start/middle/end states. A generic keyframe call such as `锁定中段动作、表情或视觉变化` is not acceptable.
- Self-correction: run the validator and also read representative rows manually. Do not wait for the user to discover obvious continuity, relevance, or keyframe mismatches.

Do not bulk-fill a final prompt workbook by script and present it as production-ready. If a script is used, it may only create a blank internal scaffold:
1. Read the full approved script from beginning to end.
2. Lock continuity: scene geography, seating/blocking, character relationships, product state, and shot handoffs.
3. Decide which frame prompts are actually needed per shot.
4. Write each prompt in the sample style with concrete second-by-second visual instructions.
5. Compare first/middle/end frame prompts against the video prompt so they do not contradict each other.
6. Run validation only after the AI-written pass; validation is a gate, not a substitute for writing.

The script-generated scaffold must leave these cells blank: `首帧Prompt`, `中间关键帧Prompt`, `结尾帧Prompt`, `生成前执行说明`, and `视频内容Prompt（含声音/负面）`. Filling those cells is an AI director writing task, not a script task.

Before delivering an internal prompt workbook, run `scripts/validate_prompt_detail.py`. Treat failures for template filler, missing `核心主题：`, missing `【运镜规则】`, keyframe mismatch, music generation wording, full local paths, or missing no-text rules as blocking issues.
- Freeze the main table header row at `A2`.
- Header rows must be bold, centered, and visually distinct.
- Short structured columns such as `镜号`, `原始镜号`, `执行时长(s)`, `台词/旁白`, `音效/音乐`, `制作状态`, and `样片建议` should stay compact; do not widen them just because the row height is large.
- Long text columns such as `原始脚本内容`, `确认后执行内容`, `参考素材`, `首帧Prompt`, `中间关键帧Prompt`, `结尾帧Prompt`, and `视频内容Prompt（含声音/负面）` should be left-aligned, top-aligned, and wrapped.
- Row heights should balance scanning and completeness. Do not set every row to a huge fixed height; use moderate heights and let users inspect long Prompt cells when needed.

Save first-frame and middle-keyframe images directly in `05_内部制作执行/01_首帧与关键帧/`. Do not create another nested folder such as `镜头首帧` under it.

For active/current asset folders, keep the structure flat whenever practical. For example, current character images should be placed directly in `03_设定资产/01_人物设定图/`, not inside `第一版启用/` or other version subfolders. Put unused or historical versions under `03_设定资产/90_历史版本/`.

Keep `03_设定资产` as a top-level project folder. Do not move it under `05_内部制作执行`: setting assets are confirmed reusable references, while `05_内部制作执行` contains production execution outputs such as the final prompt workbook, first/key frames, video clips, final renders, and cover assets.

Because execution still needs character, scene, product, prop, and effect references, create a lightweight reference entry inside `05_内部制作执行` only when useful: `00_设定资产参考入口` should point to `03_设定资产`. Prefer a symlink/alias/reference entry over duplicating or moving the asset folder, so there is still one source of truth. Do not create the reference entry as an empty placeholder.

The complete generation prompt should combine image, video, sound, and negative requirements in one cell. Use the standard in `references/prompt_standard.md`.

Before writing any shot Prompt, first do a whole-film continuity pass. Do not write prompts shot-by-shot in isolation. This continuity pass is internal reasoning and should normally be folded into the final row-level execution text, not exposed as extra process worksheets in the final internal workbook. It must define:
- scene geography and camera axis
- character seating/blocking positions and left/right relationships
- which character is beside whom, who is foreground/midground/background, and where empty seats or key props are located
- product position, product state, airflow/effect direction, and screen/open/closed state changes
- shot-to-shot handoff: what must remain unchanged from the previous shot and what changes in the next shot

For banquet, court, meeting, vehicle, classroom, family-table, or any repeated-group scene, lock the seating map before writing `首帧Prompt`, `中间关键帧Prompt`, `结尾帧Prompt`, and `视频内容Prompt（含声音/负面）`. Example: if shot 1 establishes character A beside character B, shot 2 cannot suddenly place A beside character C unless the script explicitly shows movement or a cutaway that justifies it.

Every internal video Prompt should reflect `全片连续性/座次` or `空间连续性` when applicable. Keep it concise and useful for generation; do not add separate process sheets just to show reasoning.

Continuity does not mean every anchor must remain visible in every shot. Before forcing a seat, prop, product, or character into the frame, decide whether it should be on-screen or off-screen for that shot size and camera direction. If a local close/medium shot crops out an established anchor, write it as an off-screen spatial anchor, e.g. `C位空座和贾母位于画外左侧，三人眼神和身体朝向仍按该方向组织`. Do not cram off-screen anchors into the background when doing so makes the composition illogical.

Carry the confirmed picture ratio into every internal prompt workbook and keyframe prompt. If the client/project confirms `9:16竖屏`, every `首帧Prompt`, `中间关键帧Prompt`, `结尾帧Prompt`, and `视频内容Prompt（含声音/负面）` must explicitly say `9:16竖屏`. Do not reuse `16:9横版` wording from older templates. For vertical videos, rewrite composition for a vertical frame: keep faces, hand actions, products, props, and effect paths inside the safe picture area; reorganize group shots with foreground/midground/background depth instead of cropping a horizontal group image.

Generated keyframe assets must be checked by actual pixel size, not only by visual orientation. For confirmed `9:16竖屏` video work, production keyframes should be saved as 4K vertical working files when possible: `2160x3840` PNG. If the image tool returns a lower-resolution but visually approved vertical image, keep the original file and create a sibling `_4K.png` production copy with high-quality upscaling before connecting it to LibTV/SeedDance nodes. Do not connect a low-resolution keyframe as the production reference when a 4K working copy is available.

When building LibTV video nodes for internal execution, distinguish reference-asset resolution from video-generation resolution. Keyframe/reference images may use 4K working files for identity and composition stability, but LibTV video node settings should default to `resolution=720p` unless the user explicitly asks for a different generation resolution. Always keep `ratio` aligned with the confirmed delivery format, e.g. `ratio=9:16` for vertical projects, and do not trigger generation when the user asks only to build nodes.

For `【画面内容】`, do not only summarize the whole shot. When the shot has multiple beats, write time-coded sub-shots such as `分镜一：00:00-00:02 景别...机位...构图...运镜手法...画面内容...`. This is required for product entrances, transformations, VFX transitions, and shots longer than 2 seconds.

Video Prompt detail is a hard acceptance gate, not an optional writing preference. Every time-coded segment must explicitly contain:
- `景别`
- `机位`
- `构图`
- `运镜手法`
- `动作`
- `特效`
- `声音`
- `结束状态`
- `衔接要求`

Use the user's reference prompt style as the writing benchmark, not merely as a column template. A strong video prompt should read like a compact director's shooting instruction:
- Start with the shot's `核心主题` or production intent when useful.
- Define `基础设定`: visible characters/products/props/scene and exact reference roles.
- Define `氛围与画质`: cinematic style, lens/camera feel, light, color, texture, realism boundary.
- Define `镜头规则`: single-take vs cut, opening angle, camera path, breathing/handheld/stabilized feel, and when the shot may or may not switch.
- Define `关键帧调用`: first/middle/end frame roles for image-to-video tools.
- Write `画面内容` as time-coded beats such as `0-2秒 · 凝视` or `分镜1：00:00-00:02`, where each beat has a concrete action state, camera behavior, VFX/sound, end state, and handoff.
- End with `声音/台词` and `负面要求` when needed.

Avoid table-derived filler. Do not use generic sentences such as `围绕本段动作组织画面`, `关键人物、手部动作、道具和视线方向完整入画`, `视线或运动方向预留空间`, or repeated `固定机位，仅保留轻微呼吸感` unless that sentence is genuinely specific to the shot. Replace filler with the actual subject, body part, prop, product state, effect path, composition, and camera path.

Put keyframe/image-upload instructions in a separate column immediately before `视频内容Prompt（含声音/负面）`, such as `生成前执行说明`. The video Prompt itself should focus on what appears in the picture and sound. Do not clutter the video Prompt with raw execution bookkeeping such as which keyframe image to generate next. However, every image-to-video prompt must include a short model-facing `【关键帧调用】` section near the top of the prompt, stating which uploaded image is the `首帧`, which image(s) are `中间关键帧`, which image is the `结尾帧`, and which state each frame controls. This section is not a production checklist; it is part of the actual video-generation instruction so tools such as SeedDance/LibTV know how to use the uploaded references. When an asset must be visually anchored in the video Prompt, use inline visual tags inside the picture description, for example `贾母@角色_贾母_设定图_预览_v02.png` or `宴会厅@场景_大观园宴会厅全景_预览_v02.png`.

Keyframe image prompts must upload every reference asset needed to preserve continuity, not only the scene. For each shot, include:
- scene/environment reference
- every clearly visible named character reference
- product/prop/effect reference if it appears or affects the action
- for group shots, include the group atmosphere reference plus the main named characters that need continuity in nearby shots; state that individual character references control recognizable foreground/midground roles, while the crowd follows the group atmosphere

Do not leave `特效`, `声音`, or `衔接要求` blank. If a segment has no added VFX, write `特效：无新增特效`. If it is silent, write `声音：无` or state the retained ambience. Do not write scattered raw `引用资产` lines inside the video prompt; put upload/selection bookkeeping in `生成前执行说明`. The video prompt must still contain `【关键帧调用】` and mark visible identity references inline as `人物@文件名`, `背景@文件名`, `场景@文件名`, `产品@文件名`, `道具@文件名`, or `特效@文件名`.

Do not use placeholder wording such as `按本镜头需要选择`, `根据主体动作采用`, `按画面执行`, `保持可识别`, `适当`, or `根据实际情况`. Replace each placeholder with a concrete production instruction. A generated Prompt table is incomplete until every segment passes this field-level check.

Do not satisfy the field check by mechanically repeating the same generic sentence in every segment. Each segment's `构图`, `动作`, `特效`, and `结束状态` must mention the actual character, product, prop, effect path, or scene relationship for that time range. The goal is a production instruction, not a schema-shaped placeholder.

For image-to-video execution, distinguish `首帧Prompt`, `中间关键帧Prompt`, and `结尾帧Prompt`. The first frame is frame 0 before the main action completes; it should not jump to a product reveal, transformation climax, absorption moment, or already-resolved state unless the shot explicitly starts there. The middle keyframe can lock the strongest product/effect/composition reference. The end frame locks the visible result and the handoff to the next shot. These three columns are keyframe status slots, not mandatory image-generation slots: generate only the frames explicitly required by the video action structure and `生成前执行说明`. If a separate middle or end frame is unnecessary, leave that keyframe Prompt cell blank. The skip reason belongs in `生成前执行说明`, not inside the blank keyframe cell.

Prefer a simpler keyframe plan when it will control the video better. For many short shots, use only `首帧` and `结尾帧`, or only `首帧`, and explicitly skip middle keyframes. Do not create `中间关键帧` just because the column exists. If the planned middle frame is visually close to the first or end frame, skip it and describe the motion in `视频内容Prompt（含声音/负面）` instead. Keyframes should represent materially different states, not minor expression, mouth-shape, hand-height, or gaze differences.

Do not spend AI image-generation compute on pure placeholder frames. Pure black, pure white, solid-color, empty fade-in/fade-out, or other no-subject transition frames are not production keyframes. If the edit needs a black screen or solid-color transition, describe it in `视频内容Prompt（含声音/负面）` as `黑场淡入/淡出` or create a deterministic local placeholder only when a downstream tool technically requires an uploaded image. Do not write a `首帧Prompt / 中间关键帧Prompt / 结尾帧Prompt` for a pure-color frame, do not upload it as a keyframe, and do not connect it to LibTV/SeedDance unless the user explicitly approves that workaround.

The correct Prompt workflow is:
1. Read the original script and confirmed execution script.
2. Write the `视频内容Prompt（含声音/负面）` first, including time-coded action, camera movement, sound, end state, asset references, handoff, and a compact `【关键帧调用】` section.
3. Decide the keyframe plan from the video prompt, not from a fixed three-frame template.
4. Write `首帧Prompt`, `中间关键帧Prompt`, and `结尾帧Prompt` only for frames that the keyframe plan requires.
5. If a middle or end frame is not needed, leave that keyframe Prompt cell blank and record the skip in `生成前执行说明`.

Before generating any keyframe image, run a pre-generation necessity review on the written prompts. Compare the planned `首帧 / 中间关键帧 / 结尾帧` text, especially multiple middle-frame blocks in the same cell. If two planned frames differ only by dialogue sentence, mouth shape, tiny eye movement, slight smile strength, or a small fan/hand height change, merge them before image generation. Rewrite the workbook/task list first, then generate only the merged frame. Do not generate both and decide after seeing the results; visual QC after generation is only for checking whether the selected plan was executed correctly.

Keyframe decision criteria:
- `首帧Prompt`: normally required for each independently generated video clip. It may be replaced by `复用上一镜头结尾帧` only when the next shot is a true continuous continuation with the same scene, subject position, camera angle, composition, and action state.
- `中间关键帧Prompt`: default to skip unless there is a meaningful middle state that cannot be controlled by first/end frames alone, such as a materially different product state, transformation midpoint, VFX path, large blocking change, camera-axis change, or a duration usually above 4 seconds with multiple distinct beats.
- Multiple middle keyframes are allowed only when each one has a material visual difference: different shot size, camera axis, subject position, blocking, product state, prop state, effect path, or clearly separate performance beat. Do not generate A/B middle frames merely because two adjacent lines or facial expressions differ slightly. If the difference is only a small mouth shape, tiny eye movement, or similar fan/hand position, merge them into one middle keyframe or skip the middle frame entirely and describe the change in the video prompt.
- `结尾帧Prompt`: generate when the final state is materially different from the first frame, must anchor the video ending, or will become the next shot's reused first frame. Skip it for very short/simple shots where the first frame can naturally animate through the whole clip without a controlled final state.
- Pure black, pure white, solid-color, empty fade-in/fade-out, or no-subject transition frames are not AI keyframes. Do not write image prompts for them and do not spend image-generation compute on them. Express black-screen/fade requirements in `视频内容Prompt（含声音/负面）` or post-production notes instead.
- Do not generate a keyframe only because a worksheet column exists.

Adjacent-shot reuse rule:
- If one continuous action is split into two rows and the previous shot's final visible state is exactly the next shot's starting visible state, generate the image once.
- Prefer generating it as the previous shot's `结尾帧Prompt`, then write the next row's `首帧Prompt` as `复用上一镜头结尾帧：镜头NN_结尾帧_vXX.png`.
- Reuse is allowed only when subject, pose/state, camera angle, shot size, composition, scene geography, and product/prop state are the same. Same location alone is not enough.
- If there is a cut-in, reverse angle, different character, different shot size, new camera axis, new product state, or changed expression/action, do not reuse; write a separate first frame.
- Record the decision in `生成前执行说明` so the producer does not infer it manually.

The final internal workbook should open on the main execution sheet. Keep `内部执行脚本与Prompt表` or `执行脚本与Prompt表` as the first worksheet. Optional `项目说明` can follow after it. Do not include process-only sheets such as `全片连续性设定` or `关键帧决策标准` in the final execution workbook; those rules belong in the skill and generation logic.

The internal workbook must keep separate columns for `参考素材`, `首帧Prompt`, `中间关键帧Prompt`, `结尾帧Prompt`, `生成前执行说明`, and `视频内容Prompt（含声音/负面）`. Do not create a separate `转场衔接要求` column. In `生成前执行说明`, state:
- which keyframe images need to be generated or skipped
- whether the first frame reuses a previous shot's end frame
- which keyframe images and reference assets should be uploaded/selected before video generation
- visual QC requirements after keyframe generation: shot size, composition, action state, seating/spatial continuity, character/product identity, no-text/no-watermark
- any production-only notes that are not useful inside the actual video prompt

Inside `视频内容Prompt（含声音/负面）`, write visual content only: scene, action, camera, composition, effect, sound, end state, transition/handoff, and keyframe-use roles. Include a concise `【关键帧调用】` section before `【画面内容】`, for example:

```text
【关键帧调用】
首帧：镜头03_首帧_v09.png，作为00:00起始状态。
中间关键帧A：镜头03_中间关键帧A_v09.png，控制台词前半段表情和手部位置。
中间关键帧B：镜头03_中间关键帧B_v09.png，控制台词后半段眼神和动作推进。
结尾帧：镜头03_结尾帧_v09.png，锁定镜头结束状态；末段动作收束到该画面。
```

If a frame is skipped, state it briefly, e.g. `中间关键帧：不使用单独中间关键帧，以分镜动作和运镜控制中段。` Use inline asset tags when useful, such as `人物@角色_林黛玉_设定图_预览_v02.png`, `场景@场景_贾母C位座次_预览_v02.png`, `背景@场景_大观园宴会厅全景_预览_v02.png`, `道具@道具_团扇绢帕宴席器物_设定_预览_v02.png`, `产品@官方产品图.png`, `特效@特效_170度环抱送风_关键帧_预览_v02.png`. When a repeated background must stay visually identical across shots, explicitly write `背景@文件名`; do not rely on `场景@文件名` alone, because some video tools treat scene references as loose atmosphere instead of a locked background.

Keyframe visual QC is mandatory after images are generated and before any LibTV/SeedDance video node is connected or run:
- Compare every generated `首帧/中间关键帧/结尾帧` image against its own Prompt, the `视频内容Prompt（含声音/负面）`, and `生成前执行说明`.
- Character consistency is a visual pass, not a filename pass. Writing `人物@角色_林黛玉_设定图_预览_v02.png` in a prompt does not mean the image generator actually used that file as a bound visual reference. Before accepting keyframes, compare the generated face, costume color, hair ornaments, props, and body type against the actual character-setting image. If the current generation tool cannot upload/bind local reference images, say so explicitly and either use a tool/workflow that can bind the image reference, or reduce variation by generating/reusing a single approved standard character keyframe for that character. Never claim that a reference image was used when it was only mentioned in text.
- For visually similar characters, write and enforce a short character bible before generation: fixed costume color, fixed hair ornament color/material, fixed prop, fixed temperament, and an explicit contrast against the similar character. Example: `林黛玉=浅青蓝外衫+淡粉紫内衬+蓝白花钗+团扇+清瘦敏感；薛宝钗=象牙金外衣+金色头饰+不拿团扇+温润端庄`. Recheck repeated shots for clothing drift before marking the image usable.
- Confirm the actual image matches the required shot size. If the Prompt says `结尾中景` but the generated image remains `全景/远景`, the image fails even if it looks good.
- Confirm the actual image matches the action state: first frame is the start, middle frame is the mid-action/performance state, end frame is the final visible state. Do not use a middle-looking image as a first frame or a first-looking image as an end frame.
- Confirm spatial continuity: seating, left/right positions, product state, prop positions, and camera axis must match the continuity map. Same room is not enough.
- Product consistency is stricter than character consistency. When the client has provided official product materials, every visible product must use the real product image/material as the highest-priority reference. Do not let an image model repaint the product body, fake the logo, change proportions, invent screen text, alter the side outlet, or simplify the air-guide structure. Product video can be omitted if the user says so, but official product stills must still be used for product keyframes and video-node references.
- For air-conditioner wide-angle airflow claims such as `170°环抱送风`, verify the geometry before accepting the keyframe: the air conditioner is the vertex/source, two straight boundary lines extend directly from the unit to form the angle, and any `170°` label belongs near the product-side vertex rather than floating on the far arc. Avoid the misleading pattern where airflow first exits as a curved narrow stream and only then opens into a fan, because it does not show large-angle outlet delivery.
- Confirm image hygiene: no captions, no labels, no UI, no watermark, no garbled text, no unintended logo/screen text.
- If an image fails visual QC, do not connect it to a video node. Regenerate the image first, update the filename/version in `生成前执行说明` and `【关键帧调用】`, then continue.

When a shot changes shot size across time, keyframe prompts must say the target shot size negatively and positively. Example: `结尾帧必须是贾母与C位空座的中景/中近景，不是全宴席全景；不要保留完整圆桌和整间大厅。` This prevents the model from copying a full-view first frame into a closer end frame.

Video-generation prompts must not ask the video tool to generate music, BGM, underscore, score, or background music. AI video music is usually uncontrollable and discontinuous. Only write dialogue/voiceover, action sound effects, product sound effects, ambience, foley, and clean audio boundaries. If the source script contains music notes such as `古筝琵琶合奏`, keep them as post-production music guidance outside the actual video prompt, or rewrite the video prompt as `不生成音乐/BGM，音乐后期单独配`.

Use the column title `首帧Prompt`; do not use `真正首帧Prompt`.

Prompt execution tables must include `原始脚本内容` next to the execution version. Summarize the original shot's 景别、画面、时长、台词/旁白、音效/音乐、备注 and any later user modification instructions. This prevents hallucinated execution changes and lets the user compare original requirements with the final execution prompt.

For generated keyframe image files, use a stable flat naming rule under `05_内部制作执行/01_首帧与关键帧/`:
- `镜头{NN}_首帧_v01.png`
- `镜头{NN}_中间关键帧_v01.png`
- `镜头{NN}_中间关键帧A_v01.png`, `镜头{NN}_中间关键帧B_v01.png` when a long dialogue, camera switch, jump cut, or multi-beat performance needs multiple middle references
- `镜头{NN}_结尾帧_v01.png`

If one workbook cell contains multiple keyframe blocks or multiple `输出文件名：...` entries, split them into separate image-generation tasks before calling any image tool. Never submit the whole cell as one prompt, because it will often produce a contact-sheet/collage instead of a single usable production frame. Each generated file must correspond to exactly one frame role and one output filename.

If a separate keyframe is not generated because it reuses another frame, record that explicitly in the workbook or a local prompt task file; do not leave a silent gap in the expected filenames.

When generating keyframe images from a workbook, do not iterate blindly over `首帧Prompt / 中间关键帧Prompt / 结尾帧Prompt`. First read `视频内容Prompt（含声音/负面）` and build an active keyframe list:
- Use `生成前执行说明` as the source of truth for which keyframe images to generate.
- If `生成前执行说明` says `中间关键帧=不生成`, the `中间关键帧Prompt` cell must be blank and must be skipped.
- If `生成前执行说明` says `结尾帧=不生成`, the `结尾帧Prompt` cell must be blank and must be skipped.
- If a planned frame is only pure black, pure white, a solid color, or an empty fade transition, remove it from the active keyframe list. Keep the transition instruction inside the video prompt or post-production note instead of generating a PNG with AI.
- If the workbook and video prompt disagree, fix the workbook before generating images.
- Before connecting a locally generated keyframe to LibTV/SeedDance, confirm the image is at least 2K on the short side when possible, and for confirmed `9:16竖屏` production work prefer a `2160x3840` or larger PNG. If the image tool returns a smaller approved image, create a high-quality `_4K.png` production copy and connect that copy instead of the low-resolution original.

Do not leave browser-upload helper files inside the formal keyframe folder. Temporary reference copies such as `_upload_refs_*` are allowed only while operating the browser; after generation, keep the official output images and the workbook, then move temporary helper copies to an internal cleanup/temporary area or remove them after user confirmation. Formal `01_首帧与关键帧/` should contain current keyframe images and, if needed, one concise generation checklist, not dozens of upload-copy folders.

When a user approves a prompt-writing reference,固化 means two things: update `references/prompt_standard.md` and update any prompt-generation script that creates Excel output. Do not rely on a one-off sample workbook as the standard. The generated `完整生成Prompt` must follow the reference creator's second-by-second logic: each important time range has a clear action, camera, composition, effect path, sound boundary, and end state.

Before delivering any internal execution Prompt workbook, run `scripts/validate_prompt_detail.py`. If it reports missing fields or placeholder wording, fix the workbook before delivery.

For one-take appearance / transformation / product-generation shots, use staged time blocks such as `00:00-00:02 · 显化` with `动作 / 镜头 / 特效 / 声音`. For cuttable or multi-beat shots, use `分镜一：00:00-00:02 景别...机位...构图...运镜手法...画面内容...`. Choose the structure based on the shot, not a fixed template.
