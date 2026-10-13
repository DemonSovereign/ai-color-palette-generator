"""Image loading with a hard dimension cap so we don't OOM on 30k banners."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError

from palette_gen.models.errors import ExtractionError


def load_rgb(path: Path, max_dim: int = 8192) -> np.ndarray:
    """Return float32 RGB in [0,1], shape (H*W, 3). Raises ExtractionError."""
    try:
        with Image.open(path) as im:
            im = im.convert("RGB")
            if max(im.size) > max_dim:
                im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
            arr = np.asarray(im, dtype=np.float32) / 255.0
    except (UnidentifiedImageError, OSError) as exc:
        raise ExtractionError(f"cannot read image {path}: {exc}") from exc
    return arr.reshape(-1, 3)