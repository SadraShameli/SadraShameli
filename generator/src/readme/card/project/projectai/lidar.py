from dataclasses import dataclass
from typing import ClassVar

from readme.svg.fragment import SvgFragment


@dataclass(kw_only=True, frozen=True, slots=True)
class CardProjectProjectaiLidarHit:
    dx: int
    dy: int


@dataclass(kw_only=True, frozen=True, slots=True)
class CardProjectProjectaiLidar:
    RANGE: ClassVar[int] = 260
    RINGS: ClassVar[tuple[int, ...]] = (60, 120, 180, 240)
    HITS: ClassVar[tuple[CardProjectProjectaiLidarHit, ...]] = (
        CardProjectProjectaiLidarHit(dx=150, dy=-30),
        CardProjectProjectaiLidarHit(dx=95, dy=75),
        CardProjectProjectaiLidarHit(dx=210, dy=20),
        CardProjectProjectaiLidarHit(dx=175, dy=120),
        CardProjectProjectaiLidarHit(dx=60, dy=-110),
        CardProjectProjectaiLidarHit(dx=230, dy=-90),
        CardProjectProjectaiLidarHit(dx=120, dy=160),
        CardProjectProjectaiLidarHit(dx=40, dy=140),
    )
    GREEN: ClassVar[str] = "#4ade80"
    GREEN_LIGHT: ClassVar[str] = "#86efac"
    GREEN_DARK: ClassVar[str] = "#22c55e"

    cx: int
    cy: int

    def render(self) -> SvgFragment:
        cx, cy, r = self.cx, self.cy, self.RANGE
        rings = "".join(
            f'<circle cx="{cx}" cy="{cy}" r="{ring}" fill="none" stroke="{self.GREEN}" '
            f'stroke-opacity=".35" stroke-dasharray="2 5"/>'
            for ring in self.RINGS
        )
        sweep = (
            f'<g id="sweep"><path d="M{cx} {cy}L{cx + r} {cy}A{r} {r} 0 0 0 {cx + r * 0.866:.1f} '
            f'{cy - r * 0.5:.1f}Z" fill="url(#wedge)"/><line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" '
            f'stroke="{self.GREEN_LIGHT}" stroke-width="1.6"/></g>'
        )
        hits = "".join(
            f'<circle class="hit h{i}" cx="{cx + hit.dx}" cy="{cy + hit.dy}" r="3" fill="{self.GREEN}"/>'
            for i, hit in enumerate(self.HITS)
        )
        wedge = (
            '<linearGradient id="wedge" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{self.GREEN_DARK}" stop-opacity=".0"/>'
            f'<stop offset="1" stop-color="{self.GREEN_DARK}" stop-opacity=".45"/></linearGradient>'
        )

        return SvgFragment(
            body=f"<defs>{wedge}</defs>{rings}{sweep}{hits}",
            css="@keyframes sweep{to{transform:rotate(-360deg)}}"
            f"#sweep{{transform-origin:{cx}px {cy}px;animation:sweep 3s linear infinite}}"
            "@keyframes hit{0%{opacity:0}8%{opacity:1}60%,100%{opacity:0}}"
            ".hit{opacity:.0;animation:hit 3s linear infinite}"
            + "".join(
                f".h{i}{{animation-delay:{i * 0.37:.2f}s}}"
                for i in range(len(self.HITS))
            ),
        )
