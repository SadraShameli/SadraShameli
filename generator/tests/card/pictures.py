from readme.card.card_base import CardBase
from readme.card.picture import CardPicture
from readme.dock.dock import Dock


def pictures_for(cards: tuple[type[CardBase], ...]) -> dict[str, CardPicture]:
    stems = [
        stem
        for card in cards
        for stem in (
            card.NAME,
            *(
                Dock.stem(card.NAME, row, column)
                for row, links in enumerate(
                    card.DOCK.rows if card.DOCK else ()
                )
                for column, _ in enumerate(links)
            ),
        )
    ]

    return {
        stem: CardPicture(dark=f"{stem}-dark.svg", light=f"{stem}-light.svg")
        for stem in stems
    }
