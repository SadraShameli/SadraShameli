from dataclasses import dataclass

from readme.svg.constants import SVG_CLIP_GROUP, SVG_CLIP_ID
from readme.svg.theme import SvgTheme


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgFrame:
    width: float
    height: float
    radius: int
    open_bottom: bool

    def open(self, theme: SvgTheme, defs: str = "") -> str:
        return (
            f"<defs>{self.clip_path()}{defs}</defs>"
            + self.outline(theme)
            + SVG_CLIP_GROUP
        )

    def outline(self, theme: SvgTheme) -> str:
        w, h, r = self.width, self.height, self.radius

        if not self.open_bottom:
            return (
                f'<rect x=".5" y=".5" width="{w - 1:g}" height="{h - 1:g}" rx="{r}" '
                f'fill="{theme.bg}" stroke="{theme.border}"/>'
            )

        ri = r - 0.5

        return (
            f'<path d="M0 {h:g}V{r}A{r} {r} 0 0 1 {r} 0H{w - r:g}A{r} {r} 0 0 1 {w:g} {r}V{h:g}Z" fill="{theme.bg}"/>'
            f'<path d="M.5 {h:g}V{r}A{ri} {ri} 0 0 1 {r} .5H{w - r:g}A{ri} {ri} 0 0 1 {w - 0.5:g} {r}V{h:g}" '
            f'fill="none" stroke="{theme.border}"/>'
        )

    def clip_path(self) -> str:
        w, h = self.width, self.height
        bottom = (
            f'<rect x="1" y="{h / 2:g}" width="{w - 2:g}" height="{h / 2:g}"/>'
            if self.open_bottom
            else ""
        )

        return (
            f'<clipPath id="{SVG_CLIP_ID}"><rect x="1" y="1" width="{w - 2:g}" height="{h - 2:g}" '
            f'rx="{self.radius - 1}"/>{bottom}</clipPath>'
        )
