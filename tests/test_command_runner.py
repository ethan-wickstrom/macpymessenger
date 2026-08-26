from __future__ import annotations

from typing import TYPE_CHECKING, Any

from macpymessenger import CommandRunner, SubprocessCommandRunner

if TYPE_CHECKING:
    from collections.abc import Sequence

    import pytest


def test_subprocess_runner_invokes_subprocess_without_a_shell_or_inherited_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded: dict[str, Any] = {}

    def fake_run(command: Sequence[str], **kwargs: object) -> None:
        recorded["command"] = command
        recorded["kwargs"] = kwargs

    monkeypatch.setattr("macpymessenger.commands.subprocess.run", fake_run)
    runner: CommandRunner = SubprocessCommandRunner()
    runner(["/usr/bin/osascript", "send.scpt", "+10000000000", "hello", "0"])

    assert recorded["command"] == (
        "/usr/bin/osascript",
        "send.scpt",
        "+10000000000",
        "hello",
        "0",
    )
    assert recorded["kwargs"] == {
        "capture_output": True,
        "check": True,
        "shell": False,
        "text": True,
    }
