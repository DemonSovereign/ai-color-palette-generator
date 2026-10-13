"""Dispatch a Palette to a format handler. One branch per registered format."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Protocol

from palette_gen.config.settings import Settings
from palette_gen.models.errors import ExportError
from palette_gen.models.palette import Palette

log = logging.getLogger(__name__)


class _FormatWriter(Protocol):
    ext: str
    def write(self, palette: Palette, dest: Path) -> Path: ...


class _JsonWriter:
    ext = "json"

    def write(self, palette: Palette, dest: Path) -> Path:
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / f"{palette.name or 'palette'}.json"
        path.write_text(
            json.dumps(
                {
                    "name": palette.name,
                    "source": palette.source,
                    "swatches": [{"hex": s.hex, "r": s.r, "g": s.g, "b": s.b, "weight": s.weight} for s in palette.swatches],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return path


class _GplWriter:
    """GIMP palette. Ubiquitous on Windows design toolchains."""

    ext = "gpl"

    def write(self, palette: Palette, dest: Path) -> Path:
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / f"{palette.name or 'palette'}.gpl"
        lines = ["GIMP Palette", f"Name: {palette.name}", "Columns: 4", "#"]
        for s in palette.swatches:
            lines.append(f"{s.r:3d} {s.g:3d} {s.b:3d}\t{s.label or s.hex}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path


_WRITERS: dict[str, _FormatWriter] = {w.ext: w for w in (_JsonWriter(), _GplWriter())}


class ExportHandler:
    def __init__(self, settings: Settings) -> None:
        self._s = settings

    def write(self, palette: Palette, fmt: str = "json", dest: Path | None = None) -> Path:
        writer = _WRITERS.get(fmt.lower())
        if writer is None:
            raise ExportError(f"no writer for {fmt!r}; have {sorted(_WRITERS)}")
        target = dest or self._s.export_dir
        path = writer.write(palette, target)
        log.info("exported %s -> %s", palette.name, path)
        return path