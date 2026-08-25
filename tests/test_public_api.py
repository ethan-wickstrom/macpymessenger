from __future__ import annotations

from importlib.metadata import version

import macpymessenger


def test_package_exports_the_supported_api_from_one_place() -> None:
    assert set(macpymessenger.__all__) == {
        "BulkSendResult",
        "CommandRunner",
        "Configuration",
        "ConfigurationError",
        "IMessageClient",
        "InvalidDelayTypeError",
        "MacPyMessengerError",
        "MessageSendError",
        "NegativeDelayError",
        "ScriptNotFoundError",
        "SubprocessCommandRunner",
        "TemplateAlreadyExistsError",
        "TemplateError",
        "TemplateManager",
        "TemplateNotFoundError",
        "TemplateTypeError",
        "__version__",
    }


def test_package_version_comes_from_distribution_metadata() -> None:
    assert macpymessenger.__version__ == version("macpymessenger")


def test_removed_placeholder_and_wrapper_types_are_not_public() -> None:
    assert not hasattr(macpymessenger, "FileLoggingConfiguration")
    assert not hasattr(macpymessenger, "RenderedTemplate")
    assert not hasattr(macpymessenger.TemplateManager, "compose_template")
