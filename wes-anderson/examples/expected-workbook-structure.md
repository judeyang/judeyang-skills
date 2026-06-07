# Expected Workbook Structure

## Client Confirmation Workbook

First two sheets:

1. `脚本审核确认表`
2. `形象场景描述确认表`

Required behavior:

- Preserve original shot numbers and include every original shot.
- Mark missing official product image, logo, font, music, and brand material as `待提供`.
- Include picture-ratio confirmation before prompt generation.
- Use client-facing wording only; do not expose internal Prompt production instructions.

## Internal Asset Production Workbook

Location: `05_内部制作执行/设定资产制作表_v01.xlsx`

Required behavior:

- Include asset category, asset name, source shot range, source summary, visual direction, prompt type, full prompt, output filename, finished asset path, status, and notes.
- Treat this as producer-facing, not client-facing.

## Internal Prompt Workbook

Location: `05_内部制作执行/内部执行脚本与Prompt表_v01.xlsx`

Required behavior:

- Preserve source script content next to execution content.
- Include first-frame/keyframe planning and video prompts only after client confirmation.
- Run prompt-detail validation before delivery.
