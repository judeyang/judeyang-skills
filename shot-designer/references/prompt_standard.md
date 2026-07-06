# Internal Shot Prompt Standard

Use this structure in the final `内部执行脚本与Prompt表.xlsx`.

One row = one shot. Keep execution logistics and actual video prompt separate:
- `生成前执行说明`: what to generate/upload/select before video generation.
- `视频内容Prompt（含声音/负面）`: the model-facing director prompt.

Scripts may create workbook scaffolds, extract facts, and validate structure. Scripts must not generate final prompt prose.

## Seedance-Fit Principle

Seedance 2.0 is a multimodal video model. Public first-party/partner documentation describes text-to-video and image-to-video workflows where text controls scene, movement, and rhythm, and where uploaded image/video/audio references can constrain the generation. Therefore prompts should read like a compact director brief:
- state what each reference controls
- describe visible subjects, environment, action, camera, and constraints
- split important action into time ranges
- keep music/BGM out of the generation prompt; the tool should generate only dialogue, room tone, foley, action sound, and product sound

Do not use the old long heading stack (`核心主题`, standalone `运镜规则`, standalone `声音/台词`, standalone `负面要求`) as the default video prompt. The production prompt now has three major sections only.

## Video Prompt Template

This is an output contract, not a loose suggestion. Final video prompts must use exactly these three top-level headings and no alternate top-level headings.

