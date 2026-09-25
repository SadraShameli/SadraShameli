from enum import StrEnum, auto


class CardProjectTradingbotEnumStage(StrEnum):
    DATA = "data"
    FEAT = "feat"
    SCORE = "score"
    CHECK = "check"
    RISK = "risk"
    ORDER = "order"


class CardProjectTradingbotEnumTone(StrEnum):
    TEXT = auto()
    DIM = auto()
    GOOD = auto()
    BAD = auto()
