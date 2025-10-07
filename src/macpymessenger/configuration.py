"""Configuration primitives for :mod:`macpymessenger`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final, Optional

from .exceptions import ScriptNotFoundError


_PACKAGE_ROOT: Final[Path] = Path(__file__).resolve().parent


@dataclass(frozen=True, slots=True)
class Configuration:
    """Immutable configuration for :class:`~macpymessenger.client.IMessageClient`."""

    send_script_path: Path

    def __init__(self, send_script_path: Optional[Path | str] = None) -> None:
        script_path = self._determine_script_path(send_script_path)
        object.__setattr__(self, "send_script_path", script_path)

    @staticmethod
    def _determine_script_path(candidate: Optional[Path | str]) -> Path:
        if candidate is None:
            script_path = _PACKAGE_ROOT / "osascript" / "sendMessage.scpt"
        elif isinstance(candidate, Path):
            script_path = candidate
        else:
            script_path = Path(candidate)

        if not script_path.exists():
            raise ScriptNotFoundError(f"Send script not found at path: {script_path}")

        return script_path

    def __repr__(self) -> str:
        return f"Configuration(send_script_path={self.send_script_path!s})"
