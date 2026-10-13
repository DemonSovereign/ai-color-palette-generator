"""Apply a harmony rule to a seed swatch, producing related hues."""

from __future__ import annotations

import colorsys

from palette_gen.models.errors import HarmonyError
from palette_gen.models.harmony import HUE_OFFSETS, Harmony
from palette_gen.models.palette import Palette, Swatch


class HarmonyService:
    def generate(self, seed: Swatch, rule: Harmony, count: int) -> Palette:
        offsets = HUE_OFFSETS.get(rule)
        if not offsets:
            raise HarmonyError(f"unknown rule: {rule}")
        h, s, l = seed.as_hsl()
        out: list[Swatch] = []
        for i in range(count):
            off = offsets[i % len(offsets)]
            nh = (h + off) % 360
            # nudge lightness so a 4-swatch tetradic doesn't look flat
            nl = max(0.08, min(0.92, l + (i // len(offsets)) * 0.14 - 0.07))
            r, g, b = colorsys.hls_to_rgb(nh / 360, nl, s)
            out.append(
                Swatch(
                    r=int(round(r * 255)),
                    g=int(round(g * 255)),
                    b=int(round(b * 255)),
                    weight=1.0,
                    label=f"{rule.value}:{i}",
                )
            )
        return Palette(swatches=tuple(out), name=f"{seed.label or 'seed'}-{rule.value}", source="harmony")