from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

import macpymessenger
from macpymessenger import client as client_module
from macpymessenger import commands as commands_module
from macpymessenger.commands import SubprocessCommandRunner
from macpymessenger.exceptions import InvalidCommandError

if TYPE_CHECKING:
    from collections.abc import Sequence


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


def test_subprocess_runner_invokes_subprocess_without_shell(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded: dict[str, Any] = {}

    def fake_run(command: Sequence[str], **kwargs: object) -> None:
        recorded["command"] = command
        recorded["kwargs"] = kwargs

    monkeypatch.setattr("macpymessenger.commands.subprocess.run", fake_run)
    runner = SubprocessCommandRunner()
    runner(["osascript", "send.scpt", "+10000000000", "hello", "0"])

    assert recorded["command"] == ("osascript", "send.scpt", "+10000000000", "hello", "0")
    expected_kwargs = {"check": True, "text": True, "shell": False}
    assert expected_kwargs.items() <= recorded["kwargs"].items()


def test_command_runner_exports_remain_importable_from_client_and_package_root() -> None:
    assert client_module.SubprocessCommandRunner is commands_module.SubprocessCommandRunner
    assert macpymessenger.SubprocessCommandRunner is commands_module.SubprocessCommandRunner
    assert client_module.CommandRunner is commands_module.CommandRunner
    assert macpymessenger.CommandRunner is commands_module.CommandRunner
