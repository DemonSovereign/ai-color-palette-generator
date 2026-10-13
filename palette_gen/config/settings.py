"""Typed settings loaded from TOML, with sane defaults for Windows desktops."""

from __future__ import annotations

import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field

DEFAULT_CONFIG = Path("config/default.toml")


class Settings(BaseModel):
    log_level: str = "INFO"
    cache_dir: Path = Path(".cache/palette_gen")
    export_dir: Path = Path("exports")
    max_image_dim: int = Field(default=8192, ge=256, le=16384)
    kmeans_iters: int = Field(default=24, ge=4, le=256)
    kmeans_seed: int = 6767
    ai_backend: str = Field(default="kmeans", pattern="^(kmeans|torch)$")
    weights_path: Path = Path("models/weights/palette_embed.pt")


@lru_cache(maxsize=1)
def load_settings(path: Path | None = None) -> Settings:
    cfg_path = path or DEFAULT_CONFIG
    if cfg_path.exists():
        raw = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
        return Settings(**raw.get("palette_gen", {}))
    return Settings()