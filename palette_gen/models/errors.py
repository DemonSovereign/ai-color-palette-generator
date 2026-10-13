class PaletteError(Exception):
    """Base class for all palette_gen errors."""


class ExtractionError(PaletteError):
    """Raised when palette extraction fails on an input image."""


class HarmonyError(PaletteError):
    """Raised when a harmony rule cannot produce a valid palette."""


class ExportError(PaletteError):
    """Raised when an export handler cannot serialize a palette."""