"""Custom exceptions for :mod:`macpymessenger`."""

from __future__ import annotations

from typing import Literal, Self

type MessageFailureReason = Literal["delivery", "transport"]
type SendTextField = Literal["recipient", "message"]
type SendTextValidationReason = Literal["type", "empty", "encoding"]


class MacPyMessengerError(Exception):
    """Base exception for all macpymessenger errors."""


class InvalidSendTextError(MacPyMessengerError, ValueError):
    """Raised when a request contains invalid recipient or message text.

    ``field`` identifies ``"recipient"`` or ``"message"``. ``reason`` is the
    closed value ``"type"``, ``"empty"``, or ``"encoding"``. Error messages
    never include the rejected private value.
    """

    def __init__(
        self,
        field: SendTextField,
        reason: SendTextValidationReason,
        message: str,
    ) -> None:
        super().__init__(message)
        self.field = field
        self.reason = reason

    @classmethod
    def wrong_type(cls, field: SendTextField) -> Self:
        return cls(field, "type", f"{field.capitalize()} must be a string.")

    @classmethod
    def empty(cls, field: SendTextField) -> Self:
        return cls(field, "empty", f"{field.capitalize()} must not be empty.")

    @classmethod
    def invalid_encoding(cls, field: SendTextField) -> Self:
        return cls(field, "encoding", f"{field.capitalize()} must be valid UTF-8 text.")


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
    ``reason`` is either ``"delivery"`` or ``"transport"``. The human-readable
    message stays generic so tracebacks do not repeat the private recipient.
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
        return cls(recipient, "delivery", "Message delivery failed.")

    @classmethod
    def transport_failed(cls, recipient: str) -> Self:
        return cls(recipient, "transport", "Message transport failed.")


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
