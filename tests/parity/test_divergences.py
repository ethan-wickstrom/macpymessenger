"""Intentional divergences from the incumbent (commit 327762d).

Each test pins new behavior and records the old behavior it replaces plus
the requirement that justifies the change (see docs/paradigm.md and
docs/audit.md). Every difference between old and new that is not covered by
test_baseline.py is listed here; anything else would be a defect.
"""

from __future__ import annotations

import inspect
import logging
from typing import TYPE_CHECKING

import pytest

import macpymessenger
from macpymessenger import Configuration, IMessageClient, TemplateManager, client, exceptions
from tests.support import StubRunner

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def script_path(tmp_path: Path) -> Path:
    script = tmp_path / "send.scpt"
    script.write_text("-- test script", encoding="utf-8")
    return script


class TestLibraryNoLongerManagesLogHandlers:
    """Old: IMessageClient accepted file_logging=FileLoggingConfiguration(),
    attached a logging.FileHandler with its own format, defaulted the module
    logger's level to INFO, and raised
    ConfigurationError.file_logging_unavailable when the file could not open.

    Justification: the Python logging contract for libraries — emit to
    logging.getLogger(__name__) behind a NullHandler; never attach handlers,
    set levels, or choose formats (docs/paradigm.md § Logging).
    """

    def test_file_logging_configuration_is_gone(self) -> None:
        assert not hasattr(macpymessenger, "FileLoggingConfiguration")

    def test_client_has_no_file_logging_parameter(self) -> None:
        parameters = inspect.signature(IMessageClient).parameters
        assert "file_logging" not in parameters

    def test_client_does_not_mutate_logger_level(self, script_path: Path) -> None:
        logger = logging.getLogger("macpymessenger.delivery")
        original_level = logger.level
        IMessageClient(Configuration(script_path), command_runner=StubRunner())
        assert logger.level == original_level == logging.NOTSET

    def test_package_installs_null_handler(self) -> None:
        package_logger = logging.getLogger("macpymessenger")
        assert any(isinstance(h, logging.NullHandler) for h in package_logger.handlers)

    def test_file_logging_error_factory_is_gone(self) -> None:
        assert not hasattr(exceptions.ConfigurationError, "file_logging_unavailable")


class TestExperimentalStubsAreGone:
    """Old: get_chat_history and send_with_attachment existed only to raise
    NotImplementedError with an "Experimental:" prefix.

    Justification: the public API is the set of things the library can do
    (docs/audit.md § 5); no requirement reserves the names.
    """

    @pytest.mark.parametrize("name", ["get_chat_history", "send_with_attachment"])
    def test_stub_methods_removed(self, name: str) -> None:
        assert not hasattr(IMessageClient, name)


class TestRunnerNoLongerPreValidates:
    """Old: SubprocessCommandRunner raised InvalidCommandError for
    non-sequence commands or non-string segments before calling subprocess.

    Justification: the command is built internally and subprocess.run
    already rejects invalid argument types; validation belongs at system
    boundaries only (docs/foundation.md § Boundary rule).
    """

    def test_invalid_command_error_is_gone(self) -> None:
        assert not hasattr(exceptions, "InvalidCommandError")


class TestRenderingReturnsPlainStrings:
    """Old: TemplateManager.compose_template wrapped render_template's
    string in a RenderedTemplate dataclass; the only consumer immediately
    unwrapped .content.

    Justification: rendering produces a string (docs/audit.md § 4).
    """

    def test_rendered_template_is_gone(self) -> None:
        assert not hasattr(macpymessenger, "RenderedTemplate")

    def test_compose_template_is_gone(self) -> None:
        assert not hasattr(TemplateManager, "compose_template")


class TestMigrationShimExportsAreGone:
    """Old: macpymessenger.client re-exported CommandRunner and
    SubprocessCommandRunner after their extraction to macpymessenger.commands
    (issue #35 compatibility shim).

    Justification: the migration is finished; one canonical import path
    (docs/audit.md § 7). Root exports are unchanged (see baseline).
    """

    def test_client_module_no_longer_re_exports_runner_names(self) -> None:
        assert "CommandRunner" not in client.__all__
        assert "SubprocessCommandRunner" not in client.__all__
