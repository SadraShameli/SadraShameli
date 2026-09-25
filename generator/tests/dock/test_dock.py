from readme.dock.dock import Dock
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink

LINK = DockLink(label="x", href="https://example.com", icon=DockEnumIcon.GLOBE)


def test_buttons_know_their_place_in_the_grid() -> None:
    dock = Dock(href="https://example.com", rows=((LINK, LINK, LINK), (LINK,)))
    buttons = dock.buttons(card="card", width=900, radius=16)

    assert list(buttons) == [
        "dock/card-0-0",
        "dock/card-0-1",
        "dock/card-0-2",
        "dock/card-1-0",
    ]
    assert [button.width for button in buttons.values()] == [
        300,
        300,
        300,
        900,
    ]
    assert buttons["dock/card-0-0"].first
    assert not buttons["dock/card-0-0"].bottom
    assert buttons["dock/card-0-2"].last
    assert buttons["dock/card-1-0"].first
    assert buttons["dock/card-1-0"].last
    assert buttons["dock/card-1-0"].bottom


def test_cell_width_splits_the_row_evenly() -> None:
    assert Dock.cell_width((LINK,)) == "100%"
    assert Dock.cell_width((LINK, LINK)) == "50%"
    assert Dock.cell_width((LINK, LINK, LINK)) == "33.3333%"
