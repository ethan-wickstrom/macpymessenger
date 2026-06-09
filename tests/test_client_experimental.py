from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

import pytest

from macpymessenger import IMessageClient

if TYPE_CHECKING:
    from pathlib import Path

    from tests.support import StubRunner


def test_get_chat_history_is_experimental(client: tuple[IMessageClient, StubRunner]) -> None:
    instance, _ = client
    with pytest.raises(
        NotImplementedError, match=r"Experimental: Chat history retrieval is not yet implemented\."
    ):
        instance.get_chat_history("+15551234567")
    doc = inspect.getdoc(IMessageClient.get_chat_history)
    assert doc is not None
    assert "Experimental: Chat history retrieval is not yet implemented." in doc
    assert "Expected availability: TBD." in doc


def test_send_with_attachment_is_experimental(
    client: tuple[IMessageClient, StubRunner], tmp_path: Path
) -> None:
    instance, _ = client
    with pytest.raises(
        NotImplementedError,
        match=r"Experimental: Sending messages with attachments is not yet implemented\.",
    ):
        instance.send_with_attachment("+15559876543", "hello", str(tmp_path / "file.pdf"))
    doc = inspect.getdoc(IMessageClient.send_with_attachment)
    assert doc is not None
    assert "Experimental: Sending messages with attachments is not yet implemented." in doc
    assert "Expected availability: TBD." in doc
