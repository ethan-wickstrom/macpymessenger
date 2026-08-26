from __future__ import annotations

import io
import json

import pytest

import macpymessenger.__main__ as cli
from macpymessenger import IMessageClient, SendRequest, __version__
from tests.support import StubTransport

INVALID_INPUT_EXIT_CODE = 2


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


@pytest.mark.parametrize(
    "payload",
    [
        "[]",
        '{"message":"private-message"}',
        '{"recipient":"private-recipient"}',
        '{"recipient":1,"message":"private-message"}',
        '{"recipient":"private-recipient","message":1}',
        '{"recipient":"","message":"private-message"}',
        '{"recipient":"private-recipient","message":""}',
        '{"recipient":"private-recipient","message":"private-message","delay_seconds":true}',
        '{"recipient":"private-recipient","message":"private-message","delay_seconds":-1}',
        '{"recipient":"private-recipient","message":"private-message","delay_seconds":1.5}',
        '{"recipient":"first","recipient":"second","message":"private-message"}',
        r'{"recipient":"private-recipient","message":"\ud800"}',
        '{"recipient":"private-recipient","message":"private-message","unexpected":true}',
    ],
)
def test_send_json_rejects_ambiguous_or_invalid_input_before_creating_a_client(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    payload: str,
) -> None:
    def unexpected_client() -> IMessageClient:
        message = "invalid input reached the Messages effect boundary"
        raise AssertionError(message)

    monkeypatch.setattr(cli, "IMessageClient", unexpected_client)
    _set_stdin(monkeypatch, payload)

    exit_code = cli.main(["send", "--json"])
    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == INVALID_INPUT_EXIT_CODE
    assert result == {
        "tool": "macpymessenger-send",
        "version": __version__,
        "ok": False,
        "error": {"code": "invalid_input"},
    }
    assert captured.err == ""
    assert "private-recipient" not in captured.out
    assert "private-message" not in captured.out


def test_send_json_rejects_malformed_json_without_echoing_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    malformed = '{"recipient":"private-recipient","message":"private-message"'
    _set_stdin(monkeypatch, malformed)

    exit_code = cli.main(["send", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == INVALID_INPUT_EXIT_CODE
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


def test_send_help_documents_the_noninteractive_contract(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["send", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    assert "one JSON object from standard input" in output
    assert '"recipient"' in output
    assert '"message"' in output
    assert '"delay_seconds"' in output
    assert "Exit status:" in output
    assert "0  transport completed" in output
    assert "1  send or transport failure" in output
    assert "2  invalid input" in output
