from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


class StubRunner:
    def __init__(self, failing_recipient_handles: Sequence[str] | None = None) -> None:
        self.commands: list[list[str]] = []
        self.failing_recipient_handles = set(failing_recipient_handles or ())

    def __call__(self, command: Sequence[str]) -> None:
        arguments = list(command)
        self.commands.append(arguments)
        recipient = arguments[2]
        if recipient in self.failing_recipient_handles:
            raise subprocess.CalledProcessError(returncode=1, cmd=arguments)
