"""Entry point. `palette-gen` dispatches into handlers based on argv."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import typer
from rich.console import Console

from palette_gen.config.settings import load_settings
from palette_gen.handlers.export_handler import ExportHandler
from palette_gen.handlers.image_handler import ImageHandler
from palette_gen.handlers.prompt_handler import PromptHandler
from palette_gen.utils.logging_setup import configure_logging

app = typer.Typer(add_completion=False, help="AI color palette generator.")
console = Console()


@app.command()
def extract(
    source: Path = typer.Argument(..., exists=True, readable=True),
    count: int = typer.Option(6, "--count", "-n", min=2, max=16),
    export: str = typer.Option("json", "--export", "-e"),
    out: Path = typer.Option(Path("exports"), "--out", "-o"),
) -> None:
    """Extract a palette from an image."""
    settings = load_settings()
    configure_logging(settings.log_level)
    handler = ImageHandler(settings)
    palette = handler.extract(source, count=count)
    ExportHandler(settings).write(palette, fmt=export, dest=out)
    console.print(f"[green]wrote {count} swatches to {out}[/green]")


@app.command()
def prompt(
    text: str = typer.Argument(...),
    count: int = typer.Option(5, "--count", "-n", min=2, max=16),
    export: str = typer.Option("json", "--export", "-e"),
    out: Path = typer.Option(Path("exports"), "--out", "-o"),
) -> None:
    """Generate a palette from a text prompt."""
    settings = load_settings()
    configure_logging(settings.log_level)
    handler = PromptHandler(settings)
    palette = handler.generate(text, count=count)
    ExportHandler(settings).write(palette, fmt=export, dest=out)
    console.print(f"[green]wrote {count} swatches for '{text}'[/green]")


def main() -> int:
    try:
        app()
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).exception("unhandled: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())