"""Color conversions and perceptual distance. Pure functions, no state."""

from __future__ import annotations

import math


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise ValueError(f"bad hex: {value!r}")
    return int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb_to_lab(r: int, g: int, b: int) -> tuple[float, float, float]:
    rl, gl, bl = (_srgb_to_linear(x / 255) for x in (r, g, b))
    x = rl * 0.4124 + gl * 0.3576 + bl * 0.1805
    y = rl * 0.2126 + gl * 0.7152 + bl * 0.0722
    z = rl * 0.0193 + gl * 0.1192 + bl * 0.9505
    x, y, z = x / 0.95047, y / 1.0, z / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e_76(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    """CIE76 distance. Cheap and good enough for clustering dedupe."""
    la, aa, ba = rgb_to_lab(*a)
    lb, ab, bb = rgb_to_lab(*b)
    return math.sqrt((la - lb) ** 2 + (aa - ab) ** 2 + (ba - bb) ** 2)