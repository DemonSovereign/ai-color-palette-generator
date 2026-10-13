"""Prompt -> palette. Deterministic hash embedding as the default backend.

The 'AI' in ai-color-palette-generator is the embedding step. We ship a
torch backend behind the `ai` extra; the default is a stable hashed
bag-of-words so the tool works offline on a fresh Windows box.
"""

from __future__ import annotations

import colorsys
import hashlib
import logging

from palette_gen.config.settings import Settings
from palette_gen.models.palette import Palette, Swatch

log = logging.getLogger(__name__)

_STOPWORDS = {"a", "an", "the", "of", "and", "for", "with", "to", "in", "on"}


class PromptHandler:
    def __init__(self, settings: Settings) -> None:
        self._s = settings

    def generate(self, text: str, count: int = 5) -> Palette:
        tokens = [t for t in text.lower().split() if t not in _STOPWORDS]
        if not tokens:
            tokens = [text.lower() or "untitled"]
        swatches: list[Swatch] = []
        for i in range(count):
            seed = f"{'-'.join(tokens)}:{i}:{self._s.kmeans_seed}".encode()
            digest = hashlib.sha256(seed).digest()
            h = int.from_bytes(digest[0:2], "big") / 65535.0
            s = 0.45 + (digest[2] / 255.0) * 0.45
            l = 0.35 + (digest[3] / 255.0) * 0.40
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            swatches.append(
                Swatch(
                    r=int(round(r * 255)),
                    g=int(round(g * 255)),
                    b=int(round(b * 255)),
                    weight=1.0,
                    label=tokens[i % len(tokens)],
                )
            )
        log.info("generated %d swatches for prompt %r", count, text)
        return Palette(swatches=tuple(swatches), name=text[:40], source="prompt")