"""Custom exceptions for :mod:`macpymessenger`."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from pathlib import Path


class MacPyMessengerError(Exception):
    """Base exception for all macpymessenger errors."""


class InvalidCommandError(MacPyMessengerError, TypeError):
    """Raised when a command runner receives an invalid command."""

    @classmethod
    def non_sequence(cls) -> Self:
        message = "Command must be a sequence of strings."
        return cls(message)

    @classmethod
    def non_string_segment(cls) -> Self:
        message = "Command segments must be strings."
        return cls(message)


class InvalidDelayTypeError(MacPyMessengerError, TypeError):
    """Raised when a send delay is not an integer number of seconds."""

    def __init__(self) -> None:
        message = "Delay must be provided as an integer number of seconds."
        super().__init__(message)


class NegativeDelayError(MacPyMessengerError, ValueError):
    """Raised when a send delay is negative."""

    def __init__(self) -> None:
        message = "Delay must be non-negative."
        super().__init__(message)


class MessageSendError(MacPyMessengerError):
    """Raised when sending a message fails."""

    @classmethod
    def delivery_failed(cls, phone_number: str) -> Self:
        message = f"Failed to send message to {phone_number}"
        return cls(message)

    @classmethod
    def command_failed(cls, phone_number: str) -> Self:
        message = f"Failed to execute osascript for {phone_number}"
        return cls(message)


class TemplateError(MacPyMessengerError):
    """Base exception for template-related errors."""


class TemplateTypeError(TemplateError):
    """Raised when template interpolation values are not strings."""

    @classmethod
    def non_string_interpolation(cls, expression: str, value_type: str) -> Self:
        message = f"Interpolation '{expression}' resolved to {value_type}; expected str"
        return cls(message)

    @classmethod
    def unexpected_element(cls, element_type: str) -> Self:
        message = f"Unexpected template element of type {element_type}"
        return cls(message)

    @classmethod
    def invalid_factory_return(cls) -> Self:
        message = "Template factories must return a string.templatelib.Template instance."
        return cls(message)


class TemplateNotFoundError(TemplateError):
    """Raised when a template cannot be located."""

    @classmethod
    def missing_identifier(cls, identifier: str) -> Self:
        message = f"Template with ID '{identifier}' does not exist."
        return cls(message)


class TemplateAlreadyExistsError(TemplateError):
    """Raised when a template identifier already exists."""

    @classmethod
    def duplicate_identifier(cls, identifier: str) -> Self:
        message = f"Template with ID '{identifier}' already exists."
        return cls(message)


class ConfigurationError(MacPyMessengerError):
    """Base class for configuration-related errors."""

    @classmethod
    def file_logging_unavailable(cls, log_file_path: Path, reason: str) -> Self:
        message = f"Unable to configure file logging using '{log_file_path}': {reason}"
        return cls(message)


class ScriptNotFoundError(ConfigurationError):
    """Raised when the configured AppleScript cannot be found on disk."""

    @classmethod
    def missing_script(cls, script_path: Path) -> Self:
        message = f"Send script not found at path: {script_path}"
        return cls(message)

    @classmethod
    def unreadable_script(cls, script_path: Path, reason: str) -> Self:
        message = f"Send script at path '{script_path}' cannot be read: {reason}"
        return cls(message)

    @classmethod
    def unreadable_script_permissions(cls, script_path: Path) -> Self:
        message = f"Send script at path '{script_path}' is not readable due to permission error."
        return cls(message)
