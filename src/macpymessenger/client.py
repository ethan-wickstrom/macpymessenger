"""The public messaging client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, NamedTuple

from .delivery import MessageDelivery
from .exceptions import MessageSendError
from .templates import TemplateCallable, TemplateManager
from .transport import AppleScriptTransport

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from .transport import MessageTransport

__all__ = ["BulkSendResult", "IMessageClient"]


class BulkSendResult(NamedTuple):
    """Immutable recipients classified by a sequential bulk send."""

    sent: tuple[str, ...]
    failed: tuple[str, ...]


class IMessageClient:
    """Send text through the local macOS Messages app.

    ``IMessageClient()`` uses the bundled :class:`AppleScriptTransport`. Pass a
    custom ``transport`` when another delivery mechanism or a test double owns
    the effect. The client emits delivery events to ``macpymessenger.client``
    unless a caller-owned logger is provided.
    """

    __slots__ = ("_delivery", "_logger", "template_manager", "transport")

    def __init__(
        self,
        *,
        transport: MessageTransport | None = None,
        template_manager: TemplateManager | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.transport = transport if transport is not None else AppleScriptTransport()
        self.template_manager = (
            template_manager if template_manager is not None else TemplateManager()
        )
        self._logger = logger if logger is not None else logging.getLogger(__name__)
        self._delivery = MessageDelivery(
            transport=self.transport,
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
