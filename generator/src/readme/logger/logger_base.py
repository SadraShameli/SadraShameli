import logging
from typing import ClassVar

from readme.logger.manager import get_logger


class LoggerBase:
    __slots__ = ()

    logger: ClassVar[logging.Logger]

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)

        cls.logger = get_logger(cls.__name__)
