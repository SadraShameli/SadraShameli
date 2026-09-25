from readme.card.card_base import CardBase
from readme.card.constants import (
    CARD_README_HEADER,
    CARD_README_SPACER,
    CARD_README_TILES_PER_ROW,
)
from readme.card.enum import CardEnumLayout
from readme.card.page import CardPage
from tests.card.pictures import pictures_for


def test_page_starts_with_the_header_and_lists_every_card(
    cards: tuple[type[CardBase], ...],
) -> None:
    pictures = pictures_for(cards)
    page = CardPage(cards=cards, pictures=pictures).render()

    assert page.startswith(CARD_README_HEADER)
    assert page.endswith("</p>\n")
    assert all(f"{card.NAME}-dark.svg" in page for card in cards)


def test_spacers_precede_spaced_cards(
    cards: tuple[type[CardBase], ...],
) -> None:
    page = CardPage(cards=cards, pictures=pictures_for(cards)).render()

    assert page.count(f"\n\n{CARD_README_SPACER}\n\n") == sum(
        card.SPACED for card in cards
    )


def test_tiles_share_rows(cards: tuple[type[CardBase], ...]) -> None:
    tiles = [card for card in cards if card.LAYOUT is CardEnumLayout.TILE]
    page = CardPage(cards=cards, pictures=pictures_for(cards)).render()

    for first in range(0, len(tiles), CARD_README_TILES_PER_ROW):
        row = tiles[first : first + CARD_README_TILES_PER_ROW]
        start = page.index(f"{row[0].NAME}-dark.svg")
        end = page.index("</p>", start)

        assert all(
            start <= page.index(f"{tile.NAME}-dark.svg") < end for tile in row
        )
