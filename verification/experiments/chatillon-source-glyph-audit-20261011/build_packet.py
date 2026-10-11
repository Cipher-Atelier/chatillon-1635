#!/usr/bin/env python3
"""Build a local, lossless PNG inspection packet from explicitly supplied boxes.

No EXIF orientation correction, color conversion, filtering, or rotation is
applied. Native crops preserve decoded source samples. Optional 3x views use
nearest-neighbor replication. The complete source is never written to the packet.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import sys

from PIL import Image


LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
# These modes can be written to PNG without color conversion or sample clipping.
PNG_MODES = {"1", "L", "LA", "P", "RGB", "RGBA", "I;16"}


def safe_label(value: object, location: str) -> str:
    if not isinstance(value, str) or LABEL.fullmatch(value) is None:
        raise ValueError(f"{location}: label must be 1-64 ASCII letters, digits, '_' or '-', starting with a letter or digit")
    return value


def checked_box(value: object, size: tuple[int, int], location: str) -> list[int]:
    if not isinstance(value, list) or len(value) != 4 or any(type(n) is not int for n in value):
        raise ValueError(f"{location}: box must be [x, y, width, height] with four integers")
    x, y, width, height = value
    if x < 0 or y < 0 or width <= 0 or height <= 0:
        raise ValueError(f"{location}: coordinates must be nonnegative and dimensions positive")
    if x + width > size[0] or y + height > size[1]:
        raise ValueError(f"{location}: box lies outside source dimensions {size[0]}x{size[1]}")
    return value


def checked_spec(spec: object, size: tuple[int, int]) -> list[dict]:
    if not isinstance(spec, dict) or set(spec) != {"pairs"}:
        raise ValueError("spec must be an object containing only 'pairs'")
    pairs = spec["pairs"]
    if not isinstance(pairs, list) or not pairs:
        raise ValueError("spec.pairs must be a nonempty list")
    seen_pairs = set()
    for index, pair in enumerate(pairs):
        location = f"pairs[{index}]"
        if not isinstance(pair, dict) or set(pair) != {"label", "items"}:
            raise ValueError(f"{location}: expected only 'label' and 'items'")
        label = safe_label(pair["label"], location)
        # Case-insensitive uniqueness also prevents collisions on macOS/Windows.
        if label.casefold() in seen_pairs:
            raise ValueError(f"{location}: duplicate pair label {label!r}")
        seen_pairs.add(label.casefold())
        items = pair["items"]
        if not isinstance(items, list) or not items:
            raise ValueError(f"{location}.items must be a nonempty list")
        seen_items = set()
        for item_index, item in enumerate(items):
            item_location = f"{location}.items[{item_index}]"
            if not isinstance(item, dict) or set(item) != {"label", "box", "context_box"}:
                raise ValueError(f"{item_location}: expected only 'label', 'box', and 'context_box'")
            item_label = safe_label(item["label"], item_location)
            if item_label.casefold() in seen_items:
                raise ValueError(f"{item_location}: duplicate item label {item_label!r}")
            seen_items.add(item_label.casefold())
            checked_box(item["box"], size, f"{item_location}.box")
            checked_box(item["context_box"], size, f"{item_location}.context_box")
    return pairs


def no_duplicate_keys(entries: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in entries:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def write_png(image: Image.Image, path: Path, output_dir: Path) -> dict:
    image.save(path, format="PNG")
    data = path.read_bytes()
    return {
        "path": path.relative_to(output_dir).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "dimensions": list(image.size),
        "mode": image.mode,
    }


def build_packet(source: Path, spec_path: Path, output_dir: Path, enlarge_3x: bool = False) -> dict:
    if not source.is_file():
        raise ValueError(f"source does not exist or is not a file: {source}")
    if output_dir.exists() or output_dir.is_symlink():
        raise ValueError(f"output directory already exists: {output_dir}")
    # Decode and hash the same snapshot, even if the source changes during a run.
    source_bytes = source.read_bytes()
    spec = json.loads(spec_path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
    with Image.open(io.BytesIO(source_bytes)) as original:
        if getattr(original, "n_frames", 1) != 1:
            raise ValueError("source must contain exactly one image frame")
        original.load()
        if original.mode not in PNG_MODES:
            raise ValueError(f"source mode {original.mode!r} cannot be emitted as PNG without sample conversion")
        pairs = checked_spec(spec, original.size)
        manifest = {
            "schema_version": 1,
            "source": {
                "sha256": hashlib.sha256(source_bytes).hexdigest(),
                "bytes": len(source_bytes),
                "dimensions": list(original.size),
                "mode": original.mode,
                "format": original.format,
            },
            "processing": {
                "box_format": "x,y,width,height",
                "orientation": "decoded source; no EXIF transform",
                "enlargement": "nearest-neighbor 3x" if enlarge_3x else None,
            },
            "pairs": [],
        }
        # Exclusive creation is the final guard against overwriting any output.
        output_dir.mkdir()
        try:
            for pair in pairs:
                pair_dir = output_dir / pair["label"]
                pair_dir.mkdir()
                pair_entry = {"label": pair["label"], "items": []}
                for item in pair["items"]:
                    item_dir = pair_dir / item["label"]
                    item_dir.mkdir()
                    item_entry = {"label": item["label"]}
                    for kind, key in (("crop", "box"), ("context", "context_box")):
                        x, y, width, height = item[key]
                        crop = original.crop((x, y, x + width, y + height))
                        entry = write_png(crop, item_dir / f"{kind}.png", output_dir)
                        entry["box"] = item[key]
                        item_entry[kind] = entry
                        if enlarge_3x:
                            enlarged = crop.resize((width * 3, height * 3), resample=Image.Resampling.NEAREST)
                            item_entry[f"{kind}_3x"] = write_png(enlarged, item_dir / f"{kind}_3x.png", output_dir)
                    pair_entry["items"].append(item_entry)
                manifest["pairs"].append(pair_entry)
            (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        except BaseException:
            shutil.rmtree(output_dir)
            raise
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="exact local source image path")
    parser.add_argument("--spec", required=True, type=Path, help="JSON crop specification path")
    parser.add_argument("--output-dir", required=True, type=Path, help="new output directory; parent must already exist")
    parser.add_argument("--enlarge-3x", action="store_true", help="also emit nearest-neighbor 3x views")
    args = parser.parse_args()
    try:
        manifest = build_packet(args.source, args.spec, args.output_dir, args.enlarge_3x)
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Created {args.output_dir / 'manifest.json'} ({len(manifest['pairs'])} pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
