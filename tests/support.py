from __future__ import annotations

import logging
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


class StubRunner:
    def __init__(self, failing_recipient_handles: Sequence[str] | None = None) -> None:
        self.commands: list[list[str]] = []
        if failing_recipient_handles is None:
            self.failing_recipient_handles = set()
        else:
            self.failing_recipient_handles = set(failing_recipient_handles)

    def __call__(self, command: Sequence[str]) -> None:
        arguments = list(command)
        self.commands.append(arguments)
        recipient_handle = arguments[2]
        if recipient_handle in self.failing_recipient_handles:
            raise subprocess.CalledProcessError(returncode=1, cmd=arguments)


def remove_file_handlers(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        if isinstance(handler, logging.FileHandler):
            handler.close()
            logger.removeHandler(handler)
