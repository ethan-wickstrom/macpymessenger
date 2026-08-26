"""Focused tests for the delivery boundary."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pytest

from macpymessenger import MessageSendError, SendRequest
from macpymessenger.delivery import MessageDelivery
from tests.support import StubTransport

if TYPE_CHECKING:
    from macpymessenger import MessageTransport


class OSErrorTransport:
    def send(self, request: SendRequest) -> None:  # noqa: ARG002
        message = "transport unavailable"
        raise OSError(message)


@pytest.fixture
def delivery_logger() -> logging.Logger:
    return logging.getLogger("test.delivery")


@pytest.fixture
def delivery(
    delivery_logger: logging.Logger,
) -> tuple[MessageDelivery, StubTransport]:
    transport = StubTransport()
    instance = MessageDelivery(
        transport=transport,
        logger=delivery_logger,
    )
    return instance, transport


def test_delivery_sends_one_immutable_request(
    delivery: tuple[MessageDelivery, StubTransport],
) -> None:
    instance, transport = delivery

    instance.deliver("+10000000000", "Hello", delay_seconds=5)

    assert transport.requests == [SendRequest("+10000000000", "Hello", delay_seconds=5)]


def test_delivery_logs_success_without_private_content(
    delivery: tuple[MessageDelivery, StubTransport],
    caplog: pytest.LogCaptureFixture,
) -> None:
    instance, _ = delivery
    recipient = "+10000000000\nforged log entry"
    private_message = "private message body"

    with caplog.at_level(logging.INFO, logger="test.delivery"):
        instance.deliver(recipient, private_message)

    assert "Message sent" in caplog.text
    assert recipient not in caplog.text
    assert "forged log entry" not in caplog.text
    assert private_message not in caplog.text


def test_delivery_maps_applescript_failure_without_private_cause_log_or_text(
    delivery_logger: logging.Logger,
    caplog: pytest.LogCaptureFixture,
) -> None:
    recipient = "+19999999999\nforged log entry"
    private_message = "private message body"
    transport = StubTransport([recipient])
    instance = MessageDelivery(transport=transport, logger=delivery_logger)

    with (
        caplog.at_level(logging.ERROR, logger="test.delivery"),
        pytest.raises(MessageSendError) as exc_info,
    ):
        instance.deliver(recipient, private_message)

    error = exc_info.value
    assert error.recipient == recipient
    assert error.reason == "delivery"
    assert error.__cause__ is None
    assert str(error) == "Message delivery failed."
    assert "Message delivery failed" in caplog.text
    assert recipient not in caplog.text
    assert "forged log entry" not in caplog.text
    assert private_message not in caplog.text
    assert recipient not in str(error)
    assert private_message not in str(error)


def test_delivery_maps_transport_failure_without_private_cause_log_or_text(
    delivery_logger: logging.Logger,
    caplog: pytest.LogCaptureFixture,
) -> None:
    recipient = "+10000000000\nforged log entry"
    private_message = "private message body"
    transport: MessageTransport = OSErrorTransport()
    instance = MessageDelivery(transport=transport, logger=delivery_logger)

    with (
        caplog.at_level(logging.ERROR, logger="test.delivery"),
        pytest.raises(MessageSendError) as exc_info,
    ):
        instance.deliver(recipient, private_message)

    error = exc_info.value
    assert error.recipient == recipient
    assert error.reason == "transport"
    assert error.__cause__ is None
    assert str(error) == "Message transport failed."
    assert "Message transport failed" in caplog.text
    assert recipient not in caplog.text
    assert "forged log entry" not in caplog.text
    assert private_message not in caplog.text
    assert recipient not in str(error)
    assert private_message not in str(error)
