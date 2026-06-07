# Wes Anderson Delivery Rules

This reference holds detailed delivery rules that are too specific for the top-level `SKILL.md`. Load it when creating filenames, writing client-facing workbooks, preparing final archives, or reviewing whether a downstream step is allowed.

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
- `归档_客户最终确认_v01.pdf`
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
- Do not treat preview character, scene, product, prop, or effect images as approved production assets before they are referenced back in the client confirmation workbook and confirmed.
- Do not ask the client to confirm storyboards unless explicitly required.
- Do not use AI-generated product appearance as final brand reference; official product assets override prompts.
- Do not put internal image/video prompts in client-facing sheets; prompts belong in `设定资产制作表` or `内部执行脚本与Prompt表`.
- Do not create a separate `02_视频Prompt` folder; the prompt workbook belongs directly under `05_内部制作执行/`.
- Do not create a separate top-level `03_执行版脚本/` folder or standalone `执行版脚本.xlsx` unless explicitly requested.
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
