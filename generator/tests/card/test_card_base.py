from xml.etree import ElementTree

from readme.card.card_base import CardBase
from readme.card.constants import CARD_README_WIDTH_FULL
from readme.card.context import CardContext
from readme.card.enum import CardEnumName
from tests.card.pictures import pictures_for


def test_every_card_name_has_a_registered_card(
    cards: tuple[type[CardBase], ...],
) -> None:
    assert [card.NAME for card in cards] == list(CardEnumName)


def test_every_card_renders_well_formed_svg(
    cards: tuple[type[CardBase], ...], context: CardContext
) -> None:
    for card in cards:
        for stem, document in card(context=context).documents().items():
            root = ElementTree.fromstring(document.render())

            assert root.get("width"), stem


def test_docked_cards_render_one_button_per_link(
    cards: tuple[type[CardBase], ...], context: CardContext
) -> None:
    for card in cards:
        links = sum(len(row) for row in card.DOCK.rows) if card.DOCK else 0

        assert len(card(context=context).documents()) == 1 + links


def test_docked_markup_has_no_whitespace_between_buttons(
    cards: tuple[type[CardBase], ...],
) -> None:
    pictures = pictures_for(cards)

    for card in cards:
        if card.DOCK is None:
            continue

        markup = card.markup(pictures)
        rows = markup.removeprefix("<p>\n").removesuffix("\n</p>").split("\n")

        assert f'width="{CARD_README_WIDTH_FULL}"' in rows[0]
        assert len(rows) == 1 + len(card.DOCK.rows)
        assert all(" <a" not in row and "> <" not in row for row in rows)
