from collections.abc import Mapping
from dataclasses import dataclass
from itertools import batched, groupby

from readme.card.card_base import CardBase
from readme.card.constants import (
    CARD_README_HEADER,
    CARD_README_SPACER,
    CARD_README_TILES_PER_ROW,
)
from readme.card.enum import CardEnumLayout
from readme.card.picture import CardPicture


@dataclass(kw_only=True, frozen=True, slots=True)
class CardPage:
    cards: tuple[type[CardBase], ...]
    pictures: Mapping[str, CardPicture]

    def render(self) -> str:
        blocks: list[str] = []

        for layout, group in groupby(self.cards, key=lambda card: card.LAYOUT):
            cards = tuple(group)

            match layout:
                case CardEnumLayout.TILE:
                    blocks += self._spacer(cards[0])
                    blocks.append(self._tiles(cards))
                case CardEnumLayout.BLOCK:
                    for card in cards:
                        blocks += self._spacer(card)
                        blocks.append(card.markup(self.pictures))

        return CARD_README_HEADER + "\n\n".join(blocks) + "\n"

    @staticmethod
    def _spacer(card: type[CardBase]) -> list[str]:
        return [CARD_README_SPACER] if card.SPACED else []

    def _tiles(self, cards: tuple[type[CardBase], ...]) -> str:
        return "\n".join(
            "<p>\n"
            + "".join(f"  {card.markup(self.pictures)}\n" for card in row)
            + "</p>"
            for row in batched(cards, CARD_README_TILES_PER_ROW, strict=False)
        )
