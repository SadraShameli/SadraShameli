import logging

LOGGER_ROOT_NAME = "readme"
LOGGER_FORMAT = "%(name)s: %(message)s"


def get_logger(owner: str | None = None) -> logging.Logger:
    if owner is None:
        return logging.getLogger(LOGGER_ROOT_NAME)

    return logging.getLogger(f"{LOGGER_ROOT_NAME}.{owner}")


def configure_logger() -> None:
    logger = get_logger()

    if logger.handlers:
        return

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
