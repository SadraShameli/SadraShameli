from dataclasses import dataclass

from readme.svg.constants import SVG_NAMESPACE, SVG_REDUCED_MOTION_CSS
from readme.svg.util import esc


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgDocument:
    width: float
    height: float
    body: str
    css: str
    title: str
    description: str = ""

    def render(self) -> str:
        w, h = self.width, self.height
        description = (
            f"<desc>{esc(self.description)}</desc>" if self.description else ""
        )

        return (
            f'<svg xmlns="{SVG_NAMESPACE}" width="{w:g}" height="{h:g}" '
            f'viewBox="0 0 {w:g} {h:g}" role="img" aria-labelledby="t">'
            f'<title id="t">{esc(self.title)}</title>{description}'
            f"<style>{self.css}{SVG_REDUCED_MOTION_CSS}</style>{self.body}</svg>\n"
        )