```text
【基础设定】
镜头任务：用一句话写清本镜头要完成什么，不写空泛宣传语。
参考素材：人物@文件名控制脸、服装和体态；背景@文件名锁定可见空间；产品@文件名锁定外观、Logo、结构；首帧@文件名作为00:00起始状态；结尾帧@文件名锁定结束状态。没有上传的素材不得写成已使用。
人物/产品/道具/场景：写本镜头实际可见或必须保持连续的设定。只写会影响画面的事实。
连续性：写空间轴线、左右关系、座次/站位、产品状态、上一镜头/下一镜头交接。不可用泛泛的“保持连续性”。
声音：只生成对白、同期环境声、动作音效、产品音效或房间底噪；台词按情绪使用自然停顿、重音、尾音和气息控制；不需要配乐，不生成BGM，音乐后期单独配。
文字策略：默认画面为无文字纯图片。禁止生成字幕、标题、角标、水印、说明文字、乱码、伪Logo、排版边框和UI界面。产品镜头仅保留官方素材中已有的品牌Logo和官方屏显信息，禁止新增文字、伪Logo或屏幕文案。剧情道具镜头如报纸、信件、招牌必须出现文字，只允许少量大字或可后期替换的占位文字，禁止复杂小字和乱码。非产品镜头也必须写本行，不得只在最后一个分镜里补一句“不加字幕”。

【氛围与画质】
风格核心：写影片风格、类型质感、真实感目标和表演边界。真人/实拍类镜头默认优先使用这组真实感锚点：电影级质感、超写实、极致逼真、Photorealism、真人实景拍摄；再补充本片类型风格，并写清杜绝游戏CG感、杜绝动作僵硬。不要写错为 `Photirealism`。
视觉基调：写摄影机/镜头/画幅/景深/运动稳定性/可剪辑性，例如 IMAX 胶片摄影机质感、Panavision C 系列镜头、主体清晰、运动处保留轻微动态模糊。
色彩与影调：写色彩、光源、对比、颗粒、明暗细节和商业画面干净度，例如低饱和复古胶片、高光不过曝、暗部保留细节。
质量边界：只写与本镜头相关的短负面清单，通常 3-6 项，不超过 8 项；例如人物表演镜头写避免低清、塑料皮肤、脸部漂移、畸形手指、动作僵硬；产品镜头写避免产品变形、Logo错误、伪UI、过曝、低清。不要整片复制同一串负面词。

【画面内容】
分镜一：00:00-00:02
景别：
机位：
构图：
运镜手法：
画面内容：写主体、动作、动作原因、动作效果、表情/身体部位/道具/产品状态。不要只写命令，要写清为什么发生和最终要给观众看到什么。
特效：
声音：
结束状态：
衔接要求：

分镜二：00:02-00:05
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

Forbidden alternate top-level headings:
- `【视频类型】`
- `【产品一致性 / Logo / 屏显文字策略】`
- `【三段式结构 / 逐秒分镜】`
- `【声音要求】`
- `第一段 / 第二段 / 第三段` as top-level structure

Those facts must be merged into `【基础设定】`, `【氛围与画质】`, or the time-coded blocks inside `【画面内容】`.

Mandatory base labels:
- `镜头任务：`
- `参考素材：`
- `人物/产品/道具/场景：`
- `连续性：`
- `声音：`
- `文字策略：`

## What Goes Where

`【基础设定】` contains stable facts and reference binding:
- shot task
- reference image descriptions and roles
- character, product, prop, scene facts
- continuity, blocking, left/right, product state
- sound boundary and dialogue/foley limits
- text strategy, no-subtitle/no-watermark boundary, and product/logo/story-prop exceptions

`【氛围与画质】` contains quality control:
- `风格核心`
- `视觉基调`
- `色彩与影调`
- commercial cleanliness and visual negative constraints

`【画面内容】` contains all shot execution:
- time ranges
- shot size
- camera angle
- composition
- camera movement
- action/story effect
- VFX
- per-beat sound
- end state
- transition/handoff

Do not create a separate `【运镜规则】`. Put camera path, movement speed, focus behavior, axis rules, and allowed/forbidden cuts in each time block's `运镜手法：` and `衔接要求：`.

Do not create a separate `【声音/台词】`. Put global sound limits in `【基础设定】`, and put per-beat dialogue/foley in `【画面内容】` under `声音：`. Spoken lines must use `{完整原文台词}` when dialogue exists, and key sound effects can use `<音效>` when useful.

For dialogue, read `references/voice_dialogue_rules.md` before writing the final prompt. Use punctuation and delivery notes to control speech:
- `，` = short natural pause
- `。` = closed ending or restrained emotion
- `！` = emphasis or emotional lift
- `？` = doubt, trial, or rising tail tone
- `？！` = challenge, disbelief, or burst
- `……` = emotional blockage or hesitation
- `~` = soft, light, intimate tail tone
- `--` = sudden turn, interruption, or self-correction

Write the complete spoken line and the delivery together. The text inside `{}` is source-locked by default:

```text
声音：角色压低声音说{别动。再往前一步，我就不客气了。}，两个句号都收住，`再往前一步` 放慢重读；保留轻微脚步声和衣料摩擦声。
```

If the dialogue is client-confirmed or the user says `一字不改`, `原文保留`, `不得修改`, `照抄`, or `法务确认`, preserve every character and punctuation mark inside `{}`. Add delivery guidance outside `{}`; do not add ellipses, split, paraphrase, shorten, or rewrite the line. If a separate performance version is explicitly allowed, keep the original line and label the variant separately.

Dialogue punctuation controls audio only. Never put `{台词}` into visible subtitles, screen text, prop text, captions, UI labels, or watermarks.

If a dialogue shot is split into multiple time-coded blocks, every block's `声音：` must state one of:
- the complete spoken line in `{}` when the line is delivered in that block
- an exact source fragment in `{}` plus clear continuation wording when the source line is intentionally split for timing
- `无新台词` when only breath, reaction sound, room tone, foley, or tail-tone continuation remains

Do not create a separate `【负面要求】` by default. Put text strategy and product/logo/story-prop limits in `【基础设定】`; put visual-quality negatives in `【氛围与画质】`; put action-specific forbidden behavior in the relevant `画面内容` beat.

## Keyframe And Reference Policy

Keyframe columns are status slots, not obligations.

Default approach:
- `首帧Prompt`: usually required for independently generated clips
- `结尾帧Prompt`: generate when the final state is materially different or must hand off to the next shot
- `中间关键帧Prompt`: skip by default; generate only for a materially different middle state

Do not create image prompts for pure black, pure white, solid-color, fade-only, or no-subject transition frames. Express those as video/post-production instructions.

The video prompt must still say which references are actually used, but inside `【基础设定】`, not as a standalone `【关键帧调用】` heading:

```text
参考素材：首帧@镜头03_首帧_v02.png作为00:00起始状态；中间关键帧不使用，以分镜动作和运镜控制中段；结尾帧@镜头03_结尾帧_v02.png锁定镜头结束状态。
```

If one continuous action is split into two rows and the previous shot's final visible state exactly equals the next shot's starting state, generate the image once:

```text
参考素材：首帧复用上一镜头结尾帧@镜头02_结尾帧_v02.png，作为00:00起始状态。
```

Reuse is allowed only when subject, pose/state, camera angle, shot size, composition, scene geography, and product/prop state are the same.

## Time-Coded Shot Segments

Every time-coded segment must contain these labels:

```text
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

