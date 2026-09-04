"""Message transport for the local macOS Messages app."""

from __future__ import annotations

import base64
import subprocess
from dataclasses import dataclass
from importlib.resources import files
from typing import Protocol

from .exceptions import (
    InvalidDelayTypeError,
    InvalidSendTextError,
    NegativeDelayError,
    ScriptNotFoundError,
    SendTextField,
)

_OSASCRIPT_COMMAND = ("/usr/bin/osascript", "-")
_SCRIPT_RESOURCE = ("osascript", "sendMessage.applescript")


def _validate_send_text(field: SendTextField, value: object) -> None:
    """Reject text that cannot cross the UTF-8 AppleScript boundary."""
    if not isinstance(value, str):
        raise InvalidSendTextError.wrong_type(field)
    if not value:
        raise InvalidSendTextError.empty(field)
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise InvalidSendTextError.invalid_encoding(field) from None


@dataclass(frozen=True, slots=True)
class SendRequest:
    """One valid, immutable text delivery request."""

    recipient: str
    message: str
    delay_seconds: int = 0

    def __post_init__(self) -> None:
        _validate_send_text("recipient", self.recipient)
        _validate_send_text("message", self.message)
        if isinstance(self.delay_seconds, bool) or not isinstance(self.delay_seconds, int):
            raise InvalidDelayTypeError
        if self.delay_seconds < 0:
            raise NegativeDelayError


class MessageTransport(Protocol):
    """Transport boundary used to send one immutable request."""

    def send(self, request: SendRequest) -> None:
        """Send ``request`` or raise an execution-specific exception."""


def _load_script_source() -> str:
    """Load the bundled AppleScript handler source."""
    try:
        resource = files("macpymessenger").joinpath(*_SCRIPT_RESOURCE)
        return resource.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        raise ScriptNotFoundError.bundled_script_unavailable() from None


def _encode_text(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def _render_applescript(
    request: SendRequest,
    *,
    script_source: str | None = None,
) -> str:
    """Render a complete script whose private values never enter process argv."""
    source = _load_script_source() if script_source is None else script_source
    recipient = _encode_text(request.recipient)
    message = _encode_text(request.message)
    invocation = (
        f'my sendMessage(my decodeBase64("{recipient}"), '
        f'my decodeBase64("{message}"), {request.delay_seconds})'
    )
    return f"{source.rstrip()}\n\n{invocation}\n"


class AppleScriptTransport:
    """Send requests through ``/usr/bin/osascript`` and the local Messages app."""

    __slots__ = ("_script_source",)

    def __init__(self) -> None:
        self._script_source = _load_script_source()

    def send(self, request: SendRequest) -> None:
        """Send ``request`` without exposing recipient or message text in argv."""
        subprocess.run(  # noqa: S603
            _OSASCRIPT_COMMAND,
            input=_render_applescript(request, script_source=self._script_source),
            capture_output=True,
            check=True,
            shell=False,
            text=True,
        )
