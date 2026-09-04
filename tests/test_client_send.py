from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from macpymessenger import (
    AppleScriptTransport,
    IMessageClient,
    InvalidDelayTypeError,
    MessageSendError,
    NegativeDelayError,
    SendRequest,
)
from tests.support import StubTransport

if TYPE_CHECKING:
    from tests.support import StubTransport as ClientStubTransport


def test_client_uses_the_applescript_transport_by_default() -> None:
    client = IMessageClient()

    assert isinstance(client.transport, AppleScriptTransport)


def test_send_message_builds_one_request(
    client: tuple[IMessageClient, ClientStubTransport],
) -> None:
    instance, transport = client

    instance.send("1234567890", "Hello")

    assert transport.requests == [SendRequest("1234567890", "Hello")]


def test_send_request_crosses_the_client_without_reconstruction(
    client: tuple[IMessageClient, ClientStubTransport],
) -> None:
    instance, transport = client
    request = SendRequest("1234567890", "Hello", delay_seconds=3)

    instance.send_request(request)

    assert transport.requests == [request]
    assert transport.requests[0] is request


def test_send_message_failure(client: tuple[IMessageClient, ClientStubTransport]) -> None:
    instance, transport = client
    transport.failing_recipients.add("9876543210")

    with pytest.raises(MessageSendError):
        instance.send("9876543210", "Hello")


def test_send_message_rejects_negative_delay(
    client: tuple[IMessageClient, ClientStubTransport],
) -> None:
    instance, _ = client
    with pytest.raises(NegativeDelayError, match="Delay must be non-negative"):
        instance.send("1234567890", "Hello", delay_seconds=-1)


def test_send_message_requires_integer_delay(
    client: tuple[IMessageClient, ClientStubTransport],
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


def test_client_accepts_a_custom_transport() -> None:
    transport = StubTransport()

    client = IMessageClient(transport=transport)

    assert client.transport is transport
