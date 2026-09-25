from collections.abc import Iterator
from dataclasses import dataclass, field
from itertools import count
from typing import ClassVar

from readme.svg.constants import SVG_MONO_ADVANCE
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.frame import SvgFrame
from readme.svg.theme import SvgTheme
from readme.svg.util import esc


@dataclass(kw_only=True, slots=True)
class CardTerminal:
    TITLE_HEIGHT: ClassVar[int] = 44
    FONT_SIZE: ClassVar[int] = 14
    CHAR_WIDTH: ClassVar[float] = FONT_SIZE * SVG_MONO_ADVANCE
    TYPE_START: ClassVar[float] = 0.35
    TYPE_STEP: ClassVar[float] = 0.045
    BLINK: ClassVar[str] = "animation:blink 1.05s step-end infinite"

    theme: SvgTheme
    title: str
    body: list[str] = field(default_factory=list)
    css: list[str] = field(
        default_factory=lambda: [
            "@keyframes in{from{opacity:0}to{opacity:1}}",
            "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}",
        ]
    )
    appearances: Iterator[int] = field(default_factory=lambda: count(1))

    def appear(self, delay: float, duration: float = 0.01) -> str:
        n = next(self.appearances)
        self.css.append(
            f".a{n}{{animation:in {duration}s linear {delay:.2f}s both}}"
        )

        return f"a{n}"

    def prompt(self, x: float, y: float, cwd: str) -> float:
        self.body.append(
            f'<text x="{x}" y="{y}" xml:space="preserve"><tspan fill="{self.theme.green}">{esc(cwd)}</tspan>'
            f'<tspan fill="{self.theme.muted}"> $ </tspan></text>'
        )

        return x + (len(cwd) + 3) * self.CHAR_WIDTH

    def type_text(self, x: float, y: float, text: str, start: float) -> float:
        for i, char in enumerate(text):
            if char != " ":
                self.body.append(
                    f'<text x="{x + i * self.CHAR_WIDTH:.1f}" y="{y}" fill="{self.theme.text}" '
                    f'class="{self.appear(start + i * self.TYPE_STEP)}">{esc(char)}</text>'
                )

        return start + len(text) * self.TYPE_STEP

    def command(self, x: float, y: float, cwd: str, command: str) -> float:
        return self.type_text(
            self.prompt(x, y, cwd), y, command, self.TYPE_START
        )

    def cursor(self, x: float, y: float, delay: float) -> None:
        size, width = self.FONT_SIZE, self.CHAR_WIDTH
        self.body.append(
            f'<g class="{self.appear(delay)}"><rect x="{x:.1f}" y="{y - size * 0.82:.1f}" width="{width * 0.9:.1f}" '
            f'height="{size * 1.05:.1f}" fill="{self.theme.text}" style="{self.BLINK}"/></g>'
        )

    def render(
        self,
        *,
        frame: SvgFrame,
        fonts: tuple[SvgEnumFont, ...],
        description: str,
    ) -> SvgDocument:
        t, w, th = self.theme, frame.width, self.TITLE_HEIGHT
        mono = SvgEnumFontFamily.MONO.stack
        lights = "".join(
            f'<circle cx="{26 + i * 20}" cy="{th / 2}" r="6" fill="{color}"/>'
            for i, color in enumerate((t.red, t.yellow, t.green))
        )
        body = (
            frame.open(t)
            + f'<rect width="{w}" height="{th}" fill="{t.panel}"/>'
            + f'<line x1="0" y1="{th}" x2="{w}" y2="{th}" stroke="{t.border}"/>'
            + lights
            + f'<text x="{w / 2}" y="{th / 2 + 5}" text-anchor="middle" fill="{t.faint}" '
            f'font-family="{mono}" font-size="13">{esc(self.title)}</text>'
            + f'<g font-family="{mono}" font-size="{self.FONT_SIZE}">{"".join(self.body)}</g>'
            + "</g>"
        )

        return SvgDocument(
            width=w,
            height=frame.height,
            body=body,
            css=SvgFont.css(*fonts) + "".join(self.css),
            title=self.title,
            description=description,
        )
