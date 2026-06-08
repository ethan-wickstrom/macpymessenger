"""Configuration primitives for :mod:`macpymessenger`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .exceptions import ScriptNotFoundError

_PACKAGE_ROOT: Final[Path] = Path(__file__).resolve().parent


@dataclass(frozen=True, slots=True)
class Configuration:
    """Immutable configuration for :class:`~macpymessenger.client.IMessageClient`."""

    send_script_path: Path

    def __init__(self, send_script_path: Path | str | None = None) -> None:
        script_path = self._determine_script_path(send_script_path)
        object.__setattr__(self, "send_script_path", script_path)

    @staticmethod
    def _determine_script_path(candidate: Path | str | None) -> Path:
        if candidate is None:
            script_path = _PACKAGE_ROOT / "osascript" / "sendMessage.scpt"
        elif isinstance(candidate, Path):
            script_path = candidate
        else:
            script_path = Path(candidate)

        if not script_path.exists():
            raise ScriptNotFoundError.missing_script(script_path)

        try:
            with script_path.open("rb"):
                pass
        except PermissionError as error:
            raise ScriptNotFoundError.unreadable_script_permissions(script_path) from error
        except OSError as error:
            raise ScriptNotFoundError.unreadable_script(script_path, str(error)) from error

        return script_path

    def __repr__(self) -> str:
        return f"Configuration(send_script_path={self.send_script_path!s})"
