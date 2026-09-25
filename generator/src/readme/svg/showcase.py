from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from readme.svg.box import SvgBox
from readme.svg.constants import (
    SVG_COLOR_BLACK,
    SVG_COLOR_WHITE,
    SVG_SHOWCASE_RATIO,
)
from readme.svg.photo import SvgPhoto
from readme.svg.theme import SvgTheme


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgShowcase:
    INSET_X: ClassVar[int] = 36
    INSET_Y: ClassVar[int] = 30
    BLEED: ClassVar[int] = 20
    GRID: ClassVar[int] = 24
    PLUS_SIZE: ClassVar[int] = 6
    PLUS_OPACITY: ClassVar[float] = 0.8

    photo: Path
    width: float
    height: float
    ratio: float = SVG_SHOWCASE_RATIO
    overlay: str = ""

    @classmethod
    def shot(cls, *, width: float, height: float, ratio: float) -> SvgBox:
        shot_width = width - 2 * cls.INSET_X

        return SvgBox(
            x=cls.INSET_X,
            y=cls.INSET_Y,
            width=shot_width,
            height=max(shot_width / ratio, height - cls.INSET_Y + cls.BLEED),
        )

    @classmethod
    def plus(cls, x: float, y: float, color: str) -> str:
        size = cls.PLUS_SIZE

        return (
            f'<path d="M{x - size:.1f} {y:.1f}H{x + size:.1f}M{x:.1f} {y - size:.1f}V{y + size:.1f}" '
            f'stroke="{color}" stroke-opacity="{cls.PLUS_OPACITY}" stroke-width="1.2"/>'
        )

    def render(self, theme: SvgTheme) -> str:
        w, h, grid, bleed = self.width, self.height, self.GRID, self.BLEED
        shot = self.shot(width=w, height=h, ratio=self.ratio)
        sx, sy, sw, sh = shot.x, shot.y, shot.width, shot.height
        spot, spot_opacity = theme.showcase_spot, theme.showcase_spot_opacity
        overlay = (
            f'<g clip-path="url(#shot)">{self.overlay}</g>'
            if self.overlay
            else ""
        )

        return "".join(
            (
                (
                    "<defs>"
                    f'<clipPath id="area"><rect width="{w}" height="{h}"/></clipPath>'
                    f'<clipPath id="shot"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh + bleed:.1f}" rx="10"/></clipPath>'
                    f'<pattern id="grid" width="{grid}" height="{grid}" patternUnits="userSpaceOnUse" x="{sx % grid}" y="{sy % grid}">'
                    f'<path d="M{grid} 0H0V{grid}" fill="none" stroke="{theme.border}" stroke-width="1"/></pattern>'
                    f'<radialGradient id="gridfade" cx="50%" cy="20%" r="75%"><stop offset="0" stop-color="{SVG_COLOR_WHITE}"/>'
                    f'<stop offset="1" stop-color="{SVG_COLOR_WHITE}" stop-opacity="0"/></radialGradient>'
                    f'<mask id="gridmask"><rect width="{w}" height="{h}" fill="url(#gridfade)"/></mask>'
                    f'<radialGradient id="spot" cx="50%" cy="0%" r="70%"><stop offset="0" stop-color="{spot}" '
                    f'stop-opacity="{spot_opacity}"/><stop offset="1" stop-color="{spot}" stop-opacity="0"/></radialGradient>'
                    '<filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feGaussianBlur stdDeviation="12"/></filter>'
                    "</defs>"
                    '<g clip-path="url(#area)">'
                    f'<rect width="{w}" height="{h}" fill="{theme.panel}"/>'
                    f'<rect width="{w}" height="{h}" fill="url(#grid)" mask="url(#gridmask)" opacity=".7"/>'
                    f'<rect width="{w}" height="{h}" fill="url(#spot)"/>'
                    f'<path d="M{sx} 0V{h}M{sx + sw} 0V{h}M0 {sy}H{w}" stroke="{theme.faint}" stroke-opacity=".5" '
                    f'stroke-dasharray="3 4"/>'
                    f'<rect x="{sx + 6}" y="{sy + 14}" width="{sw - 12}" height="{sh}" rx="10" fill="{SVG_COLOR_BLACK}" '
                    f'fill-opacity=".45" filter="url(#shadow)"/>'
                ),
                SvgPhoto(
                    path=self.photo, box=shot, clip="shot", grain=False
                ).render(theme),
                overlay,
                (
                    f'<rect x="{sx + 0.5}" y="{sy + 0.5}" width="{sw - 1}" height="{sh + bleed:.1f}" rx="10" fill="none" '
                    f'stroke="{theme.showcase_frame}" stroke-opacity="{theme.showcase_frame_opacity}"/>'
                ),
                self.plus(sx, sy, theme.muted),
                self.plus(sx + sw, sy, theme.muted),
                "</g>",
            )
        )
