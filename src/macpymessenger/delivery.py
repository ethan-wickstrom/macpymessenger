"""Message delivery through one domain transport."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from .exceptions import MessageFailureReason, MessageSendError

if TYPE_CHECKING:
    import logging

    from .transport import MessageTransport, SendRequest

__all__ = ["MessageDelivery"]


def _sanitized_failure(
    recipient: str,
    reason: MessageFailureReason,
) -> MessageSendError:
    if reason == "delivery":
        return MessageSendError.delivery_failed(recipient)
    return MessageSendError.transport_failed(recipient)


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
        """Send one validated request or raise a context-free typed failure."""
        failure: MessageSendError | None = None
        try:
            self._transport.send(request)
        except MessageSendError as error:
            failure = _sanitized_failure(request.recipient, error.reason)
        except subprocess.CalledProcessError:
            # Preserve compatibility with custom transports built before the
            # typed transport-failure contract.
            failure = MessageSendError.delivery_failed(request.recipient)
        except OSError:
            failure = MessageSendError.transport_failed(request.recipient)

        if failure is not None:
            self._logger.error("Message %s failed", failure.reason)
            # Raise after leaving the handler so an unsafe custom transport
            # exception is not reachable through ``__cause__`` or ``__context__``.
            raise failure

        self._logger.info("Message sent")
