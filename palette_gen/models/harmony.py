"""Harmony rule definitions used by the harmony service."""

from __future__ import annotations

from enum import Enum


class Harmony(str, Enum):
    COMPLEMENTARY = "complementary"
    ANALOGOUS = "analogous"
    TRIADIC = "triadic"
    TETRADIC = "tetradic"
    SPLIT_COMPLEMENTARY = "split_complementary"
    MONOCHROMATIC = "monochromatic"


HUE_OFFSETS: dict[Harmony, tuple[float, ...]] = {
    Harmony.COMPLEMENTARY: (0.0, 180.0),
    Harmony.ANALOGOUS: (-30.0, 0.0, 30.0),
    Harmony.TRIADIC: (0.0, 120.0, 240.0),
    Harmony.TETRADIC: (0.0, 90.0, 180.0, 270.0),
    Harmony.SPLIT_COMPLEMENTARY: (0.0, 150.0, 210.0),
    Harmony.MONOCHROMATIC: (0.0,),
}