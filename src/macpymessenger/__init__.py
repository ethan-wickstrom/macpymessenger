"""Public package exports for macpymessenger."""

from __future__ import annotations

import logging

from .client import IMessageClient
from .commands import CommandRunner, SubprocessCommandRunner
from .configuration import Configuration
from .templates import TemplateManager

__all__ = [
    "CommandRunner",
    "Configuration",
    "IMessageClient",
    "SubprocessCommandRunner",
    "TemplateManager",
]

logging.getLogger(__name__).addHandler(logging.NullHandler())
