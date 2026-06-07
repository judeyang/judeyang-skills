# Project Folder Standard

Do not make the folder template too rigid. First read and understand the script, extract likely asset categories, then create project-specific asset subfolders.

Keep first-level folders stable:

```text
项目文件夹/
  00_项目说明_文件夹与命名规则.md
  01_客户原始资料/
    01_脚本/
    02_产品素材/
    03_用户反馈参考图/        # only when feedback/reference images exist
    04_品牌素材/              # only when provided
    05_字体授权/              # only when provided
  02_用户确认文件/
  03_设定资产/
  04_最终确认归档/
  05_内部制作执行/
    01_首帧与关键帧/
    02_视频片段/
    03_成片/
    04_封面/
```

Do not create a separate first-level `03_执行版脚本/` directory. If a confirmed text execution script is needed, keep it in `02_用户确认文件/` when it is user-facing, or keep the execution layer inside the internal workbook in `05_内部制作执行/`.

Do not create empty placeholder folders. Create optional folders such as `03_用户反馈参考图/`, `04_品牌素材/`, `05_字体授权/`, or `05_内部制作执行/04_封面/` only when the project actually has those materials or deliverables.

Do not create a generic `提示词参考` folder in the project structure. If a user provides a prompt reference file, use it to update the skill or prompt standard when appropriate, then archive the source only if the user explicitly wants to keep it.

Create subfolders under `03_设定资产/` according to the actual script. Do not hardcode project-specific names such as `产品与法器设定` in the generic template. Product source materials belong under `01_客户原始资料/02_产品素材`; generated product-effect keyframes can go under a project-specific asset folder only when needed.

Examples:

```text
西游/神话项目:
  03_设定资产/
    01_人物设定图/
    02_场景设定图/
    03_道具设定图/
    04_特效关键帧/

汽车广告:
  03_设定资产/
    01_车型外观参考/
    02_场景设定图/
    03_驾驶员形象/
    04_动态特效关键帧/

美妆广告:
  03_设定资产/
    01_人物模特设定/
    02_产品质感参考/
    03_场景氛围图/
    04_质地特效关键帧/
```

Use `scripts/create_project.py` to scaffold the stable structure and create the initial confirmation workbook. If asset categories are already known, pass them with `--asset-subfolders`.

Example:

```bash
python scripts/create_project.py \
  --project-name "海尔空调西游记AI短剧" \
  --base-dir "/path/to/output-root" \
  --asset-subfolders "人物设定图,场景设定图,道具设定图,特效关键帧"
```
