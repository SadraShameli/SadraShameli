from dataclasses import dataclass
from typing import ClassVar

from readme.dock.constants import DOCK_HEIGHT
from readme.dock.icon import DockIcon
from readme.dock.link import DockLink
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.theme import SvgTheme
from readme.svg.util import esc


@dataclass(kw_only=True, frozen=True, slots=True)
class DockButton:
    FONT: ClassVar[SvgEnumFont] = SvgEnumFont.MONO_REGULAR
    FONT_SIZE: ClassVar[int] = 14
    GAP: ClassVar[int] = 10
    ARROW: ClassVar[str] = "↗"
    ARROW_WIDTH: ClassVar[int] = 9

    link: DockLink
    width: float
    radius: int
    first: bool
    last: bool
    bottom: bool

    def render(self, theme: SvgTheme) -> SvgDocument:
        w, h = self.width, DOCK_HEIGHT
        label_w = SvgFont.measure(self.link.label, self.FONT, self.FONT_SIZE)
        content_w = (
            DockIcon.SIZE + self.GAP + label_w + self.GAP + self.ARROW_WIDTH
        )
        x = (w - content_w) / 2
        cy = h / 2
        text_x = x + (DockIcon.SIZE + self.GAP)
        mono = SvgEnumFontFamily.MONO.stack
        body = (
            self._fill(theme)
            + DockIcon(
                icon=self.link.icon, x=x, center_y=cy, color=theme.text
            ).render()
            + f'<text x="{text_x:.1f}" y="{cy + 5:.1f}" font-family="{mono}" font-size="{self.FONT_SIZE}" fill="{theme.text}">'
            f"{esc(self.link.label)}</text>"
            + f'<text x="{text_x + label_w + self.GAP:.1f}" y="{cy + 5:.1f}" font-family="{mono}" font-size="{self.FONT_SIZE}" '
            f'fill="{theme.faint}">{self.ARROW}</text>' + self._edges(theme)
        )

        return SvgDocument(
            width=w,
            height=h,
            body=body,
            css=SvgFont.css(self.FONT),
            title=self.link.label,
        )

    @property
    def radius_left(self) -> int:
        return self.radius if self.first and self.bottom else 0

    @property
    def radius_right(self) -> int:
        return self.radius if self.last and self.bottom else 0

    def _fill(self, theme: SvgTheme) -> str:
        w, h = self.width, DOCK_HEIGHT
        rl, rr = self.radius_left, self.radius_right

        return (
            f'<path d="M0 0H{w:.2f}V{h - rr}'
            + (f"A{rr} {rr} 0 0 1 {w - rr:.2f} {h}" if rr else "")
            + f"H{rl}"
            + (f"A{rl} {rl} 0 0 1 0 {h - rl}" if rl else f"L0 {h}")
            + f'Z" fill="{theme.panel}"/>'
        )

    def _edges(self, theme: SvgTheme) -> str:
        w, h = self.width, DOCK_HEIGHT
        rl, rr = self.radius_left, self.radius_right
        edges = [f'<path d="M0 .5H{w:.2f}" stroke="{theme.border}"/>']

        if self.first:
            edges.append(
                f'<path d="M.5 0V{h - rl}'
                + (
                    f"A{rl - 0.5} {rl - 0.5} 0 0 0 {rl} {h - 0.5}"
                    if rl
                    else ""
                )
                + f'" fill="none" stroke="{theme.border}"/>'
            )

        edges.append(
            f'<path d="M{w - 0.5:.2f} 0V{h - rr}'
            + (
                f"A{rr - 0.5} {rr - 0.5} 0 0 1 {w - rr:.2f} {h - 0.5}"
                if rr
                else ""
            )
            + f'" fill="none" stroke="{theme.border}"/>'
        )

        if self.bottom:
            edges.append(
                f'<path d="M{rl} {h - 0.5}H{w - rr:.2f}" stroke="{theme.border}"/>'
            )

        return "".join(edges)
