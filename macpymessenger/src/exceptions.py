class MacPyMessengerError(Exception):
    """Base exception class for macpymessenger."""


class MessageSendError(MacPyMessengerError):
    """Raised when there's an error sending a message."""


class TemplateError(MacPyMessengerError):
    """Base exception class for template-related errors."""


class TemplateNotFoundError(TemplateError):
    """Raised when a requested template is not found."""


class TemplateAlreadyExistsError(TemplateError):
    """Raised when attempting to create a template that already exists."""


class ConfigurationError(MacPyMessengerError):
    """Raised when there's an error in the configuration."""


class ScriptNotFoundError(ConfigurationError):
    """Raised when a required script file is not found."""


class AttachmentError(MacPyMessengerError):
    """Raised when there's an error handling attachments."""
