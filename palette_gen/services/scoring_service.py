"""Score a palette on contrast, spread, and perceptual variety."""

from __future__ import annotations

import itertools
import math

from palette_gen.models.palette import Palette
from palette_gen.utils.color_math import delta_e_76, rgb_to_lab


class ScoringService:
    """Returns 0..1. Higher is more usable as a UI palette."""

    def score(self, palette: Palette) -> float:
        if len(palette) < 2:
            return 0.0
        contrast = self._contrast(palette)
        spread = self._spread(palette)
        variety = self._variety(palette)
        return round((contrast * 0.4 + spread * 0.35 + variety * 0.25), 4)

    def _contrast(self, palette: Palette) -> float:
        lums = []
        for s in palette.swatches:
            r, g, b = s.r / 255, s.g / 255, s.b / 255
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            lums.append(lum)
        ratio = (max(lums) + 0.05) / (min(lums) + 0.05)
        return min(1.0, math.log(ratio + 1, 21))

    def _spread(self, palette: Palette) -> float:
        labs = [rgb_to_lab(s.r, s.g, s.b) for s in palette.swatches]
        a_vals = [l[1] for l in labs]
        b_vals = [l[2] for l in labs]
        return min(1.0, (max(a_vals) - min(a_vals) + max(b_vals) - min(b_vals)) / 220)

    def _variety(self, palette: Palette) -> float:
        pairs = list(itertools.combinations(palette.swatches, 2))
        if not pairs:
            return 0.0
        dists = [delta_e_76((a.r, a.g, a.b), (b.r, b.g, b.b)) for a, b in pairs]
        return min(1.0, sum(dists) / len(dists) / 90)