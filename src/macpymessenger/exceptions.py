"""Custom exceptions for :mod:`macpymessenger`."""

from __future__ import annotations

from typing import Literal, Self

type MessageFailureReason = Literal["delivery", "transport"]


class MacPyMessengerError(Exception):
    """Base exception for all macpymessenger errors."""


class InvalidDelayTypeError(MacPyMessengerError, TypeError):
    """Raised when a send delay is not an integer number of seconds."""

    def __init__(self) -> None:
        super().__init__("Delay must be provided as an integer number of seconds.")


class NegativeDelayError(MacPyMessengerError, ValueError):
    """Raised when a send delay is negative."""

    def __init__(self) -> None:
        super().__init__("Delay must be non-negative.")


class MessageSendError(MacPyMessengerError):
    """Raised when Messages rejects a send or its transport cannot run.

    ``recipient`` and ``reason`` let callers respond without parsing error text.
    ``reason`` is either ``"delivery"`` or ``"transport"``.
    """

    def __init__(
        self,
        recipient: str,
        reason: MessageFailureReason,
        message: str,
    ) -> None:
        super().__init__(message)
        self.recipient = recipient
        self.reason = reason

    @classmethod
    def delivery_failed(cls, recipient: str) -> Self:
        return cls(recipient, "delivery", f"Failed to send message to {recipient}")

    @classmethod
    def transport_failed(cls, recipient: str) -> Self:
        return cls(recipient, "transport", f"Message transport failed for {recipient}")


class TemplateError(MacPyMessengerError):
    """Base exception for template-related errors."""


class TemplateTypeError(TemplateError):
    """Raised when a template factory does not return a t-string template."""

    @classmethod
    def invalid_factory_return(cls) -> Self:
        message = "Template factories must return a string.templatelib.Template instance."
        return cls(message)


class TemplateNotFoundError(TemplateError):
    """Raised when a template cannot be located."""

    @classmethod
    def missing_identifier(cls, identifier: str) -> Self:
        return cls(f"Template with ID '{identifier}' does not exist.")


class TemplateAlreadyExistsError(TemplateError):
    """Raised when a template identifier already exists."""

    @classmethod
    def duplicate_identifier(cls, identifier: str) -> Self:
        return cls(f"Template with ID '{identifier}' already exists.")


class ScriptNotFoundError(MacPyMessengerError):
    """Raised when the bundled AppleScript source cannot be read."""

    @classmethod
    def bundled_script_unavailable(cls) -> Self:
        return cls("Bundled AppleScript could not be read; reinstall macpymessenger.")
