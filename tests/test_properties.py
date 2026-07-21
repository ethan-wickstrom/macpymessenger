"""Property-based checks for the correctness properties in docs/foundation.md.

Invariants verified here:

- The send command round-trips arbitrary recipient and body text unchanged;
  argv passing means no escaping layer exists to corrupt it.
- Template rendering of string values matches Python's own f-string
  semantics for conversions and format specs.
- Delay validation accepts exactly the non-negative non-bool ints.
- ``send_bulk`` partitions recipients losslessly and order-preservingly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from hypothesis import given
from hypothesis import strategies as st

from macpymessenger import Configuration, IMessageClient, TemplateManager
from macpymessenger.exceptions import InvalidDelayTypeError, NegativeDelayError
from tests.support import StubRunner

if TYPE_CHECKING:
    from pathlib import Path
    from string.templatelib import Template


@pytest.fixture(scope="module")
def configuration(tmp_path_factory: pytest.TempPathFactory) -> Configuration:
    script: Path = tmp_path_factory.mktemp("scripts") / "send.scpt"
    script.write_text("-- test script", encoding="utf-8")
    return Configuration(script)


@given(
    recipient=st.text(min_size=1),
    body=st.text(),
    delay=st.integers(min_value=0, max_value=10**6),
)
def test_send_command_round_trips_text_unchanged(
    configuration: Configuration, recipient: str, body: str, delay: int
) -> None:
    runner = StubRunner()
    client = IMessageClient(configuration, command_runner=runner)
    client.send(recipient, body, delay)
    assert runner.commands[-1] == [
        "osascript",
        str(configuration.send_script_path),
        recipient,
        body,
        str(delay),
    ]


@given(value=st.text())
def test_rendering_matches_fstring_semantics(value: str) -> None:
    manager = TemplateManager()

    def factory(name: str) -> Template:
        return t"pre {name!r:>20} post"

    manager.create_template("prop", factory)
    assert manager.render_template("prop", {"name": value}) == f"pre {value!r:>20} post"
    manager.delete_template("prop")


@given(delay=st.integers(max_value=-1))
def test_negative_delays_rejected(configuration: Configuration, delay: int) -> None:
    client = IMessageClient(configuration, command_runner=StubRunner())
    with pytest.raises(NegativeDelayError):
        client.send("+15551234567", "hi", delay)


@given(delay=st.one_of(st.booleans(), st.floats(), st.text(), st.none()))
def test_non_int_delays_rejected(configuration: Configuration, delay: object) -> None:
    client = IMessageClient(configuration, command_runner=StubRunner())
    with pytest.raises(InvalidDelayTypeError):
        client.send("+15551234567", "hi", delay)  # ty: ignore[invalid-argument-type]


@given(
    recipients=st.lists(st.text(min_size=1), max_size=20),
    failing=st.sets(st.text(min_size=1), max_size=10),
)
def test_send_bulk_partitions_losslessly(
    configuration: Configuration, recipients: list[str], failing: set[str]
) -> None:
    runner = StubRunner(failing_recipient_handles=sorted(failing))
    client = IMessageClient(configuration, command_runner=runner)
    successful, failed = client.send_bulk(recipients, "hi")
    assert successful == [r for r in recipients if r not in failing]
    assert failed == [r for r in recipients if r in failing]
