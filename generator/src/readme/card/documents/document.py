import math
from dataclasses import dataclass
from typing import ClassVar

from readme.constants import BYTES_PER_KIB


@dataclass(kw_only=True, frozen=True, slots=True)
class CardDocumentsDocument:
    UNITS: ClassVar[tuple[str, ...]] = ("K", "M", "G")
    ONE_DECIMAL_BELOW: ClassVar[int] = 10

    file: str
    added: str
    note: str

    @classmethod
    def human_size(cls, size: int) -> str:
        value, unit = float(size), ""

        for bigger in cls.UNITS:
            if value < BYTES_PER_KIB:
                break

            value, unit = value / BYTES_PER_KIB, bigger

        if not unit:
            return str(size)

        if value < cls.ONE_DECIMAL_BELOW:
            return f"{math.ceil(value * 10) / 10:.1f}{unit}"

        return f"{math.ceil(value)}{unit}"
