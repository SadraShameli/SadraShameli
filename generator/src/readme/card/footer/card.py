from dataclasses import dataclass
from typing import ClassVar

from readme.card.card_base import CardBase
from readme.card.constants import CARD_TERMINAL_RADIUS
from readme.card.enum import CardEnumName
from readme.svg.constants import SVG_MONO_ADVANCE
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.util import esc


@dataclass(kw_only=True, slots=True)
class CardFooter(CardBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.FOOTER
    ALT: ClassVar[str] = (
        "~ $ exit. logout. thanks for scrolling, come say hi at sadra.nl"
    )
    SPACED: ClassVar[bool] = True
    RADIUS: ClassVar[int] = CARD_TERMINAL_RADIUS
    HEIGHT: ClassVar[int] = 132
    FONT_SIZE: ClassVar[int] = 16
    CHAR_WIDTH: ClassVar[float] = FONT_SIZE * SVG_MONO_ADVANCE
    COMMAND: ClassVar[str] = "exit"
    MESSAGE: ClassVar[str] = "logout. thanks for scrolling, come say hi at "
    SITE: ClassVar[str] = "sadra.nl"
    TYPE_ON: ClassVar[float] = 0.6
    TYPE_STEP: ClassVar[float] = 0.12

    def render(self) -> SvgDocument:
        t, w, h = self.theme, self.WIDTH, self.HEIGHT
        size, cw = self.FONT_SIZE, self.CHAR_WIDTH
        x0, y1, y2 = 36, 56, 88
        css = [
            SvgFont.css(SvgEnumFont.MONO_REGULAR),
            f"text{{font-family:{SvgEnumFontFamily.MONO.stack};font-size:{size}px}}",
            "@keyframes in{from{opacity:0}to{opacity:1}}",
            "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}",
        ]
        body = [
            self.frame(h).open(t),
            f'<text x="{x0}" y="{y1}"><tspan fill="{t.green}">~</tspan><tspan fill="{t.muted}"> $ </tspan></text>',
        ]

        for i, char in enumerate(self.COMMAND):
            css.append(
                f".e{i}{{animation:in .01s linear {self.TYPE_ON + i * self.TYPE_STEP:.2f}s both}}"
            )
            body.append(
                f'<text x="{x0 + (4 + i) * cw:.1f}" y="{y1}" fill="{t.text}" class="e{i}">{char}</text>'
            )

        out_d = self.TYPE_ON + len(self.COMMAND) * self.TYPE_STEP + 0.4
        css.append(f".o{{animation:in .3s ease-out {out_d:.2f}s both}}")
        body.append(
            f'<text x="{x0}" y="{y2}" class="o" fill="{t.muted}">{esc(self.MESSAGE)}'
            f'<tspan fill="{t.text}">{self.SITE}</tspan></text>'
        )
        body.append(
            f'<text x="{w - x0}" y="{y2}" class="o" text-anchor="end" fill="{t.faint}" font-size="13">'
            "[process completed]</text>"
        )
        cur_x = x0 + (len(self.MESSAGE) + len(self.SITE) + 1) * cw
        css.append(f".cu{{animation:in .01s linear {out_d + 0.3:.2f}s both}}")
        body.append(
            f'<g class="cu"><rect x="{cur_x:.1f}" y="{y2 - size * 0.82:.1f}" width="{cw * 0.9:.1f}" '
            f'height="{size * 1.05:.1f}" fill="{t.text}" style="animation:blink 1.05s step-end infinite"/></g>'
        )
        body.append("</g>")

        return SvgDocument(
            width=w,
            height=h,
            body="".join(body),
            css="".join(css),
            title="exit",
            description="logout. thanks for scrolling.",
        )
