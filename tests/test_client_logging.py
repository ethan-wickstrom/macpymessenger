from __future__ import annotations

import logging

import macpymessenger
from macpymessenger import Configuration, IMessageClient, TemplateManager
from tests.support import StubRunner


def test_package_logger_has_only_a_null_handler() -> None:
    logger = logging.getLogger(macpymessenger.__name__)

    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.NullHandler)


def test_default_client_logger_does_not_configure_levels_or_handlers(
    configuration: Configuration,
    template_manager: TemplateManager,
) -> None:
    logger = logging.getLogger("macpymessenger.client")
    original_handlers = list(logger.handlers)
    original_level = logger.level
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)

    try:
        client = IMessageClient(
            configuration=configuration,
            template_manager=template_manager,
            command_runner=StubRunner(),
        )

        assert client.logger is logger
        assert client.logger.level == logging.NOTSET
        assert client.logger.handlers == []
    finally:
        logger.handlers[:] = original_handlers
        logger.setLevel(original_level)


def test_client_preserves_a_caller_owned_logger(
    configuration: Configuration,
    template_manager: TemplateManager,
) -> None:
    logger = logging.getLogger("tests.macpymessenger")
    handler = logging.NullHandler()
    logger.handlers[:] = [handler]
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    try:
        client = IMessageClient(
            configuration=configuration,
            template_manager=template_manager,
            command_runner=StubRunner(),
            logger=logger,
        )

        assert client.logger is logger
        assert client.logger.handlers == [handler]
        assert client.logger.level == logging.DEBUG
        assert client.logger.propagate is False
    finally:
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
