from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from palette_gen.config.settings import Settings
from palette_gen.handlers.export_handler import ExportHandler
from palette_gen.handlers.prompt_handler import PromptHandler
from palette_gen.models.palette import Palette, Swatch
from palette_gen.services.extraction_service import ExtractionService
from palette_gen.services.harmony_service import HarmonyService
from palette_gen.services.scoring_service import ScoringService
from palette_gen.models.harmony import Harmony


@pytest.fixture