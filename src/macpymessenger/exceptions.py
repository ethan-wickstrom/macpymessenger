"""Custom exceptions for :mod:`macpymessenger`."""

from __future__ import annotations


class MacPyMessengerError(Exception):
    """Base exception for all macpymessenger errors."""


class MessageSendError(MacPyMessengerError):
    """Raised when sending a message fails."""


class TemplateError(MacPyMessengerError):
    """Base exception for template-related errors."""


class TemplateTypeError(TemplateError):
    """Raised when template interpolation values are not strings."""


class TemplateNotFoundError(TemplateError):
    """Raised when a template cannot be located."""


class TemplateAlreadyExistsError(TemplateError):
    """Raised when a template identifier already exists."""


class DuplicateTemplateIdentifierError(TemplateError):
    """Raised when duplicate template identifiers are detected while loading."""


class ConfigurationError(MacPyMessengerError):
    """Base class for configuration-related errors."""


class ScriptNotFoundError(ConfigurationError):
    """Raised when the configured AppleScript cannot be found on disk."""
