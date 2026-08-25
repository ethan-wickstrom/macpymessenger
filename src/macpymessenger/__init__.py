"""Public package API for macpymessenger."""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

from .client import BulkSendResult, IMessageClient
from .commands import CommandRunner, SubprocessCommandRunner
from .configuration import Configuration
from .exceptions import (
    ConfigurationError,
    InvalidDelayTypeError,
    MacPyMessengerError,
    MessageSendError,
    NegativeDelayError,
    ScriptNotFoundError,
    TemplateAlreadyExistsError,
    TemplateError,
    TemplateNotFoundError,
    TemplateTypeError,
)
from .templates import TemplateManager

try:
    __version__ = version("macpymessenger")
except PackageNotFoundError:  # pragma: no cover - source tree without installation
    __version__ = "0+unknown"

__all__ = [
    "BulkSendResult",
    "CommandRunner",
    "Configuration",
    "ConfigurationError",
    "IMessageClient",
    "InvalidDelayTypeError",
    "MacPyMessengerError",
    "MessageSendError",
    "NegativeDelayError",
    "ScriptNotFoundError",
    "SubprocessCommandRunner",
    "TemplateAlreadyExistsError",
    "TemplateError",
    "TemplateManager",
    "TemplateNotFoundError",
    "TemplateTypeError",
    "__version__",
]

logging.getLogger(__name__).addHandler(logging.NullHandler())
