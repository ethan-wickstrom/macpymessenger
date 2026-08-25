"""Custom exceptions for :mod:`macpymessenger`."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from pathlib import Path


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
    """Raised when sending a message fails.

    ``recipient`` and ``reason`` let callers respond without parsing the error
    message. ``reason`` is either ``"delivery"`` or ``"command"``.
    """

    def __init__(self, recipient: str, reason: str, message: str) -> None:
        super().__init__(message)
        self.recipient = recipient
        self.reason = reason

    @classmethod
    def delivery_failed(cls, recipient: str) -> Self:
        return cls(recipient, "delivery", f"Failed to send message to {recipient}")

    @classmethod
    def command_failed(cls, recipient: str) -> Self:
        return cls(recipient, "command", f"Failed to execute osascript for {recipient}")


class TemplateError(MacPyMessengerError):
    """Base exception for template-related errors."""


class TemplateTypeError(TemplateError):
    """Raised when template interpolation values are not strings."""

    @classmethod
    def non_string_interpolation(cls, expression: str, value_type: str) -> Self:
        message = f"Interpolation '{expression}' resolved to {value_type}; expected str"
        return cls(message)

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


class ConfigurationError(MacPyMessengerError):
    """Base class for configuration-related errors."""


class ScriptNotFoundError(ConfigurationError):
    """Raised when the configured AppleScript cannot be found or read."""

    @classmethod
    def missing_script(cls, script_path: Path) -> Self:
        return cls(f"Send script not found at path: {script_path}")

    @classmethod
    def unreadable_script(cls, script_path: Path, reason: str) -> Self:
        return cls(f"Send script at path '{script_path}' cannot be read: {reason}")

    @classmethod
    def unreadable_script_permissions(cls, script_path: Path) -> Self:
        return cls(f"Send script at path '{script_path}' is not readable due to permission error.")
