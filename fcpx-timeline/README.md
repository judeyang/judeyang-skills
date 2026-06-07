# FCPX Timeline

[English](#english) | [中文](#中文)

![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-28a6a6)
![Output](https://img.shields.io/badge/Output-FCPXML-14213d)
![Platform](https://img.shields.io/badge/Platform-macOS%20%2B%20Final%20Cut%20Pro-eef7f7)

## 中文

把本地视频、照片、Live Photo 按拍摄时间生成 Final Cut Pro 可导入的 FCPXML 时间线。

### 适用场景

- 手机、相机、AirDrop 或云盘导出的混乱素材文件夹
- 需要按拍摄时间快速生成粗剪时间线
- 需要处理照片、视频、Live Photo 混合素材

### 使用

```bash
python3 scripts/make_timeline.py "/path/to/media-folder" \
  --out "/path/to/output-folder/timeline.fcpxml" \
  --photo-duration 2 \
  --convert-stills \
  --manifest "/path/to/output-folder/timeline_manifest.json"
```

导入 Final Cut Pro 时，保持原始媒体文件夹和 `timeline_stills/` 可访问。

### 校验与回归

- `test-prompts.json`：覆盖混合素材、Final Cut 导入失败定位、缺少元数据工具。
- `examples/`：包含示例 manifest 和期望时间线行为。
- `scripts/validate-fcpxml.py`：检查 FCPXML 结构和帧边界。

```bash
python3 scripts/validate-fcpxml.py "/path/to/output-folder/timeline.fcpxml" --fps 30
```

## English

Create a Final Cut Pro XML timeline from local videos, photos, and Live Photos, sorted by capture time.

### Use Cases

- Messy media folders exported from phones, cameras, AirDrop, or cloud drives
- First-pass timeline assembly in capture order
- Mixed video, photo, and Live Photo workflows

### Usage

```bash
python3 scripts/make_timeline.py "/path/to/media-folder" \
  --out "/path/to/output-folder/timeline.fcpxml" \
  --photo-duration 2 \
  --convert-stills \
  --manifest "/path/to/output-folder/timeline_manifest.json"
```

Keep the original media folder and `timeline_stills/` available when importing into Final Cut Pro.

### Validation And Regression

- `test-prompts.json`: covers mixed media, Final Cut import failure diagnosis, and missing metadata tools.
- `examples/`: contains a sample manifest and expected timeline behavior.
- `scripts/validate-fcpxml.py`: checks FCPXML structure and frame boundaries.

```bash
python3 scripts/validate-fcpxml.py "/path/to/output-folder/timeline.fcpxml" --fps 30
```

## Structure

```text
fcpx-timeline/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── examples/
│   ├── expected-timeline-notes.md
│   └── sample-media-manifest.json
├── scripts/
│   ├── make_timeline.py
│   └── validate-fcpxml.py
└── test-prompts.json
```

## License

MIT License. See the repository root [LICENSE](../LICENSE).
