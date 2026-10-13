"""Thin adapter: image file -> ExtractionService -> Palette."""

from __future__ import annotations

import logging
from pathlib import Path

from palette_gen.config.settings import Settings
from palette_gen.services.extraction_service import ExtractionService
from palette_gen.utils.cache import read_palette, write_palette
from palette_gen.utils.image_io import load_rgb

log = logging.getLogger(__name__)


class ImageHandler:
    def __init__(self, settings: Settings) -> None:
        self._s = settings
        self._svc = ExtractionService(settings)

    def extract(self, source: Path, count: int = 6) -> "palette_gen.models.palette.Palette":  # noqa: F821
        payload = source.read_bytes()
        cached = read_palette(self._s.cache_dir, payload, tag=f"img-{count}")
        if cached is not None:
            log.info("cache hit for %s", source.name)
            return cached
        pixels = load_rgb(source, max_dim=self._s.max_image_dim)
        palette = self._svc.extract(pixels, count=count, name=source.stem)
        write_palette(self._s.cache_dir, payload, tag=f"img-{count}", palette=palette)
        return palette