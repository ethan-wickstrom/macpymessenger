from __future__ import annotations

from typing import TYPE_CHECKING, Any

import macpymessenger
from macpymessenger import commands as commands_module
from macpymessenger.commands import SubprocessCommandRunner

if TYPE_CHECKING:
    from collections.abc import Sequence

    import pytest


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

    assert recorded["command"] == ["osascript", "send.scpt", "+10000000000", "hello", "0"]
    expected_kwargs = {"check": True, "text": True, "shell": False}
    assert expected_kwargs.items() <= recorded["kwargs"].items()


def test_command_runner_exports_importable_from_package_root() -> None:
    assert macpymessenger.SubprocessCommandRunner is commands_module.SubprocessCommandRunner
    assert macpymessenger.CommandRunner is commands_module.CommandRunner
