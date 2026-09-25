from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgBox:
    x: float
    y: float
    width: float
    height: float
