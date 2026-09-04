"""Message delivery through one domain transport."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from .exceptions import MessageSendError

if TYPE_CHECKING:
    import logging

    from .transport import MessageTransport, SendRequest

__all__ = ["MessageDelivery"]


class MessageDelivery:
    """Map one immutable send request across the transport effect boundary."""

    __slots__ = ("_logger", "_transport")

    def __init__(
        self,
        transport: MessageTransport,
        logger: logging.Logger,
    ) -> None:
        self._transport = transport
        self._logger = logger

    def deliver(self, request: SendRequest) -> None:
        """Send one validated request or raise a typed failure."""
        try:
            self._transport.send(request)
        except subprocess.CalledProcessError:
            # The transport exception can contain private payload or child output.
            self._logger.error("Message delivery failed")  # noqa: TRY400
            raise MessageSendError.delivery_failed(request.recipient) from None
        except OSError:
            # Do not copy transport internals into application logs or tracebacks.
            self._logger.error("Message transport failed")  # noqa: TRY400
            raise MessageSendError.transport_failed(request.recipient) from None
        self._logger.info("Message sent")
