import base64
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from readme.svg.box import SvgBox
from readme.svg.constants import SVG_COLOR_BLACK, SVG_JPEG_DATA_PREFIX
from readme.svg.theme import SvgTheme


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgPhoto:
    path: Path
    box: SvgBox
    clip: str | None = None
    grain: bool = True

    @staticmethod
    @cache
    def data_uri(path: Path) -> str:
        return (
            SVG_JPEG_DATA_PREFIX + base64.b64encode(path.read_bytes()).decode()
        )

    def render(self, theme: SvgTheme) -> str:
        x, y, w, h = self.box.x, self.box.y, self.box.width, self.box.height
        uid = f"{x:.0f}-{y:.0f}-{w:.0f}"
        box = f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"'
        clip = f' clip-path="url(#{self.clip})"' if self.clip else ""
        photo = (
            f'<image href="{self.data_uri(self.path)}" {box} preserveAspectRatio="xMidYMid slice"{clip}/>'
            f'<rect {box} fill="{SVG_COLOR_BLACK}" fill-opacity="{theme.photo_dim}"{clip}/>'
        )

        if not self.grain:
            return photo

        return (
            f'<defs><filter id="gr{uid}" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" stitchTiles="stitch"/>'
            '<feColorMatrix type="saturate" values="0"/></filter></defs>'
            + photo
            + f'<rect {box} filter="url(#gr{uid})" opacity="{theme.photo_grain}" '
            f'style="mix-blend-mode:overlay"{clip}/>'
        )
