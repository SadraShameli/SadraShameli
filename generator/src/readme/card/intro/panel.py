from dataclasses import dataclass
from typing import ClassVar

from readme.svg.box import SvgBox
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.theme import SvgTheme
from readme.svg.util import esc


@dataclass(kw_only=True, frozen=True, slots=True)
class CardIntroPanel:
    TEXT_X: ClassVar[int] = 88
    LINES: ClassVar[int] = 2

    box: SvgBox
    label: str
    title: str
    body: str
    icon: str
    reserve_right: float = 24

    def render(self, theme: SvgTheme) -> str:
        x, y, w, h = self.box.x, self.box.y, self.box.width, self.box.height
        tx = x + self.TEXT_X
        mono = SvgEnumFontFamily.MONO.stack
        sans = SvgEnumFontFamily.SANS.stack
        lines = SvgFont.wrap(
            self.body,
            SvgEnumFont.SANS_REGULAR,
            14,
            w - self.TEXT_X - self.reserve_right,
        )[: self.LINES]

        return (
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{theme.panel}" stroke="{theme.border}"/>'
            + self.icon
            + f'<text x="{tx}" y="{y + 32}" font-family="{mono}" font-size="11" letter-spacing="2" '
            f'fill="{theme.muted}">{esc(self.label)}</text>'
            + f'<text x="{tx}" y="{y + 60}" font-family="{sans}" font-size="19" font-weight="600" '
            f'fill="{theme.text}">{esc(self.title)}</text>'
            + "".join(
                f'<text x="{tx}" y="{y + 86 + i * 20}" font-family="{sans}" font-size="14" '
                f'fill="{theme.muted}">{esc(line)}</text>'
                for i, line in enumerate(lines)
            )
        )
