from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from macpymessenger import SendRequest


class StubTransport:
    def __init__(self, failing_recipients: Iterable[str] = ()) -> None:
        self.requests: list[SendRequest] = []
        self.failing_recipients = set(failing_recipients)

    def send(self, request: SendRequest) -> None:
        self.requests.append(request)
        if request.recipient in self.failing_recipients:
            raise subprocess.CalledProcessError(
                returncode=1,
                cmd=["/usr/bin/osascript", "-"],
            )
