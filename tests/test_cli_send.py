from __future__ import annotations

import io
import json
from typing import TYPE_CHECKING

import macpymessenger.__main__ as cli
from macpymessenger import IMessageClient, SendRequest, __version__
from tests.support import StubTransport

if TYPE_CHECKING:
    import pytest


def _set_stdin(monkeypatch: pytest.MonkeyPatch, payload: str) -> None:
    monkeypatch.setattr(cli.sys, "stdin", io.StringIO(payload))


def _install_client(
    monkeypatch: pytest.MonkeyPatch,
    transport: StubTransport,
) -> None:
    client = IMessageClient(transport=transport)
    monkeypatch.setattr(cli, "IMessageClient", lambda: client)


def test_send_json_reads_one_private_request_from_stdin(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    transport = StubTransport()
    _install_client(monkeypatch, transport)
    _set_stdin(
        monkeypatch,
        json.dumps(
            {
                "recipient": "+15555550123",
                "message": "private message body",
                "delay_seconds": 5,
            }
        ),
    )

    exit_code = cli.main(["send", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert json.loads(captured.out) == {
        "tool": "macpymessenger-send",
        "version": __version__,
        "ok": True,
    }
    assert captured.err == ""
    assert transport.requests == [
        SendRequest(
            recipient="+15555550123",
            message="private message body",
            delay_seconds=5,
        )
    ]


def test_send_json_reports_delivery_failure_without_echoing_private_data(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    recipient = "+15555550123"
    message = "private message body"
    _install_client(monkeypatch, StubTransport([recipient]))
    _set_stdin(
        monkeypatch,
        json.dumps({"recipient": recipient, "message": message}),
    )

    exit_code = cli.main(["send", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert payload == {
        "tool": "macpymessenger-send",
        "version": __version__,
        "ok": False,
        "error": {
            "code": "delivery_failed",
            "reason": "delivery",
        },
    }
    assert captured.err == ""
    assert recipient not in captured.out
    assert message not in captured.out


def test_send_json_rejects_unknown_fields_without_echoing_private_data(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    recipient = "+15555550123"
    message = "private message body"
    _set_stdin(
        monkeypatch,
        json.dumps(
            {
                "recipient": recipient,
                "message": message,
                "unexpected": True,
            }
        ),
    )

    exit_code = cli.main(["send", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 2
    assert payload["ok"] is False
    assert payload["error"]["code"] == "invalid_input"
    assert captured.err == ""
    assert recipient not in captured.out
    assert message not in captured.out


def test_send_json_rejects_malformed_json_without_echoing_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    malformed = '{"recipient":"private-recipient","message":"private-message"'
    _set_stdin(monkeypatch, malformed)

    exit_code = cli.main(["send", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 2
    assert payload["ok"] is False
    assert payload["error"]["code"] == "invalid_input"
    assert captured.err == ""
    assert "private-recipient" not in captured.out
    assert "private-message" not in captured.out


def test_send_human_output_is_compact_and_private(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _install_client(monkeypatch, StubTransport())
    _set_stdin(
        monkeypatch,
        json.dumps(
            {
                "recipient": "+15555550123",
                "message": "private message body",
            }
        ),
    )

    exit_code = cli.main(["send"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Message sent.\n"
    assert captured.err == ""
    assert "+15555550123" not in captured.out
    assert "private message body" not in captured.out
