# Shot Designer

`Shot Designer` is an Agent Skill for AI video production. It turns approved scripts, visual assets, and reference images into executable video-generation prompts.

It focuses on:

- per-shot prompts for Seedance, LibTV, and similar video tools
- first-frame, end-frame, and middle-keyframe planning
- character, scene, product, prop, and effect reference binding
- suppressing BGM while keeping dialogue, sync sound, foley, and product sound
- a three-part video prompt contract: `【基础设定】`, `【氛围与画质】`, `【画面内容】`
- time-coded shot control: shot size, camera position, composition, camera movement, visual content, effects, sound, end state, and transition requirements

## Output Contract

Final video prompts must use these exact top-level headings:

```text
【基础设定】
【氛围与画质】
【画面内容】
```

Every time-coded block must include:

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

## Scripts

Create an internal asset prompt workbook:

```bash
python scripts/build_asset_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Create a blank internal execution and prompt workbook:

```bash
python scripts/build_prompt_table.py \
  --input "/path/to/项目名_脚本与资产确认表_v01.xlsx" \
  --project-dir "/path/to/项目交付文件夹"
```

Validate a completed prompt workbook:

```bash
python scripts/validate_prompt_detail.py --input "/path/to/内部执行脚本与Prompt表_v01.xlsx"
```

## Quality Boundaries

- Do not generate BGM.
- Do not use `核心主题`, `运镜规则`, `关键帧调用`, `声音/台词`, or `负面要求` as standalone video prompt headings.
- Do not put style words inside `景别`.
- Do not put camera-position words inside `构图`.
- Product logo, official screen text, face identity, hands, and key props take priority over decorative effects.
