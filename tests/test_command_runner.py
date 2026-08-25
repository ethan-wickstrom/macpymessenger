from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from macpymessenger import CommandRunner, SubprocessCommandRunner

if TYPE_CHECKING:
    from collections.abc import Sequence


def test_subprocess_runner_invokes_subprocess_without_a_shell(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded: dict[str, Any] = {}

    def fake_run(command: Sequence[str], **kwargs: object) -> None:
        recorded["command"] = command
        recorded["kwargs"] = kwargs

    monkeypatch.setattr("macpymessenger.commands.subprocess.run", fake_run)
    runner: CommandRunner = SubprocessCommandRunner()
    runner(["osascript", "send.scpt", "+10000000000", "hello", "0"])

    assert recorded["command"] == (
        "osascript",
        "send.scpt",
        "+10000000000",
        "hello",
        "0",
    )
    assert recorded["kwargs"] == {"check": True, "shell": False}
