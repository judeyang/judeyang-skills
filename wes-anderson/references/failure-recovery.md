# Failure Modes And Recovery

Use these branches instead of guessing or silently continuing.

- If the client script has no recognizable shot table, then create a `资料解析问题确认表.xlsx` or a sheet in the audit workbook that lists the missing columns, the source filename, and the exact fields needed: `镜号`, `景别`, `画面内容`, `时长`, `台词/旁白`, `音效/音乐`, `备注`.
- If the script is pasted text rather than a spreadsheet, then first convert it into a shot table with stable shot numbers, preserve the original pasted text in an archive/source sheet, and mark uncertain segmentation as `待确认`.
- If shot duration is missing, then keep the shot, mark `时长=待确认`, and flag duration-sensitive risks instead of inventing seconds.
- If dialogue is too long for the stated duration, then write a client-facing choice: shorten dialogue, extend duration, or move content to voiceover. Do not silently rewrite approved dialogue.
- If official product images, logo, font authorization, brand rules, music, or voiceover references are missing, then mark each item as `待提供` in client-facing sheets and block final product-accurate prompts until provided.
- If the user asks to generate product visuals without official product references, then create placeholder direction only and state that official assets override all generated imagery.
- If the client confirmation workbook has not passed the second AI review, then fix or flag duration, dialogue, continuity, product logic, asset needs, and generation feasibility before prompt generation.
- If an approved prompt reference conflicts with `references/prompt_standard.md`, then ask whether to固化 the reference. If approved, update both `references/prompt_standard.md` and the relevant prompt-building script; otherwise apply it only to the current workbook.
- If a client changes a confirmed visual after preview/sample generation, then record sample version, affected shots/assets, affected duration, reason, rework action, and status before updating downstream prompts or assets.
- If a generated workbook cannot be validated manually, then open it with a spreadsheet library, verify worksheet names, first-row headers, required columns, file path, and row count before telling the user it is complete.