Use `特效：无新增特效` when no effect is needed. Use `声音：无` or a specific sound boundary when silent. Do not omit fields.

For shots longer than 2 seconds, product entrances, transformations, VFX transitions, fights, camera moves with dialogue, or before/after state changes, split into clear time ranges.

For a simple 1-2 second shot, one segment is enough.

## Effect Visibility Policy

Product and story effects must be controlled, not invisible:
- write effect material, path, density, start state, end state, and what it must not obscure
- product, logo, official screen, face, hand, and key prop visibility outrank decorative effects
- product ads should use clean effects such as transparent airflow, soft light trace, fine particles, glass reflection, water vapor, or restrained energy lines
- avoid both extremes: no vague `高级气流` that is invisible, and no dense smoke/light that covers product structure or official text

Examples:
- Weak: `特效：轻微气流。`
- Better: `特效：透明清洁气流从出风口向顾客手部延展，密度低、边缘柔和，不遮挡Logo、官方屏显和出风口结构。`

## Shot Field Discipline

Do not mix style, camera position, composition, and movement:
- `景别` only describes shot size, such as `大全景`、`全景`、`中景`、`中近景`、`近景`、`特写`、`大特写`. Do not write `电影感`、`史诗感`、`高级感` as shot size.
- `机位` describes camera position/angle/height, such as `无人机高空俯拍`、`低机位仰拍`、`平视正面30度`、`贴地低角度`.
- `构图` describes frame layout, visual hierarchy, foreground/midground/background, guide lines, subject placement, and negative space.
- `运镜手法` describes camera movement and rhythm, such as fixed shot, push-in, follow shot, pan, tilt, orbit, handheld, drone follow, and whether cuts are allowed.

Corrected example:

```text
景别：史诗级大全景。
机位：无人机高空俯拍。
构图：笔直公路作为引导线从画面下方延伸到远处，机器人和鸵鸟位于街道中央，废墟城市占据背景。
运镜手法：无人机保持高空跟随主体前进，镜头位置稳定，末段轻微上摇扩大城市废墟视野。
```

## Whole-Film Continuity Pass

Before writing shot prompts, read the full approved execution script from start to finish and produce a continuity note. This is mandatory for recurring scenes and character relationship scenes.

The continuity note should answer:
- stable scene geography
- camera axis
- important seats, props, products, doors, windows, light sources, or airflow sources
- character standing/seating relationships
- left/right relationships from the viewer's perspective
- object or product state changes over time
- shots that intentionally break axis or change position

Put only the relevant, concise continuity facts into each affected prompt under `【基础设定】`.

## Failure Modes

| Failure mode | Fix before delivery |
|---|---|
| `参考素材` says an image is uploaded but the file does not exist | Rewrite as `待提供` or `待生成`; only use `人物@/背景@/产品@/首帧@` for actual files. |
| Official product material is missing | Do not invent product details; ask for official reference or mark product prompt blocked. |
| Music/BGM appears in the model-facing video prompt | Remove it. The video prompt must say `不需要配乐，不生成BGM，音乐后期单独配。` |
| A story prop needs visible text | Use `文字策略` to allow only minimal large story text or post-production replacement; still forbid subtitles, watermarks, garbled text, and random labels. |
| `景别` contains style words such as `电影感` | Move style words to `风格核心`; keep shot size in `景别`. |
| `构图` contains camera position such as `无人机俯拍` | Move camera position to `机位`; keep layout and visual hierarchy in `构图`. |
| Quality boundary has too many negatives | Keep only shot-relevant negatives, normally 3-6 and never more than 8. Move any user-required extra blacklist to `生成前执行说明`, not the model-facing prompt. |
| Middle/end keyframe is skipped but the cell contains a prompt | Blank the skipped keyframe cell and state the skip in `生成前执行说明` and `【基础设定】`. |
| Generated keyframe fails identity, product, shot-size, text, or continuity QC | Do not use it in video generation; regenerate or revise the frame prompt. |

## Negative Requirement Policy

Negative requirements can help precision when they are specific and placed near the dimension they control. They can hurt commercial image quality when they dominate the prompt, conflict with positive direction, or make the model attend to unwanted visual concepts.

