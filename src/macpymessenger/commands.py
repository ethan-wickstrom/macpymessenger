"""Command execution for the messaging client.

This module defines the :class:`CommandRunner` protocol and the
subprocess-backed :class:`SubprocessCommandRunner` adapter. Tests replace the
runner with a stub so no real AppleScript runs. The runner performs no
argument validation: commands are built internally by
:class:`~macpymessenger.delivery.MessageDelivery` and :func:`subprocess.run`
rejects invalid argument types itself.
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ["CommandRunner", "SubprocessCommandRunner"]


class CommandRunner(Protocol):
    """Protocol describing callable command runners."""

    def __call__(self, command: Sequence[str]) -> None:  # pragma: no cover - Protocol definition
        """Execute the provided command."""


class SubprocessCommandRunner:
    """Command runner that delegates to :func:`subprocess.run`."""

    def __call__(self, command: Sequence[str]) -> None:
        subprocess.run(command, check=True, text=True, shell=False)  # noqa: S603
