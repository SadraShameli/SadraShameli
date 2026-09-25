from readme.logger.logger_base import LoggerBase
from readme.logger.manager import LOGGER_ROOT_NAME


def test_subclasses_get_a_logger_named_after_the_class() -> None:
    class LoggerBaseProbe(LoggerBase):
        pass

    assert LoggerBaseProbe.logger.name == f"{LOGGER_ROOT_NAME}.LoggerBaseProbe"
    assert LoggerBaseProbe().logger is LoggerBaseProbe.logger
