from __future__ import annotations

from importlib.metadata import version
from inspect import signature
from pathlib import Path

import macpymessenger


def test_package_exports_the_supported_api_from_one_place() -> None:
    assert set(macpymessenger.__all__) == {
        "AppleScriptTransport",
        "BulkSendFailure",
        "BulkSendResult",
        "IMessageClient",
        "InvalidDelayTypeError",
        "InvalidSendTextError",
        "MacPyMessengerError",
        "MessageFailureReason",
        "MessageSendError",
        "MessageTransport",
        "NegativeDelayError",
        "ScriptNotFoundError",
        "SendRequest",
        "SendTextField",
        "SendTextValidationReason",
        "TemplateAlreadyExistsError",
        "TemplateError",
        "TemplateManager",
        "TemplateNotFoundError",
        "TemplateTypeError",
        "__version__",
    }


def test_package_version_comes_from_distribution_metadata() -> None:
    assert macpymessenger.__version__ == version("macpymessenger")


def test_package_declares_inline_types() -> None:
    assert macpymessenger.__file__ is not None
    assert (Path(macpymessenger.__file__).parent / "py.typed").is_file()


def test_removed_placeholder_and_shallow_abstractions_are_not_public() -> None:
    assert not hasattr(macpymessenger, "CommandRunner")
    assert not hasattr(macpymessenger, "Configuration")
    assert not hasattr(macpymessenger, "ConfigurationError")
    assert not hasattr(macpymessenger, "FileLoggingConfiguration")
    assert not hasattr(macpymessenger, "RenderedTemplate")
    assert not hasattr(macpymessenger, "SubprocessCommandRunner")
    assert not hasattr(macpymessenger.TemplateManager, "compose_template")


def test_send_signatures_use_recipient_terminology() -> None:
    assert tuple(signature(macpymessenger.IMessageClient.send).parameters) == (
        "self",
        "recipient",
        "message",
        "delay_seconds",
    )
    assert tuple(signature(macpymessenger.IMessageClient.send_request).parameters) == (
        "self",
        "request",
    )
    assert tuple(signature(macpymessenger.IMessageClient.send_template).parameters) == (
        "self",
        "recipient",
        "template_id",
        "context",
        "delay_seconds",
    )
    assert tuple(signature(macpymessenger.IMessageClient.send_bulk).parameters) == (
        "self",
        "recipients",
        "message",
    )
