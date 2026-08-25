"""The public messaging client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, NamedTuple

from .commands import CommandRunner, SubprocessCommandRunner
from .configuration import Configuration
from .delivery import MessageDelivery
from .exceptions import MessageSendError
from .templates import TemplateCallable, TemplateManager

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

__all__ = ["BulkSendResult", "IMessageClient"]


class BulkSendResult(NamedTuple):
    """Immutable recipients classified by a bulk send.

    The named fields make call sites self-explanatory. The outer named tuple and
    inner tuples contain no shared mutable state. Tuple unpacking remains valid.
    """

    sent: tuple[str, ...]
    failed: tuple[str, ...]


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

    def send(self, recipient: str, message: str, delay_seconds: int = 0) -> None:
        """Send one text message to a Messages phone number or email address."""
        self._delivery.deliver(recipient, message, delay_seconds)

    def send_template(
        self,
        recipient: str,
        template_id: str,
        context: Mapping[str, object] | None = None,
        delay_seconds: int = 0,
    ) -> None:
        """Render a registered template and send its text."""
        message = self.template_manager.render_template(template_id, context)
        self.send(recipient, message, delay_seconds)

    def create_template(self, template_id: str, factory: TemplateCallable) -> None:
        """Register a callable t-string template."""
        self.template_manager.create_template(template_id, factory)

    def update_template(self, template_id: str, factory: TemplateCallable) -> None:
        """Replace a registered template factory."""
        self.template_manager.update_template(template_id, factory)

    def delete_template(self, template_id: str) -> None:
        """Delete a registered template factory."""
        self.template_manager.delete_template(template_id)

    def send_bulk(self, recipients: Sequence[str], message: str) -> BulkSendResult:
        """Send the same text in order and classify each recipient."""
        sent: list[str] = []
        failed: list[str] = []
        for recipient in recipients:
            try:
                self.send(recipient, message)
                sent.append(recipient)
            except MessageSendError:
                failed.append(recipient)
        return BulkSendResult(sent=tuple(sent), failed=tuple(failed))
