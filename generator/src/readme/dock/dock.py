from dataclasses import dataclass

from readme.dock.button import DockButton
from readme.dock.constants import DOCK_FOLDER
from readme.dock.link import DockLink


@dataclass(kw_only=True, frozen=True, slots=True)
class Dock:
    href: str
    rows: tuple[tuple[DockLink, ...], ...]

    @staticmethod
    def stem(card: str, row: int, column: int) -> str:
        return f"{DOCK_FOLDER}/{card}-{row}-{column}"

    @staticmethod
    def cell_width(links: tuple[DockLink, ...]) -> str:
        return f"{100 / len(links):.4f}".rstrip("0").rstrip(".") + "%"

    def buttons(
        self, *, card: str, width: float, radius: int
    ) -> dict[str, DockButton]:
        last_row = len(self.rows) - 1

        return {
            self.stem(card, row, column): DockButton(
                link=link,
                width=width / len(links),
                radius=radius,
                first=column == 0,
                last=column == len(links) - 1,
                bottom=row == last_row,
            )
            for row, links in enumerate(self.rows)
            for column, link in enumerate(links)
        }
