"""Custom exceptions for :mod:`macpymessenger`."""

from __future__ import annotations


class MacPyMessengerError(Exception):
    """Base exception for all macpymessenger errors."""


class MessageSendError(MacPyMessengerError):
    """Raised when sending a message fails."""


class TemplateError(MacPyMessengerError):
    """Base exception for template-related errors."""


class TemplateNotFoundError(TemplateError):
    """Raised when a template cannot be located."""


class TemplateAlreadyExistsError(TemplateError):
    """Raised when a template identifier already exists."""


class ConfigurationError(MacPyMessengerError):
    """Base class for configuration-related errors."""


class ScriptNotFoundError(ConfigurationError):
    """Raised when the configured AppleScript cannot be found on disk."""
