from __future__ import annotations

from macpymessenger import IMessageClient


def test_stable_client_omits_unimplemented_methods() -> None:
    assert not hasattr(IMessageClient, "get_chat_history")
    assert not hasattr(IMessageClient, "send_with_attachment")
