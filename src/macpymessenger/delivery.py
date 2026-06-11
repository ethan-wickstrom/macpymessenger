"""Message delivery for macpymessenger.

This module defines :class:`MessageDelivery`, which owns the full delivery
behavior surface: delay validation, send command construction, command
execution, delivery failure mapping, and send logging.

The delivery class depends on the :class:`~macpymessenger.commands.CommandRunner`
seam so tests can stub execution without invoking real AppleScript.
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from .exceptions import (
    InvalidDelayTypeError,
    MessageSendError,
    NegativeDelayError,
)

if TYPE_CHECKING:
    import logging

    from .commands import CommandRunner
    from .configuration import Configuration

__all__ = ["MessageDelivery"]


class MessageDelivery:
    """Encapsulates the delivery of a single message to a recipient handle.

    Parameters
    ----------
    configuration:
        Resolved configuration specifying the AppleScript entry point.
    command_runner:
        Callable that executes the generated AppleScript command.
    logger:
        Logger instance for operational events.
    """

    __slots__ = ("_command_runner", "_configuration", "_logger")

    def __init__(
        self,
        configuration: Configuration,
        command_runner: CommandRunner,
        logger: logging.Logger,
    ) -> None:
        self._configuration = configuration
        self._command_runner = command_runner
        self._logger = logger

    def deliver(
        self,
        recipient_handle: str,
        message_body: str,
        delay_seconds: object = 0,
    ) -> None:
        """Send *message_body* to *recipient_handle*.

        Parameters
        ----------
        recipient_handle:
            Destination phone number or iMessage address.
        message_body:
            Text content to deliver.
        delay_seconds:
            Non-negative integer seconds to wait before sending.

        Raises
        ------
        InvalidDelayTypeError:
            When ``delay_seconds`` is not a plain ``int``.
        NegativeDelayError:
            When ``delay_seconds`` is negative.
        MessageSendError:
            When delivery or command execution fails.
        """
        delay_value = self._validate_delay(delay_seconds)
        command = self._build_command(recipient_handle, message_body, delay_value)
        self._execute(recipient_handle, command)

    @staticmethod
    def _validate_delay(delay_seconds: object) -> int:
        """Validate and return *delay_seconds* as a plain ``int``.

        Raises
        ------
        InvalidDelayTypeError:
            When ``delay_seconds`` is a ``bool`` or not an ``int``.
        NegativeDelayError:
            When ``delay_seconds`` is less than zero.
        """
        if isinstance(delay_seconds, bool) or not isinstance(delay_seconds, int):
            raise InvalidDelayTypeError
        if delay_seconds < 0:
            raise NegativeDelayError
        return delay_seconds

    def _build_command(
        self,
        recipient_handle: str,
        message_body: str,
        delay_value: int,
    ) -> list[str]:
        """Return the ``osascript`` argument list for this delivery."""
        return [
            "osascript",
            str(self._configuration.send_script_path),
            recipient_handle,
            message_body,
            str(delay_value),
        ]

    def _execute(self, recipient_handle: str, command: list[str]) -> None:
        """Run *command* via the command runner and map failures to typed exceptions."""
        try:
            self._command_runner(command)
            self._logger.info("Message sent to %s", recipient_handle)
        except subprocess.CalledProcessError as error:
            self._logger.exception("Failed to send message to %s", recipient_handle)
            raise MessageSendError.delivery_failed(recipient_handle) from error
        except OSError as error:
            self._logger.exception("Execution error while sending to %s", recipient_handle)
            raise MessageSendError.command_failed(recipient_handle) from error
