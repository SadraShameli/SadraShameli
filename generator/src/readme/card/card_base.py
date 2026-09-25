from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from readme.card.constants import (
    CARD_RADIUS,
    CARD_README_WIDTH_FULL,
    CARD_WIDTH,
)
from readme.card.context import CardContext
from readme.card.enum import (
    CardEnumDiscoveryFile,
    CardEnumLayout,
    CardEnumName,
)
from readme.card.picture import CardPicture
from readme.dock.dock import Dock
from readme.plugin.plugin_base import PluginBase
from readme.plugin.registry import PluginRegistry
from readme.svg.document import SvgDocument
from readme.svg.frame import SvgFrame
from readme.svg.theme import SvgTheme
from readme.svg.util import esc

CARD_REGISTRY: PluginRegistry[CardEnumName, CardBase] = PluginRegistry(
    enum=CardEnumName,
    package=__name__.rpartition(".")[0],
    anchor=Path(__file__).resolve().parent,
    file=CardEnumDiscoveryFile.CARD,
)


@dataclass(kw_only=True, slots=True)
class CardBase(PluginBase, ABC, registry=CARD_REGISTRY):
    NAME: ClassVar[CardEnumName]
    ALT: ClassVar[str]
    DOCK: ClassVar[Dock | None] = None
    LAYOUT: ClassVar[CardEnumLayout] = CardEnumLayout.BLOCK
    SPACED: ClassVar[bool] = False
    WIDTH: ClassVar[int] = CARD_WIDTH
    RADIUS: ClassVar[int] = CARD_RADIUS

    context: CardContext

    @property
    def theme(self) -> SvgTheme:
        return self.context.theme

    def frame(self, height: float) -> SvgFrame:
        return SvgFrame(
            width=self.WIDTH,
            height=height,
            radius=self.RADIUS,
            open_bottom=self.DOCK is not None,
        )

    def documents(self) -> dict[str, SvgDocument]:
        documents = {str(self.NAME): self.render()}

        if self.DOCK is not None:
            documents |= {
                stem: button.render(self.theme)
                for stem, button in self.DOCK.buttons(
                    card=self.NAME, width=self.WIDTH, radius=self.RADIUS
                ).items()
            }

        return documents

    @abstractmethod
    def render(self) -> SvgDocument: ...

    @classmethod
    def markup(cls, pictures: Mapping[str, CardPicture]) -> str:
        picture = pictures[cls.NAME]

        if (dock := cls.DOCK) is None:
            return picture.block(alt=cls.ALT)

        lines = [
            f'<a href="{esc(dock.href)}">{picture.inline(alt=cls.ALT, width=CARD_README_WIDTH_FULL)}</a><br>'
        ]
        last_row = len(dock.rows) - 1

        for row, links in enumerate(dock.rows):
            cell_width = dock.cell_width(links)
            cells = "".join(
                f'<a href="{esc(link.href)}">'
                f"{pictures[dock.stem(cls.NAME, row, column)].inline(alt=link.label, width=cell_width)}</a>"
                for column, link in enumerate(links)
            )
            lines.append(cells + ("<br>" if row < last_row else ""))

        return "<p>\n" + "\n".join(lines) + "\n</p>"
