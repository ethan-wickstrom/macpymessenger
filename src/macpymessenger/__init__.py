"""Public package API for macpymessenger."""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

from .client import BulkSendFailure, BulkSendResult, IMessageClient
from .exceptions import (
    InvalidDelayTypeError,
    InvalidSendTextError,
    MacPyMessengerError,
    MessageFailureReason,
    MessageSendError,
    NegativeDelayError,
    ScriptNotFoundError,
    SendTextField,
    SendTextValidationReason,
    TemplateAlreadyExistsError,
    TemplateError,
    TemplateNotFoundError,
    TemplateTypeError,
)
from .templates import TemplateManager
from .transport import AppleScriptTransport, MessageTransport, SendRequest

try:
    __version__ = version("macpymessenger")
except PackageNotFoundError:  # pragma: no cover - source tree without installation
    __version__ = "0+unknown"

__all__ = [
    "AppleScriptTransport",
    "BulkSendFailure",
    "BulkSendResult",
    "IMessageClient",
    "InvalidDelayTypeError",
    "InvalidSendTextError",
    "MacPyMessengerError",
    "MessageFailureReason",
    "MessageSendError",
    "MessageTransport",
    "NegativeDelayError",
    "ScriptNotFoundError",
    "SendRequest",
    "SendTextField",
    "SendTextValidationReason",
    "TemplateAlreadyExistsError",
    "TemplateError",
    "TemplateManager",
    "TemplateNotFoundError",
    "TemplateTypeError",
    "__version__",
]

logging.getLogger(__name__).addHandler(logging.NullHandler())
