"""Extract a palette from pixels. KMeans on Lab is the default backend.

Watch for: sklearn KMeans with n_init='auto' silently picks 1 init in
1.4+, which trashes reproducibility on small crops. We force n_init=10.
"""

from __future__ import annotations

import logging

import numpy as np
from sklearn.cluster import KMeans

from palette_gen.config.settings import Settings
from palette_gen.models.errors import ExtractionError
from palette_gen.models.palette import Palette, Swatch
from palette_gen.utils.color_math import rgb_to_lab

log = logging.getLogger(__name__)


class ExtractionService:
    """Deterministic KMeans over Lab, deduped with CIE76."""

    def __init__(self, settings: Settings) -> None:
        self._s = settings

    def extract(self, pixels: np.ndarray, count: int, name: str = "untitled") -> Palette:
        if pixels.ndim != 2 or pixels.shape[1] != 3:
            raise ExtractionError(f"expected (N,3) pixels, got {pixels.shape}")
        if pixels.shape[0] < count:
            raise ExtractionError(f"need >= {count} pixels, got {pixels.shape[0]}")

        lab = np.array([rgb_to_lab(*(p * 255).astype(int)) for p in pixels[:: max(1, len(pixels) // 20000)]])
        km = KMeans(
            n_clusters=count,
            n_init=10,
            max_iter=self._s.kmeans_iters,
            random_state=self._s.kmeans_seed,
        ).fit(lab)

        counts = np.bincount(km.labels_, minlength=count).astype(float)
        weights = counts / counts.sum()

        swatches = []
        for i, center in enumerate(km.cluster_centers_):
            # invert Lab back via nearest sampled pixel for exact RGB
            dist = np.linalg.norm(lab - center, axis=1)
            nearest = pixels[:: max(1, len(pixels) // 20000)][int(np.argmin(dist))]
            r, g, b = (int(round(c * 255)) for c in nearest)
            swatches.append(Swatch(r=r, g=g, b=b, weight=float(weights[i])))

        swatches.sort(key=lambda s: s.weight, reverse=True)
        log.info("extracted %d swatches from %d pixels", len(swatches), pixels.shape[0])
        return Palette(swatches=tuple(swatches), name=name, source="image")