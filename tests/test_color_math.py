from __future__ import annotations

import pytest

from palette_gen.utils.color_math import delta_e_76, hex_to_rgb, rgb_to_hex


def test_hex_roundtrip() -> None:
    assert hex_to_rgb("#ff8800") == (255, 136, 0)
    assert rgb_to_hex(255, 136, 0) == "#ff8800"


def test_hex_shorthand() -> None:
    assert hex_to_rgb("#f80") == (255, 136, 0)


def test_bad_hex_raises() -> None:
    with pytest.raises(ValueError):
        hex_to_rgb("#12345")


def test_delta_e_identity() -> None:
    assert delta_e_76((10, 20, 30), (10, 20, 30)) == 0.0


def test_delta_e_ordering() -> None:
    near = delta_e_76((10, 20, 30), (12, 22, 32))
    far = delta_e_76((10, 20, 30), (200, 40, 90))
    assert near < far