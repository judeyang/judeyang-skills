---
name: fcpx-timeline
description: Use when the user wants to turn a local folder of Mac media files into a chronological Final Cut Pro timeline/FCPXML. Handles videos, JPG/PNG/HEIC photos, Live Photo still+video pairs, capture-time sorting, still-image JPEG conversion for FCP compatibility, and frame-boundary-safe durations.
---

# FCPX Timeline

## Purpose

Create a Final Cut Pro XML timeline from one local media folder, sorted by capture time. Use the bundled script instead of hand-writing FCPXML.

## Default Workflow

1. Confirm or infer the source media folder path.
2. Generate the full timeline with still conversion:

```bash
python3 scripts/make_timeline.py "/path/to/media-folder" \
  --out "/path/to/output-folder/timeline.fcpxml" \
  --photo-duration 2 \
  --convert-stills \
  --manifest "/path/to/output-folder/timeline_manifest.json"
```

3. Tell the user to import `timeline.fcpxml` into Final Cut Pro.
4. Mention that converted stills live next to the XML in `timeline_stills/`; the folder must stay available for FCP relinking/import.
5. Run `scripts/validate-fcpxml.py` before delivery when the XML exists locally.

## Rules Encoded In The Script

- Videos: `.mov`, `.mp4`, `.m4v`; placed in the timeline by capture time.
- Photos: `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`; placed as 2-second placeholders by default.
- Live Photos: when a still and video pair is detected, use only the video part and skip the still.
- HEIC/HEIF without a matching Live Photo video is treated as a photo.
- Capture time priority: embedded EXIF/QuickTime/XMP metadata first; file creation/modification time as fallback.
- Static images are copied or converted to JPEG under `timeline_stills/` when `--convert-stills` is used.
- Clip durations and offsets are aligned to the selected timeline frame rate, default `--fps 30`, to avoid FCP frame-boundary warnings.

## Required Tools

Python 3 is required. For accurate metadata and video duration, ensure these are installed:

```bash
brew install exiftool ffmpeg
```

The script also uses macOS `sips` for image conversion when `--convert-stills` is enabled.

## Validation

First run the bundled structural and frame-boundary validator:

```bash
python3 scripts/validate-fcpxml.py "/path/to/output-folder/timeline.fcpxml" --fps 30
```

After generation, validate the XML if Final Cut Pro is installed:

```bash
cp "/Applications/Final Cut Pro.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/FCPXMLv1_10.dtd" /tmp/FCPXMLv1_10.dtd
xmllint --noout --dtdvalid /tmp/FCPXMLv1_10.dtd "/path/to/output-folder/timeline.fcpxml"
```

Also check frame boundaries if the user reports warnings:

```bash
python3 - <<'PY'
from fractions import Fraction
from pathlib import Path
import re
p = Path("/path/to/output-folder/timeline.fcpxml")
for m in re.finditer(r'(duration|offset|start|tcStart)="([^"]+)"', p.read_text()):
    val = m.group(2)
    if not val.endswith("s"):
        continue
    raw = val[:-1]
    f = Fraction(raw) if "/" in raw else Fraction(int(raw), 1)
    frames = f / Fraction(1, 30)
    if frames.denominator != 1:
        print("not frame boundary", m.group(1), val, "frames=", frames)
PY
```

Regression resources:

- `examples/`: sample manifest and expected timeline behavior.
- `test-prompts.json`: Darwin/人工评估 prompts for mixed media, FCP import rejection, and missing metadata tools.

## Troubleshooting Outputs

If Final Cut Pro rejects the full timeline, generate narrow test files:

```bash
python3 scripts/make_timeline.py "/path/to/media-folder" \
  --out "/path/to/output-folder/timeline_video_only.fcpxml" \
  --video-only \
  --manifest "/path/to/output-folder/timeline_video_only_manifest.json"
```

```bash
python3 scripts/make_timeline.py "/path/to/media-folder" \
  --out "/path/to/output-folder/timeline_photos_only.fcpxml" \
  --photos-only \
  --convert-stills \
  --manifest "/path/to/output-folder/timeline_photos_only_manifest.json"
```

Use the results to isolate whether the issue is video import, still-image import, or mixed timeline import.

## Failure Branches

- If the source folder is missing, empty, or not readable, stop and ask for a valid folder path; do not create an empty timeline.
- If `exiftool` is missing, continue with filesystem timestamps, but tell the user capture-time ordering may be less accurate and recommend `brew install exiftool`.
- If `ffprobe` is missing, continue with conservative duration fallback, but tell the user video duration accuracy may be reduced and recommend `brew install ffmpeg`.
- If Live Photo detection looks wrong, generate a manifest and inspect still/video filename pairs before rerunning with the full timeline.
- If Final Cut Pro rejects the generated XML, first try `--video-only`, then `--photos-only --convert-stills`, then compare the manifests to isolate the failing media class.
- If still images fail to relink or import, rerun with `--convert-stills` and keep `timeline_stills/` next to the `.fcpxml`.
- If Final Cut Pro reports frame-boundary warnings, rerun using the intended `--fps` and run the frame-boundary validation snippet before delivering.
- If media files live on an external drive or cloud-synced folder, tell the user the drive/folder must remain mounted and available when importing into Final Cut Pro.

## Anti-Patterns And Blacklist

- Do not hand-write FCPXML when `scripts/make_timeline.py` can generate it.
- Do not delete, move, rename, or normalize the user's original media files.
- Do not commit or publish user media, generated timelines, converted stills, manifests, or local absolute paths.
- Do not claim capture-time ordering is exact when metadata is missing or inconsistent.
- Do not ignore Final Cut Pro import errors; isolate video-only, photos-only, and mixed timeline paths.
- Do not leave the user with only the XML when still conversion was used; mention that `timeline_stills/` is required for relinking/import.


## 达尔文运行护栏

### 失败分支

- 如果必要输入、文件、资源或外部工具缺失，先说明缺失项和最小补齐路径，不编造结果。
- 如果执行结果与 skill 宣称能力不一致，优先回到原始需求、引用资源和错误输出定位根因。
- 如果验证失败，保留失败证据并修正直接原因；无法验证时明确说明未验证项和原因。
- 如果用户请求超出本 skill 范围，降级为普通助手流程或切换到更匹配的 skill。

### 🔴 CHECKPOINT

以下情况必须暂停并等待用户确认：

- 需要删除文件、回滚 git、强制覆盖、发布、部署、迁移数据或修改线上配置。
- 需要修改密钥、token、认证文件、CI/CD、系统配置或全局依赖。
- 需要处理支付、账号、隐私、生产数据、客户数据或其他高风险信息。
- 继续执行会改变项目结构、业务规则、用户操作路径或长期维护边界。

### 反例与黑名单

- 不要为了完成任务而跳过验证、吞异常、关闭安全校验或伪造运行结果。
- 不要顺手重构、格式化、改写无关文件或添加需求外功能。
- 不要把不确定的假设写成事实。
- 不要输出密钥、token、cookie、私有连接串或未脱敏敏感信息。
