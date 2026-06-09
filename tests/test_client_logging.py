from __future__ import annotations

import logging
from pathlib import Path

import pytest

from macpymessenger import (
    Configuration,
    FileLoggingConfiguration,
    IMessageClient,
    TemplateManager,
)
from macpymessenger.exceptions import ConfigurationError
from tests.support import StubRunner, remove_file_handlers


def test_client_does_not_create_log_file_by_default(
    configuration: Configuration,
    template_manager: TemplateManager,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    log_path = tmp_path / "macpymessenger.log"
    logger = logging.getLogger("macpymessenger.client")
    remove_file_handlers(logger)
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=StubRunner(),
    )
    try:
        assert log_path.exists() is False
        has_file_handler = any(
            isinstance(handler, logging.FileHandler) for handler in client_instance.logger.handlers
        )
        assert not has_file_handler
    finally:
        remove_file_handlers(client_instance.logger)


def test_client_with_preexisting_filehandler_logger(
    configuration: Configuration,
    template_manager: TemplateManager,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    log_path = tmp_path / "preexisting.log"
    logger = logging.getLogger("test_logger_with_filehandler")
    remove_file_handlers(logger)
    file_handler = logging.FileHandler(log_path)
    logger.addHandler(file_handler)

    try:
        client_instance = IMessageClient(
            configuration=configuration,
            template_manager=template_manager,
            command_runner=StubRunner(),
            logger=logger,
            file_logging=FileLoggingConfiguration(),
        )
        file_handlers = [
            handler
            for handler in client_instance.logger.handlers
            if isinstance(handler, logging.FileHandler)
        ]
        assert len(file_handlers) == 1
        assert file_handlers[0] is file_handler
        assert log_path.exists() is True
    finally:
        remove_file_handlers(logger)


def test_client_file_logging_opt_in_creates_handler(
    configuration: Configuration,
    template_manager: TemplateManager,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    log_path = tmp_path / "macpymessenger.log"
    logger = logging.getLogger("macpymessenger.client")
    remove_file_handlers(logger)
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=StubRunner(),
        file_logging=FileLoggingConfiguration(),
    )
    try:
        assert log_path.exists() is True
        has_file_handler = any(
            isinstance(handler, logging.FileHandler) for handler in client_instance.logger.handlers
        )
        assert has_file_handler
    finally:
        remove_file_handlers(client_instance.logger)


def test_client_file_logging_opt_in_uses_existing_log_file(
    configuration: Configuration,
    template_manager: TemplateManager,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    log_path = tmp_path / "macpymessenger.log"
    log_path.write_text("preexisting content", encoding="utf-8")
    logger = logging.getLogger("macpymessenger.client")
    remove_file_handlers(logger)
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=StubRunner(),
        file_logging=FileLoggingConfiguration(),
    )
    try:
        assert log_path.exists() is True
        has_file_handler = any(
            isinstance(handler, logging.FileHandler) for handler in client_instance.logger.handlers
        )
        assert has_file_handler
    finally:
        remove_file_handlers(client_instance.logger)


def test_client_file_logging_uses_custom_path(
    configuration: Configuration,
    template_manager: TemplateManager,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    custom_path = tmp_path / "logs" / "custom.log"
    custom_path.parent.mkdir()
    logger = logging.getLogger("macpymessenger.client")
    remove_file_handlers(logger)
    client_instance = IMessageClient(
        configuration=configuration,
        template_manager=template_manager,
        command_runner=StubRunner(),
        file_logging=FileLoggingConfiguration(custom_path),
    )
    try:
        assert custom_path.exists() is True
        file_handlers = [
            handler
            for handler in client_instance.logger.handlers
            if isinstance(handler, logging.FileHandler)
        ]
        assert file_handlers
        assert Path(file_handlers[0].baseFilename) == custom_path
    finally:
        remove_file_handlers(client_instance.logger)


def test_client_file_logging_raises_configuration_error_on_oserror(
    configuration: Configuration,
    template_manager: TemplateManager,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    log_directory = tmp_path / "logs"
    log_directory.mkdir()
    logger = logging.getLogger("macpymessenger.client")
    remove_file_handlers(logger)
    with pytest.raises(ConfigurationError, match="Unable to configure file logging"):
        IMessageClient(
            configuration=configuration,
            template_manager=template_manager,
            command_runner=StubRunner(),
            file_logging=FileLoggingConfiguration(log_directory),
        )