Use this rule:
- Write the desired positive result first.
- Use short, concrete negatives only after the positive target, normally 3-6 items and no more than 8.
- Do not put broad negatives in `镜头任务`.
- Do not list irrelevant negatives from other shots.
- Avoid taboo/dirty/horror words. Use them only when the confirmed shot visibly requires those textures.

Examples:
- Good in `【氛围与画质】`: `超写实真人实景拍摄，商业广告级干净画面；避免低清、塑料皮肤、脸部漂移、产品变形、Logo错误。`
- Bad in `镜头任务`: `不要低清不要变形不要字幕不要乱七八糟。`

## Product Rules

If a real product is involved:
- official product references override prompt imagination
- put product filenames in `【基础设定】` reference binding
- state that product shape, logo, screen text, outlet, proportions, and material must not change
- only official existing logo/screen text may remain
- if accurate product screen text cannot be guaranteed by generation, generate a clean image and add exact text in post-production

## Story Text Rules

Default output is no-text. Allow visible text only when it is part of the confirmed product material or a story-critical prop:
- product logo / official screen: keep only what exists in official client assets
- newspaper / letter / sign / packaging: allow only the minimum visible text needed for the story
- subtitles / UI captions / watermarks / random labels: always forbidden
- complex body copy, small paragraphs, and exact long text should be added in post-production

## Text In Reference Images

Reference images containing labels, notes, title text, subtitles, watermarks, UI panels, or layout borders can contaminate generation. Prefer clean `无文字` image-only references for characters, scenes, first frames, middle keyframes, and end frames.

When a setting sheet with text is already approved, create a separate generation-reference export named like:

```text
角色_林黛玉_视频生成参考版_无文字_v01.png
场景_大观园宴会厅_视频生成参考版_无文字_v01.png
```

Use the clean version in production prompts while keeping the original confirmed sheet in the archive.

## Dialogue Timing

Keep prompt dialogue aligned with duration:
- 1-2 seconds: only a reaction word or short line
- 3 seconds: one short line
- 4 seconds: one clean product line
- longer explanation requires longer shot or voiceover

Match delivery to emotion:
- 撒娇：question/soft-tail feel, light volume, gentle rising tail.
- 警告：short closed sentences, lower voice, slower key words.
- 思考：comma/ellipsis/question rhythm, audible hesitation.
- 愤怒：short lines, challenge or burst, sudden emphasis.
- 难过：ellipsis plus closed ending, weaker breath, falling tail.
- 开心：brighter tone, quicker rhythm, light tail.
- 紧张：unstable pause, hollow breath, uncertain question tail.
- 怀疑：slower front half, key words stressed, scrutinizing question.
- 安慰：front half softer, back half steadier, tail tone lands gently.
- 失望：lighter voice, slower speed, no crying or explosion, tail sinks.
- 舍不得：pre-speech pause, very light voice, unstable breath, hollow tail.
- 反派掌控：lower voice, very slow speed, clear pause, downward tail, restrained contempt.
- 惊讶：brief stunned pause, then higher brighter voice, rising tail, believable disbelief.

For important dialogue, use this compact formula inside each time-coded `声音：` field:

```text
人物在【场景】里，因为【原因/人物状态】情绪发生变化，声音【变轻/压低/变亮/变稳】，语速【变慢/变快/一字一句】，在【停顿位置】停顿，把【关键词】加重，尾音【发虚/上扬/下压/放柔/稳稳落下】地说：【台词】
```

## Forbidden Placeholder Wording

```text
按本镜头需要选择
根据主体动作采用
按画面执行
保持可识别
适当
根据实际情况
围绕本段动作组织画面
关键人物、手部动作、道具和视线方向完整入画
视线或运动方向预留空间
按9:16竖屏组织前景、中景、背景层次
固定机位，仅保留轻微呼吸感
只生成只保留
```

Replace placeholders with concrete subjects, body parts, prop/product states, composition, camera path, and visible end states.

## Final Self-Audit

Before delivery, each prompt must answer:
- what this shot visually accomplishes
- which references are actually used and what they control
- what stays continuous from previous/next shots
- what happens in each time range
- where the subject sits in frame
- how the camera moves
- what the audience hears
- what visible state the shot ends on
- which exact visual defects are forbidden

If the text still reads like a reusable template, it is not finished.
