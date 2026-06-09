from __future__ import annotations

from typing import Any

import pytest

from macpymessenger.client import SubprocessCommandRunner
from macpymessenger.exceptions import InvalidCommandError


def test_subprocess_runner_rejects_non_sequence_command() -> None:
    runner = SubprocessCommandRunner()
    command: Any = object()
    with pytest.raises(InvalidCommandError, match="Command must be a sequence of strings"):
        runner(command)


def test_subprocess_runner_rejects_non_string_command_segments() -> None:
    runner = SubprocessCommandRunner()
    command: Any = ["osascript", 1]
    with pytest.raises(InvalidCommandError, match="Command segments must be strings"):
        runner(command)
