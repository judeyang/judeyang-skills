# Client-Facing Document Standard

Use this standard for client confirmation Excel files, final confirmation PDFs, and user-facing
project archives.

## Purpose

Client-facing documents should state:
- what has been confirmed
- what materials have been received
- what materials are still needed
- what direction will guide subsequent production
- what later adjustments need to be recorded for mutual confirmation

They should not expose internal production mechanics.

## Blocked Wording

Do not include:
- internal Prompt or prompt-table references
- internal statistics, costing, settlement, billing, workload, or pricing language
- automatic review, rule scanning, machine judgment, or validator language
- internal folder creation, file sorting, version migration, or tool-operation descriptions
- wording that blames the client, such as wasted effort or invalidated seconds
- AI implementation disclaimers such as `AI自由生成结果`

## Preferred Replacements

- `建立项目文件夹并生成首轮确认表` -> `完成原始脚本梳理并提交首轮确认内容`
- `整理为用户已确认版本` -> `确认脚本与形象场景方向`
- `空白项按默认无意见处理` -> `未提出调整的内容按当前方案执行`
- `制作口径` -> `后续制作依据`
- `不以AI自由生成结果为准` -> `均以贵方提供的官方素材为准`
- `记录对应影响范围` -> `同步记录对应调整范围，便于双方沟通确认`

## Material Status

Before rendering a final PDF, scan the project material folders. Do not list product images as
`待提供` when product images or videos are already present. List only genuinely missing client
materials.

## Validation

Generate a plain-text manifest containing every customer-visible sentence. Run
`scripts/validate_client_facing_text.py` before PDF delivery. Block delivery on hard-rule matches.
