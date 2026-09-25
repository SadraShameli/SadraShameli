from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar

from readme.card.card_base import CardBase
from readme.card.enum import CardEnumLayout
from readme.card.picture import CardPicture
from readme.card.project.enum import CardProjectEnumStyle
from readme.card.project.info import CardProjectInfo
from readme.card.project.style import CardProjectStyle
from readme.photo.enum import PhotoEnumName
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont
from readme.svg.font import SvgFont
from readme.svg.showcase import SvgShowcase
from readme.svg.util import esc


@dataclass(kw_only=True, slots=True)
class CardTileBase(CardBase):
    LAYOUT: ClassVar[CardEnumLayout] = CardEnumLayout.TILE
    WIDTH: ClassVar[int] = 490
    HEIGHT: ClassVar[int] = 452
    IMAGE_HEIGHT: ClassVar[int] = 250
    PADDING: ClassVar[int] = 28
    DESCRIPTION_LINES: ClassVar[int] = 4
    INFO: ClassVar[CardProjectInfo]
    PHOTO: ClassVar[PhotoEnumName]
    HREF: ClassVar[str]
    LINK: ClassVar[str]

    @classmethod
    def markup(cls, pictures: Mapping[str, CardPicture]) -> str:
        return pictures[cls.NAME].tile(href=cls.HREF, alt=cls.ALT)

    def render(self) -> SvgDocument:
        t, info = self.theme, self.INFO
        w, h, ih = self.WIDTH, self.HEIGHT, self.IMAGE_HEIGHT
        x, right = self.PADDING, w - self.PADDING
        body = [
            self.frame(h).open(t),
            SvgShowcase(
                photo=self.context.repository.photo(self.PHOTO),
                width=w,
                height=ih,
            ).render(t),
            f'<line x1="0" y1="{ih}" x2="{w}" y2="{ih}" stroke="{t.border}"/>',
            (
                f'<text x="{x}" y="{ih + 38}" class="{CardProjectEnumStyle.EYEBROW}" font-size="11">'
                f"{esc(info.eyebrow)}</text>"
            ),
            (
                f'<text x="{x - 1}" y="{ih + 74}" class="{CardProjectEnumStyle.TITLE}" font-size="24">'
                f"{esc(info.title)}</text>"
            ),
            (
                f'<text x="{right}" y="{ih + 74}" class="{CardProjectEnumStyle.EYEBROW}" text-anchor="end">'
                f"{esc(info.period)}</text>"
            ),
        ]
        y = ih + 104

        for line in SvgFont.wrap(
            info.description, SvgEnumFont.SANS_REGULAR, 15, right - x
        )[: self.DESCRIPTION_LINES]:
            body.append(
                f'<text x="{x}" y="{y}" class="{CardProjectEnumStyle.DESCRIPTION}" font-size="15">'
                f"{esc(line)}</text>"
            )
            y += 21

        body.append(
            f'<text x="{x}" y="{h - 24}" class="{CardProjectEnumStyle.LINK}">{esc(self.LINK)}</text>'
        )
        body.append("</g>")

        return SvgDocument(
            width=w,
            height=h,
            body="".join(body),
            css=CardProjectStyle.css(t),
            title=info.title,
            description=info.description,
        )
