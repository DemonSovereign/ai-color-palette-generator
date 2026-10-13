"""Core schema: Swatch and Palette. Both frozen and hashable."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Swatch:
    """A single color. RGB 0-255, HSL 0-360/0-1/0-1, hex without '#'."""

    r: int
    g: int
    b: int
    weight: float = 1.0
    label: str | None = None

    @property
    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def as_hsl(self) -> tuple[float, float, float]:
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        mx, mn = max(r, g, b), min(r, g, b)
        l = (mx + mn) / 2
        if mx == mn:
            return 0.0, 0.0, l
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        h = (
            60 * ((g - b) / d % 6)
            if mx == r
            else 60 * ((b - r) / d + 2)
            if mx == g
            else 60 * ((r - g) / d + 4)
        )
        return h % 360, s, l


@dataclass(frozen=True, slots=True)
class Palette:
    """An ordered set of swatches plus provenance metadata."""

    swatches: tuple[Swatch, ...]
    name: str = "untitled"
    source: str = "unknown"
    meta: dict[str, str] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.swatches)

    def hexes(self) -> list[str]:
        return [s.hex for s in self.swatches]