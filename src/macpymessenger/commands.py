"""Command execution for the messaging client.

This module defines the :class:`CommandRunner` protocol and the
subprocess-backed :class:`SubprocessCommandRunner` adapter. Tests replace the
runner with a stub so no real AppleScript runs.
"""

from __future__ import annotations

import subprocess
from collections.abc import Sequence
from typing import Protocol

from .exceptions import InvalidCommandError

__all__ = ["CommandRunner", "SubprocessCommandRunner"]


class CommandRunner(Protocol):
    """Protocol describing callable command runners."""

    def __call__(self, command: Sequence[str]) -> None:  # pragma: no cover - Protocol definition
        """Execute the provided command."""


class SubprocessCommandRunner:
    """Command runner that delegates to :func:`subprocess.run`."""

    def __call__(self, command: Sequence[str]) -> None:
        if not isinstance(command, Sequence) or isinstance(command, (str, bytes)):
            raise InvalidCommandError.non_sequence()
        for segment in command:
            if not isinstance(segment, str):
                raise InvalidCommandError.non_string_segment()
        subprocess.run(tuple(command), check=True, text=True, shell=False)  # noqa: S603
