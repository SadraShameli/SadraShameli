from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class CardBtopGauge:
    label: str
    value: int
