"""Locates the currently active trained model artefacts on disk."""
from __future__ import annotations

import json
from pathlib import Path

from app.core.config import get_settings

KINDS = ("sentiment", "themes")


def _active_pointer(kind: str, model_dir: Path | None = None) -> Path:
    return (model_dir or get_settings().model_dir) / kind / "ACTIVE.json"


def active_model_info(kind: str, model_dir: Path | None = None) -> dict | None:
    """Return metadata of the active model of ``kind`` or None when untrained."""
    pointer = _active_pointer(kind, model_dir)
    if not pointer.exists():
        return None
    return json.loads(pointer.read_text(encoding="utf-8"))


def available_models(model_dir: Path | None = None) -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for kind in KINDS:
        info = active_model_info(kind, model_dir)
        out[kind] = info["model_version"] if info else None
    return out
