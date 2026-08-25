from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from macpymessenger import (
    IMessageClient,
    InvalidDelayTypeError,
    MessageSendError,
    NegativeDelayError,
)
from tests.support import StubRunner

if TYPE_CHECKING:
    from tests.support import StubRunner as ClientStubRunner


def test_client_uses_the_bundled_configuration_by_default() -> None:
    runner = StubRunner()
    client = IMessageClient(command_runner=runner)

    client.send("1234567890", "Hello")

    assert client.configuration.send_script_path.name == "sendMessage.scpt"
    assert runner.commands[0][1] == str(client.configuration.send_script_path)


def test_send_message_success(client: tuple[IMessageClient, ClientStubRunner]) -> None:
    instance, runner = client
    instance.send("1234567890", "Hello")
    assert runner.commands[0][2] == "1234567890"


def test_send_message_failure(client: tuple[IMessageClient, ClientStubRunner]) -> None:
    instance, runner = client
    runner.failing_recipient_handles.add("9876543210")
    with pytest.raises(MessageSendError):
        instance.send("9876543210", "Hello")


def test_send_message_rejects_negative_delay(
    client: tuple[IMessageClient, ClientStubRunner],
) -> None:
    instance, _ = client
    with pytest.raises(NegativeDelayError, match="Delay must be non-negative"):
        instance.send("1234567890", "Hello", delay_seconds=-1)


def test_send_message_requires_integer_delay(
    client: tuple[IMessageClient, ClientStubRunner],
) -> None:
    instance, _ = client
    with pytest.raises(InvalidDelayTypeError, match="Delay must be provided as an integer"):
        instance.send(
            "1234567890",
            "Hello",
            delay_seconds=1.5,  # ty: ignore[invalid-argument-type]
        )
    with pytest.raises(InvalidDelayTypeError, match="Delay must be provided as an integer"):
        instance.send("1234567890", "Hello", delay_seconds=True)
