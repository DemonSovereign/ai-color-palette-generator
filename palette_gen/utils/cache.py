"""Tiny JSON cache keyed by content hash. Avoids re-extracting on repeat runs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from palette_gen.models.palette import Palette, Swatch


def _key(payload: bytes, tag: str) -> str:
    return f"{tag}-{hashlib.sha256(payload).hexdigest()[:16]}"


def read_palette(cache_dir: Path, payload: bytes, tag: str) -> Palette | None:
    path = cache_dir / f"{_key(payload, tag)}.json"
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    swatches = tuple(Swatch(**s) for s in raw["swatches"])
    return Palette(swatches=swatches, name=raw.get("name", "cached"), source=raw.get("source", "cache"))


def write_palette(cache_dir: Path, payload: bytes, tag: str, palette: Palette) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{_key(payload, tag)}.json"
    path.write_text(
        json.dumps(
            {
                "name": palette.name,
                "source": palette.source,
                "swatches": [
                    {"r": s.r, "g": s.g, "b": s.b, "weight": s.weight, "label": s.label}
                    for s in palette.swatches
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )