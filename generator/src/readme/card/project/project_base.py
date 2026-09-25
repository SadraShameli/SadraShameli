from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from readme.card.card_base import CardBase
from readme.card.project.enum import CardProjectEnumStyle
from readme.card.project.info import CardProjectInfo
from readme.card.project.style import CardProjectStyle
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont
from readme.svg.font import SvgFont
from readme.svg.fragment import SvgFragment
from readme.svg.util import esc


@dataclass(kw_only=True, slots=True)
class CardProjectBase(CardBase):
    INFO: ClassVar[CardProjectInfo]
    HEIGHT: ClassVar[int] = 320
    PANEL_WIDTH: ClassVar[int] = 400
    SPEC_CHAR_WIDTH: ClassVar[float] = 7.8

    @abstractmethod
    def visual(self) -> SvgFragment: ...

    def render(self) -> SvgDocument:
        t, info = self.theme, self.INFO
        w, h, pw = self.WIDTH, self.HEIGHT, self.PANEL_WIDTH
        visual = self.visual()
        x, right = pw + 44, w - 40
        body = [
            self.frame(h).open(t),
            visual.body,
            f'<line x1="{pw}" y1="0" x2="{pw}" y2="{h}" stroke="{t.border}"/>',
            f'<text x="{x}" y="58" class="{CardProjectEnumStyle.EYEBROW}">{esc(info.eyebrow)}</text>',
            (
                f'<text x="{right}" y="58" class="{CardProjectEnumStyle.EYEBROW}" text-anchor="end">'
                f"{esc(info.period)}</text>"
            ),
            (
                f'<text x="{x - 2}" y="104" class="{CardProjectEnumStyle.TITLE}" font-size="34">'
                f"{esc(info.title)}</text>"
            ),
        ]
        y = 138

        for line in SvgFont.wrap(
            info.description, SvgEnumFont.SANS_REGULAR, 16, right - x
        ):
            body.append(
                f'<text x="{x}" y="{y}" class="{CardProjectEnumStyle.DESCRIPTION}">{esc(line)}</text>'
            )
            y += 23

        y += 12
        key_w = max((len(spec.key) for spec in info.specs), default=0) + 2

        for spec in info.specs:
            body.append(
                f'<text x="{x}" y="{y}"><tspan class="{CardProjectEnumStyle.SPEC_KEY}">{esc(spec.key)}</tspan>'
                f'<tspan class="{CardProjectEnumStyle.SPEC_VALUE}" x="{x + key_w * self.SPEC_CHAR_WIDTH:.1f}">'
                f"{esc(spec.value)}</tspan></text>"
            )
            y += 22

        body.append("</g>")

        return SvgDocument(
            width=w,
            height=h,
            body="".join(body),
            css=CardProjectStyle.css(t) + visual.css,
            title=info.title,
            description=info.description,
        )
