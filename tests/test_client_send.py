from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from macpymessenger.exceptions import InvalidDelayTypeError, MessageSendError, NegativeDelayError

if TYPE_CHECKING:
    from macpymessenger import IMessageClient
    from tests.support import StubRunner


def test_send_message_success(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, runner = client
    instance.send("1234567890", "Hello")
    assert runner.commands[0][2] == "1234567890"


def test_send_message_failure(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, runner = client
    runner.failing_recipient_handles.add("9876543210")
    with pytest.raises(MessageSendError):
        instance.send("9876543210", "Hello")


def test_send_message_rejects_negative_delay(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, _ = client
    with pytest.raises(NegativeDelayError, match="Delay must be non-negative"):
        instance.send("1234567890", "Hello", delay_seconds=-1)


def test_send_message_requires_integer_delay(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, _ = client
    with pytest.raises(InvalidDelayTypeError, match="Delay must be provided as an integer"):
        instance.send("1234567890", "Hello", delay_seconds=1.5)
    with pytest.raises(InvalidDelayTypeError, match="Delay must be provided as an integer"):
        instance.send("1234567890", "Hello", delay_seconds=True)
