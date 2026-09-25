from dataclasses import dataclass

from readme.card.constants import (
    CARD_README_DARK_MEDIA,
    CARD_README_WIDTH_FULL,
    CARD_README_WIDTH_TILE,
)
from readme.svg.util import esc


@dataclass(kw_only=True, frozen=True, slots=True)
class CardPicture:
    dark: str
    light: str

    def inline(self, *, alt: str, width: str) -> str:
        return (
            f'<picture><source media="{CARD_README_DARK_MEDIA}" srcset="{self.dark}">'
            f'<img align="top" alt="{esc(alt)}" src="{self.light}" width="{width}"></picture>'
        )

    def block(self, *, alt: str) -> str:
        return (
            "<p>\n<picture>\n"
            f'  <source media="{CARD_README_DARK_MEDIA}" srcset="{self.dark}">\n'
            f'  <img align="top" alt="{esc(alt)}" src="{self.light}" width="{CARD_README_WIDTH_FULL}">\n'
            "</picture>\n</p>"
        )

    def tile(self, *, href: str, alt: str) -> str:
        return (
            f'<a href="{esc(href)}"><picture><source media="{CARD_README_DARK_MEDIA}" srcset="{self.dark}">'
            f'<img alt="{esc(alt)}" src="{self.light}" width="{CARD_README_WIDTH_TILE}"></picture></a>'
        )
