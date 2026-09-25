from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class CardBtopProcess:
    pid: int
    program: str
    arguments: str
    cpu: float
    starved: bool = False
