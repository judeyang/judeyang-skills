#!/usr/bin/env python3
"""Build a chronological Final Cut Pro XML timeline from a media folder."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import shutil
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


VIDEO_EXTS = {".mov", ".mp4", ".m4v"}
PHOTO_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif"}
LIVE_STILL_EXTS = {".heic", ".heif", ".jpg", ".jpeg"}
SCAN_EXTS = VIDEO_EXTS | PHOTO_EXTS | LIVE_STILL_EXTS

DATE_TAGS = (
    "EXIF:DateTimeOriginal",
    "ExifIFD:DateTimeOriginal",
    "Composite:SubSecDateTimeOriginal",
    "EXIF:CreateDate",
    "ExifIFD:CreateDate",
    "Composite:SubSecCreateDate",
    "Keys:CreationDate",
    "QuickTime:CreationDate",
    "QuickTime:CreateDate",
    "QuickTime:MediaCreateDate",
    "QuickTime:TrackCreateDate",
    "XMP:DateCreated",
    "XMP:CreateDate",
    "File:FileCreateDate",
    "File:FileModifyDate",
)
CONTENT_ID_TAGS = (
    "QuickTime:ContentIdentifier",
    "MakerNotes:ContentIdentifier",
    "MakerNotes:MediaGroupUUID",
    "MakerNotes:Apple_0x0011",
    "Composite:ContentIdentifier",
)


LOCAL_TZ = datetime.now().astimezone().tzinfo


@dataclass(frozen=True)
class MediaItem:
    path: Path
    kind: str
    capture_time: datetime
    duration: Fraction
    live_pair: bool = False


def run_json(cmd: list[str]) -> Any | None:
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def run_text(cmd: list[str]) -> str | None:
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def read_metadata(paths: list[Path]) -> dict[Path, dict[str, Any]]:
    if not paths:
        return {}
    data = run_json(
        [
            "exiftool",
            "-json",
            "-G1",
            "-api",
            "QuickTimeUTC=1",
            *[str(path) for path in paths],
        ]
    )
    if not isinstance(data, list):
        return {}
    metadata: dict[Path, dict[str, Any]] = {}
    for entry in data:
        source = entry.get("SourceFile")
        if source:
            metadata[Path(source)] = entry
    return metadata


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    if cleaned.endswith("Z"):
        cleaned = f"{cleaned[:-1]}+00:00"
    candidates = [
        cleaned,
        cleaned.replace(":", "-", 2),
    ]
    formats = (
        "%Y:%m:%d %H:%M:%S%z",
        "%Y:%m:%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
    )
    for candidate in candidates:
        for fmt in formats:
            try:
                return normalize_datetime(datetime.strptime(candidate, fmt))
            except ValueError:
                pass
        try:
            return normalize_datetime(datetime.fromisoformat(candidate))
        except ValueError:
            pass
    return None


def normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=LOCAL_TZ)
    return value.astimezone()


def capture_time(path: Path, metadata: dict[str, Any]) -> datetime:
    for tag in DATE_TAGS:
        parsed = parse_datetime(metadata.get(tag))
        if parsed is not None:
            return parsed
    stat = path.stat()
    birthtime = getattr(stat, "st_birthtime", stat.st_mtime)
    return datetime.fromtimestamp(birthtime).astimezone()


def content_id(metadata: dict[str, Any]) -> str | None:
    for tag in CONTENT_ID_TAGS:
        value = metadata.get(tag)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def duration_from_metadata(metadata: dict[str, Any]) -> Fraction | None:
    value = metadata.get("QuickTime:Duration") or metadata.get("Composite:Duration")
    if isinstance(value, (int, float)):
        return seconds_to_fraction(float(value))
    if not isinstance(value, str):
        return None
    text = value.strip()
    if text.endswith(" s"):
        try:
            return seconds_to_fraction(float(text[:-2]))
        except ValueError:
            return None
    if ":" in text:
        parts = text.split(":")
        try:
            seconds = float(parts[-1])
            minutes = int(parts[-2]) if len(parts) >= 2 else 0
            hours = int(parts[-3]) if len(parts) >= 3 else 0
            return seconds_to_fraction(hours * 3600 + minutes * 60 + seconds)
        except ValueError:
            return None
    try:
        return seconds_to_fraction(float(text))
    except ValueError:
        return None


def duration_from_ffprobe(path: Path) -> Fraction | None:
    output = run_text(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
    )
    if not output:
        return None
    try:
        return seconds_to_fraction(float(output))
    except ValueError:
        return None


def seconds_to_fraction(seconds: float) -> Fraction:
    return Fraction(max(seconds, 0.001)).limit_denominator(600_000)


def fraction_to_fcpx(value: Fraction) -> str:
    value = value.limit_denominator(600_000)
    if value.denominator == 1:
        return f"{value.numerator}s"
    return f"{value.numerator}/{value.denominator}s"


def align_to_frame(value: Fraction, frame_duration: Fraction, mode: str) -> Fraction:
    frames = value / frame_duration
    if mode == "floor":
        frame_count = frames.numerator // frames.denominator
    elif mode == "ceil":
        frame_count = -(-frames.numerator // frames.denominator)
    else:
        raise ValueError(f"Unsupported frame alignment mode: {mode}")
    return max(frame_count, 1) * frame_duration


def file_url(path: Path) -> str:
    resolved = path.resolve()
    quoted = urllib.parse.quote(str(resolved), safe="/:")
    return f"file://localhost{quoted}"


def discover_media(folder: Path, recursive: bool) -> list[Path]:
    iterator = folder.rglob("*") if recursive else folder.iterdir()
    return sorted(
        path
        for path in iterator
        if path.is_file() and path.suffix.lower() in SCAN_EXTS
    )


def build_items(paths: list[Path], photo_duration: Fraction) -> list[MediaItem]:
    metadata = read_metadata(paths)
    by_content_id: dict[str, list[Path]] = {}
    by_stem: dict[str, list[Path]] = {}

    for path in paths:
        meta = metadata.get(path, {})
        cid = content_id(meta)
        if cid:
            by_content_id.setdefault(cid, []).append(path)
        by_stem.setdefault(path.with_suffix("").name, []).append(path)

    live_video_paths: set[Path] = set()
    live_still_paths: set[Path] = set()

    for group in by_content_id.values():
        videos = [p for p in group if p.suffix.lower() in VIDEO_EXTS]
        stills = [p for p in group if p.suffix.lower() in LIVE_STILL_EXTS]
        if videos and stills:
            live_video_paths.update(videos)
            live_still_paths.update(stills)

    for group in by_stem.values():
        videos = [p for p in group if p.suffix.lower() in VIDEO_EXTS]
        stills = [p for p in group if p.suffix.lower() in LIVE_STILL_EXTS]
        has_heic_still = any(p.suffix.lower() in {".heic", ".heif"} for p in stills)
        if videos and stills and has_heic_still:
            live_video_paths.update(videos)
            live_still_paths.update(stills)

    items: list[MediaItem] = []
    for path in paths:
        ext = path.suffix.lower()
        if path in live_still_paths:
            continue
        meta = metadata.get(path, {})
        if ext in VIDEO_EXTS:
            duration = (
                duration_from_metadata(meta)
                or duration_from_ffprobe(path)
                or Fraction(2, 1)
            )
            kind = "live-video" if path in live_video_paths else "video"
        elif ext in PHOTO_EXTS:
            duration = photo_duration
            kind = "photo"
        else:
            continue
        items.append(
            MediaItem(
                path=path,
                kind=kind,
                capture_time=capture_time(path, meta),
                duration=duration,
                live_pair=path in live_video_paths,
            )
        )

    return sorted(items, key=lambda item: (item.capture_time, item.path.name.lower()))


def xml_attr(value: str) -> str:
    return escape(value, {'"': "&quot;"})


def timeline_duration(item: MediaItem, frame_duration: Fraction) -> Fraction:
    if item.kind in {"video", "live-video"}:
        return align_to_frame(item.duration, frame_duration, "floor")
    return align_to_frame(item.duration, frame_duration, "ceil")


def write_fcpxml(
    items: list[MediaItem],
    output: Path,
    project_name: str,
    frame_duration: Fraction,
) -> None:
    item_durations = [timeline_duration(item, frame_duration) for item in items]
    total = sum(item_durations, Fraction(0, 1))
    lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!DOCTYPE fcpxml>",
        '<fcpxml version="1.10">',
        "  <resources>",
        f'    <format id="r1" name="FFVideoFormat1080p30" frameDuration="{fraction_to_fcpx(frame_duration)}" width="1920" height="1080" colorSpace="1-1-1 (Rec. 709)"/>',
    ]
    for index, (item, clip_duration) in enumerate(zip(items, item_durations), start=2):
        has_audio = ' hasAudio="1"' if item.kind in {"video", "live-video"} else ""
        lines.append(
            f'    <asset id="r{index}" name="{xml_attr(item.path.name)}" '
            f'start="0s" duration="{fraction_to_fcpx(clip_duration)}" '
            f'hasVideo="1"{has_audio}>'
        )
        lines.append(
            f'      <media-rep kind="original-media" src="{xml_attr(file_url(item.path))}" suggestedFilename="{xml_attr(item.path.name)}"/>'
        )
        lines.append("    </asset>")
    lines.extend(
        [
            "  </resources>",
            "  <library>",
            f'    <event name="{xml_attr(project_name)}">',
            f'      <project name="{xml_attr(project_name)}">',
            f'        <sequence format="r1" duration="{fraction_to_fcpx(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">',
            "          <spine>",
        ]
    )
    offset = Fraction(0, 1)
    for index, (item, clip_duration) in enumerate(zip(items, item_durations), start=2):
        note = "Live Photo video" if item.live_pair else item.kind
        if item.kind == "photo":
            lines.append(
                f'            <video name="{xml_attr(item.path.name)}" ref="r{index}" '
                f'offset="{fraction_to_fcpx(offset)}" start="0s" '
                f'duration="{fraction_to_fcpx(clip_duration)}"/>'
            )
        else:
            lines.append(
                f'            <asset-clip name="{xml_attr(item.path.name)}" ref="r{index}" '
                f'offset="{fraction_to_fcpx(offset)}" start="0s" '
                f'duration="{fraction_to_fcpx(clip_duration)}" tcFormat="NDF"/>'
            )
        offset += clip_duration
    lines.extend(
        [
            "          </spine>",
            "        </sequence>",
            "      </project>",
            "    </event>",
            "  </library>",
            "</fcpxml>",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(items: list[MediaItem], output: Path) -> None:
    rows = [
        {
            "path": str(item.path),
            "name": item.path.name,
            "kind": item.kind,
            "capture_time": item.capture_time.isoformat(),
            "duration_seconds": float(item.duration),
            "live_pair": item.live_pair,
        }
        for item in items
    ]
    output.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def convert_stills_for_fcp(items: list[MediaItem], output: Path) -> list[MediaItem]:
    still_dir = output.with_suffix("").parent / f"{output.with_suffix('').name}_stills"
    if still_dir.exists():
        shutil.rmtree(still_dir)
    still_dir.mkdir(parents=True, exist_ok=True)
    converted: list[MediaItem] = []
    for item in items:
        if item.kind != "photo":
            converted.append(item)
            continue
        target = still_dir / f"{item.path.stem}.jpg"
        counter = 2
        while target.exists() and target.resolve() != item.path.resolve():
            target = still_dir / f"{item.path.stem}_{counter}.jpg"
            counter += 1
        if item.path.suffix.lower() in {".jpg", ".jpeg"}:
            shutil.copy2(item.path, target)
        else:
            result = subprocess.run(
                ["sips", "-s", "format", "jpeg", str(item.path), "--out", str(target)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise RuntimeError(f"Failed to convert still image: {item.path}\n{result.stderr}")
        converted.append(
            MediaItem(
                path=target,
                kind=item.kind,
                capture_time=item.capture_time,
                duration=item.duration,
                live_pair=item.live_pair,
            )
        )
    return converted


def write_fcpxml_bundle(
    items: list[MediaItem],
    output: Path,
    project_name: str,
    frame_duration: Fraction,
) -> None:
    fcpxml = output.with_suffix(".fcpxml")
    write_fcpxml(items, fcpxml, project_name, frame_duration)
    info = {
        "bundleVersion": 1,
        "projectName": project_name,
        "createdBy": "make_timeline.py",
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "Info.plist").write_bytes(plistlib.dumps(info))
    (output / "project.fcpxml").write_text(fcpxml.read_text(encoding="utf-8"), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a chronological Final Cut Pro XML timeline from one media folder."
    )
    parser.add_argument("folder", type=Path, help="Folder containing videos, Live Photos, JPGs, PNGs, and HEICs.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("timeline.fcpxml"),
        help="Output .fcpxml path. Default: timeline.fcpxml",
    )
    parser.add_argument(
        "--photo-duration",
        type=float,
        default=2.0,
        help="Duration in seconds for JPG/PNG photos. Default: 2",
    )
    parser.add_argument(
        "--project-name",
        default="Chronological Timeline",
        help="Project/event name written into the FCPXML.",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=30.0,
        help="Timeline frame rate used to align clip durations. Default: 30",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subfolders too.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Optional JSON manifest showing the sorted media order.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the sorted order without writing FCPXML.",
    )
    parser.add_argument(
        "--video-only",
        action="store_true",
        help="Only include videos. Useful for isolating Final Cut Pro import issues.",
    )
    parser.add_argument(
        "--photos-only",
        action="store_true",
        help="Only include photo placeholders. Useful for isolating Final Cut Pro import issues.",
    )
    parser.add_argument(
        "--convert-stills",
        action="store_true",
        help="Convert/copy all photo placeholders to JPEG files next to the output before writing FCPXML.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    folder = args.folder.expanduser()
    if not folder.exists() or not folder.is_dir():
        print(f"Folder does not exist or is not a directory: {folder}", file=sys.stderr)
        return 2
    if args.photo_duration <= 0:
        print("--photo-duration must be greater than zero.", file=sys.stderr)
        return 2
    if args.fps <= 0:
        print("--fps must be greater than zero.", file=sys.stderr)
        return 2
    frame_duration = Fraction(1, 1) / Fraction(str(args.fps)).limit_denominator(600_000)

    paths = discover_media(folder, args.recursive)
    items = build_items(paths, seconds_to_fraction(args.photo_duration))
    if args.video_only:
        items = [item for item in items if item.kind in {"video", "live-video"}]
    if args.photos_only:
        items = [item for item in items if item.kind == "photo"]
    if not items:
        print("No supported media found.", file=sys.stderr)
        return 1

    for index, item in enumerate(items, start=1):
        live = " live-pair" if item.live_pair else ""
        print(
            f"{index:03d}  {item.capture_time.isoformat()}  "
            f"{float(item.duration):8.3f}s  {item.kind}{live}  {item.path}"
        )

    if args.manifest:
        write_manifest(items, args.manifest.expanduser())

    if not args.dry_run:
        output = args.out.expanduser()
        output_items = convert_stills_for_fcp(items, output) if args.convert_stills else items
        write_fcpxml(output_items, output, args.project_name, frame_duration)
        print(f"\nWrote {args.out.expanduser()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
