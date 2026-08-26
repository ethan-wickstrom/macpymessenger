from __future__ import annotations

from typing import TYPE_CHECKING

from macpymessenger import Configuration, IMessageClient, TemplateManager
from macpymessenger import __main__ as cli
from macpymessenger.diagnostics import CheckStatus, EnvironmentCheck, EnvironmentReport

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    import pytest


def test_configuration_stores_a_resolved_script_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    script_path = tmp_path / "send.scpt"
    script_path.write_text("-- test script", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    configuration = Configuration("send.scpt")
    monkeypatch.chdir(tmp_path.parent)

    assert configuration.send_script_path == script_path.resolve()


def test_delivery_uses_the_configured_system_osascript_path(tmp_path: Path) -> None:
    script_path = tmp_path / "send.scpt"
    script_path.write_text("-- test script", encoding="utf-8")
    commands: list[list[str]] = []

    def record(command: Sequence[str]) -> None:
        commands.append(list(command))

    configuration = Configuration(script_path)
    client = IMessageClient(configuration, command_runner=record)
    client.send("+15555550123", "Hello")

    assert configuration.osascript_path.as_posix() == "/usr/bin/osascript"
    assert commands[0][0] == configuration.osascript_path.as_posix()


def test_bulk_send_snapshots_the_recipient_sequence(tmp_path: Path) -> None:
    script_path = tmp_path / "send.scpt"
    script_path.write_text("-- test script", encoding="utf-8")
    recipients = ["first", "second"]
    commands: list[list[str]] = []

    def mutate_source_after_first_send(command: Sequence[str]) -> None:
        commands.append(list(command))
        if len(commands) == 1:
            recipients[:] = ["replacement"]

    client = IMessageClient(
        Configuration(script_path),
        command_runner=mutate_source_after_first_send,
    )

    result = client.send_bulk(recipients, "Hello")

    assert result.sent == ("first", "second")
    assert result.failed == ()


def test_templates_apply_normal_python_formatting_to_values() -> None:
    templates = TemplateManager()
    templates.create_template("count", lambda count: t"Count: {count:04d}")

    assert templates.render_template("count", {"count": 7}) == "Count: 0007"


def test_environment_report_distinguishes_unknown_checks_from_local_blockers() -> None:
    report = EnvironmentReport(
        checks=(
            EnvironmentCheck(
                identifier="automation",
                status=CheckStatus.UNKNOWN,
                summary="Automation permission was not checked.",
                fix="Confirm Automation access before sending.",
            ),
        )
    )

    assert report.can_attempt_send is True
    assert report.to_dict()["can_attempt_send"] is True
    assert "ready" not in report.to_dict()


def test_doctor_does_not_claim_unknown_requirements_are_ready(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    report = EnvironmentReport(
        checks=(
            EnvironmentCheck(
                identifier="automation",
                status=CheckStatus.UNKNOWN,
                summary="Automation permission was not checked.",
                fix="Confirm Automation access before sending.",
            ),
        )
    )
    monkeypatch.setattr(cli, "diagnose_environment", lambda: report)

    exit_code = cli.main(["doctor"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Ready for a first send" not in output
    assert "No local blocker was found" in output
