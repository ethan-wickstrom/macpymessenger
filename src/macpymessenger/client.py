"""The public messaging client."""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from typing import NamedTuple

from .commands import CommandRunner, SubprocessCommandRunner
from .configuration import Configuration
from .delivery import MessageDelivery
from .exceptions import MessageSendError
from .templates import TemplateCallable, TemplateManager

__all__ = ["BulkSendResult", "IMessageClient"]


class BulkSendResult(NamedTuple):
    """Recipients classified by a bulk send.

    The named fields make call sites self-explanatory. The tuple shape keeps
    existing ``sent, failed = client.send_bulk(...)`` code working.
    """

    sent: list[str]
    failed: list[str]


class IMessageClient:
    """Send iMessages through the local macOS Messages app.

    ``IMessageClient()`` uses the AppleScript bundled with macpymessenger. Pass a
    custom :class:`Configuration` only when you maintain your own script. Tests
    can replace command execution through ``command_runner``.

    The client emits delivery events to ``macpymessenger.client`` unless a
    caller-owned logger is provided. The library never sets levels, chooses
    formats, or attaches output handlers.
    """

    __slots__ = (
        "_delivery",
        "_logger",
        "command_runner",
        "configuration",
        "template_manager",
    )

    def __init__(
        self,
        configuration: Configuration | None = None,
        template_manager: TemplateManager | None = None,
        command_runner: CommandRunner | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.configuration = configuration if configuration is not None else Configuration()
        self.template_manager = (
            template_manager if template_manager is not None else TemplateManager()
        )
        self.command_runner = (
            command_runner if command_runner is not None else SubprocessCommandRunner()
        )
        self._logger = logger if logger is not None else logging.getLogger(__name__)
        self._delivery = MessageDelivery(
            configuration=self.configuration,
            command_runner=self.command_runner,
            logger=self._logger,
        )

    @property
    def logger(self) -> logging.Logger:
        """The logger that receives delivery events."""
        return self._logger

    def send(self, phone_number: str, message: str, delay_seconds: int = 0) -> None:
        """Send one text message to a Messages phone number or email address."""
        self._delivery.deliver(phone_number, message, delay_seconds)

    def send_template(
        self,
        phone_number: str,
        template_id: str,
        context: Mapping[str, object] | None = None,
        delay_seconds: int = 0,
    ) -> None:
        """Render a registered template and send its text."""
        message = self.template_manager.render_template(template_id, context)
        self.send(phone_number, message, delay_seconds)

    def create_template(self, template_id: str, factory: TemplateCallable) -> None:
        """Register a callable t-string template."""
        self.template_manager.create_template(template_id, factory)

    def update_template(self, template_id: str, factory: TemplateCallable) -> None:
        """Replace a registered template factory."""
        self.template_manager.update_template(template_id, factory)

    def delete_template(self, template_id: str) -> None:
        """Delete a registered template factory."""
        self.template_manager.delete_template(template_id)

    def send_bulk(self, phone_numbers: Sequence[str], message: str) -> BulkSendResult:
        """Send the same text in order and classify each recipient."""
        sent: list[str] = []
        failed: list[str] = []
        for phone_number in phone_numbers:
            try:
                self.send(phone_number, message)
                sent.append(phone_number)
            except MessageSendError:
                failed.append(phone_number)
        return BulkSendResult(sent=sent, failed=failed)
