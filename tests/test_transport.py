from __future__ import annotations

import base64
import subprocess
import sys
from typing import TYPE_CHECKING, Any

import pytest

from macpymessenger import (
    AppleScriptTransport,
    InvalidSendTextError,
    MessageTransport,
    SendRequest,
)
from macpymessenger.transport import _render_applescript

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


def test_send_request_rejects_non_string_recipient() -> None:
    with pytest.raises(InvalidSendTextError) as exc_info:
        SendRequest(123, "Hello")  # ty: ignore[invalid-argument-type]

    assert exc_info.value.field == "recipient"
    assert exc_info.value.reason == "type"


def test_send_request_rejects_non_string_message() -> None:
    with pytest.raises(InvalidSendTextError) as exc_info:
        SendRequest("+15555550123", 123)  # ty: ignore[invalid-argument-type]

    assert exc_info.value.field == "message"
    assert exc_info.value.reason == "type"


@pytest.mark.parametrize(
    ("recipient", "message", "field"),
    [
        ("", "Hello", "recipient"),
        ("+15555550123", "", "message"),
    ],
)
def test_send_request_rejects_empty_text(
    recipient: str,
    message: str,
    field: str,
) -> None:
    with pytest.raises(InvalidSendTextError) as exc_info:
        SendRequest(recipient, message)

    assert exc_info.value.field == field
    assert exc_info.value.reason == "empty"


@pytest.mark.parametrize(
    ("recipient", "message", "field"),
    [
        ("\ud800", "Hello", "recipient"),
        ("+15555550123", "\ud800", "message"),
    ],
)
def test_send_request_rejects_text_that_cannot_be_encoded_as_utf8(
    recipient: str,
    message: str,
    field: str,
) -> None:
    with pytest.raises(InvalidSendTextError) as exc_info:
        SendRequest(recipient, message)

    assert exc_info.value.field == field
    assert exc_info.value.reason == "encoding"


def test_send_request_rejects_non_integer_delay() -> None:
    with pytest.raises(TypeError, match="Delay must be provided as an integer"):
        SendRequest("+15555550123", "Hello", delay_seconds=True)
    with pytest.raises(TypeError, match="Delay must be provided as an integer"):
        SendRequest("+15555550123", "Hello", delay_seconds=1.5)  # ty: ignore[invalid-argument-type]


def test_send_request_rejects_negative_delay() -> None:
    with pytest.raises(ValueError, match="Delay must be non-negative"):
        SendRequest("+15555550123", "Hello", delay_seconds=-1)


def test_applescript_transport_keeps_private_values_out_of_process_argv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded: dict[str, Any] = {}

    def fake_run(command: Sequence[str], **kwargs: object) -> None:
        recorded["command"] = tuple(command)
        recorded["kwargs"] = kwargs

    monkeypatch.setattr("macpymessenger.transport.subprocess.run", fake_run)
    transport: MessageTransport = AppleScriptTransport()
    request = SendRequest(
        recipient="+15555550123",
        message="private message body",
        delay_seconds=5,
    )

    transport.send(request)

    assert recorded["command"] == ("/usr/bin/osascript", "-")
    kwargs = recorded["kwargs"]
    assert kwargs["capture_output"] is True
    assert kwargs["check"] is True
    assert kwargs["shell"] is False
    assert kwargs["text"] is True
    script = kwargs["input"]
    assert isinstance(script, str)
    assert request.recipient not in script
    assert request.message not in script
    assert base64.b64encode(request.recipient.encode()).decode("ascii") in script
    assert base64.b64encode(request.message.encode()).decode("ascii") in script


def test_rendered_applescript_is_deterministic() -> None:
    request = SendRequest("+15555550123", "Hello", delay_seconds=3)

    assert _render_applescript(request) == _render_applescript(request)


@pytest.mark.skipif(sys.platform != "darwin", reason="AppleScript compiler is macOS-only")
def test_rendered_applescript_compiles_on_macos(tmp_path: Path) -> None:
    source_path = tmp_path / "send.applescript"
    output_path = tmp_path / "send.scpt"
    source_path.write_text(
        _render_applescript(SendRequest("+15555550123", "Hello", delay_seconds=3)),
        encoding="utf-8",
    )

    subprocess.run(  # noqa: S603
        ("/usr/bin/osacompile", "-o", str(output_path), str(source_path)),
        capture_output=True,
        check=True,
        text=True,
    )

    assert output_path.is_file()
