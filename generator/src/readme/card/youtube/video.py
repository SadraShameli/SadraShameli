import math
from dataclasses import dataclass
from typing import ClassVar

from readme.photo.enum import PhotoEnumName


@dataclass(kw_only=True, frozen=True, slots=True)
class CardYoutubeVideo:
    THOUSAND: ClassVar[int] = 1000
    HUNDRED: ClassVar[int] = 100

    file: str
    title: str
    views: int
    date: str
    thumbnail: PhotoEnumName

    @property
    def views_label(self) -> str:
        if self.views >= self.THOUSAND:
            return f"{math.floor(self.views / self.HUNDRED) / 10:g}k+ views"

        if self.views >= self.HUNDRED:
            return f"{self.views // self.HUNDRED * self.HUNDRED}+ views"

        return f"{self.views} views"
