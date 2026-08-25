"""Command execution for the messaging client.

The subprocess adapter accepts only commands built inside macpymessenger. Tests
replace it with a stub, so automated checks never invoke AppleScript.
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ["CommandRunner", "SubprocessCommandRunner"]


class CommandRunner(Protocol):
    """Callable interface for executing a prepared command."""

    def __call__(self, command: Sequence[str]) -> None:
        """Execute ``command`` or raise an operating-system error."""
        ...


class SubprocessCommandRunner:
    """Execute prepared commands with :func:`subprocess.run`."""

    def __call__(self, command: Sequence[str]) -> None:
        subprocess.run(tuple(command), check=True, shell=False)  # noqa: S603
