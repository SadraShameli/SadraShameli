from dataclasses import dataclass
from typing import ClassVar

from readme.card.project.project_base import CardProjectBase
from readme.photo.constants import PHOTO_FRAME_FEATURED
from readme.photo.enum import PhotoEnumName
from readme.svg.box import SvgBox
from readme.svg.constants import SVG_COLOR_BLACK, SVG_COLOR_WHITE
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.fragment import SvgFragment
from readme.svg.showcase import SvgShowcase
from readme.svg.util import esc


@dataclass(kw_only=True, slots=True)
class CardProjectPhotoBase(CardProjectBase):
    PHOTO: ClassVar[PhotoEnumName]
    CHIP: ClassVar[str]
    CHIP_COLOR: ClassVar[str]
    CHIP_FONT_SIZE: ClassVar[int] = 11

    def overlay(self, shot: SvgBox) -> SvgFragment:
        return SvgFragment(body="")

    def visual(self) -> SvgFragment:
        pw, h = self.PANEL_WIDTH, self.HEIGHT
        ratio = PHOTO_FRAME_FEATURED.ratio
        shot = SvgShowcase.shot(width=pw, height=h, ratio=ratio)
        overlay = self.overlay(shot)
        showcase = SvgShowcase(
            photo=self.context.repository.photo(self.PHOTO),
            width=pw,
            height=h,
            ratio=ratio,
            overlay=overlay.body + self._chip(shot.x + 12, h - 38),
        )

        return SvgFragment(body=showcase.render(self.theme), css=overlay.css)

    def _chip(self, x: float, y: float) -> str:
        size = self.CHIP_FONT_SIZE
        w = SvgFont.measure(self.CHIP, SvgEnumFont.MONO_REGULAR, size, 1) + 30

        return (
            f'<rect x="{x}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{SVG_COLOR_BLACK}" '
            f'fill-opacity=".62" stroke="{SVG_COLOR_WHITE}" stroke-opacity=".18"/>'
            f'<circle cx="{x + 13}" cy="{y + 11}" r="3.5" fill="{self.CHIP_COLOR}" '
            'style="animation:blink 1.2s step-end infinite"/>'
            f'<text x="{x + 23}" y="{y + 15}" font-family="{SvgEnumFontFamily.MONO.stack}" '
            f'font-size="{size}" letter-spacing="1" fill="{SVG_COLOR_WHITE}">{esc(self.CHIP)}</text>'
        )
