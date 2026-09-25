import logging

from readme.logger.manager import (
    LOGGER_ROOT_NAME,
    configure_logger,
    get_logger,
)


def test_get_logger_nests_owners_under_the_package() -> None:
    assert get_logger().name == LOGGER_ROOT_NAME
    assert get_logger("Owner").name == f"{LOGGER_ROOT_NAME}.Owner"
    assert get_logger("Owner") is get_logger("Owner")


def test_configure_logger_attaches_one_stream_handler() -> None:
    configure_logger()
    configure_logger()

    handlers = get_logger().handlers
    assert len(handlers) == 1
    assert isinstance(handlers[0], logging.StreamHandler)
