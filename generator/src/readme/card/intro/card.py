from dataclasses import dataclass
from typing import ClassVar

from readme.card.card_base import CardBase
from readme.card.enum import CardEnumName
from readme.card.intro.panel import CardIntroPanel
from readme.svg.box import SvgBox
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.fragment import SvgFragment
from readme.svg.util import esc


@dataclass(kw_only=True, frozen=True, slots=True)
class CardIntroStage:
    name: str
    detail: str


@dataclass(kw_only=True, frozen=True, slots=True)
class CardIntroStar:
    dx: float
    dy: float
    delay: float


@dataclass(kw_only=True, frozen=True, slots=True)
class CardIntroCandle:
    top: float
    body: float


@dataclass(kw_only=True, slots=True)
class CardIntro(CardBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.INTRO
    ALT: ClassVar[str] = (
        "Hey, I'm Sadra, not Sandra. I like owning things end to end: C++ firmware on an ESP32, "
        "a tRPC and Postgres backend, the Next.js dashboard that plots it all, and the CI that keeps "
        "both honest. By day I'm a full-stack developer at Nobears in Rotterdam, shipping and "
        "maintaining 15+ WordPress platforms. By night I trade NQ futures and I'm teaching a Python "
        "engine to trade them with me."
    )
    HEIGHT: ClassVar[int] = 340
    MARGIN: ClassVar[int] = 32
    PIPELINE: ClassVar[tuple[CardIntroStage, ...]] = (
        CardIntroStage(name="firmware", detail="C++ on an ESP32"),
        CardIntroStage(name="backend", detail="tRPC + Postgres"),
        CardIntroStage(name="dashboard", detail="Next.js, plots it all"),
        CardIntroStage(name="ci", detail="keeps both honest"),
    )
    STARS: ClassVar[tuple[CardIntroStar, ...]] = (
        CardIntroStar(dx=-26, dy=-18, delay=0.0),
        CardIntroStar(dx=24, dy=-24, delay=0.7),
        CardIntroStar(dx=30, dy=14, delay=1.4),
        CardIntroStar(dx=-22, dy=22, delay=2.1),
    )
    CANDLES: ClassVar[tuple[CardIntroCandle, ...]] = (
        CardIntroCandle(top=0.55, body=0.30),
        CardIntroCandle(top=0.42, body=0.35),
        CardIntroCandle(top=0.48, body=0.22),
        CardIntroCandle(top=0.30, body=0.40),
        CardIntroCandle(top=0.36, body=0.28),
        CardIntroCandle(top=0.22, body=0.35),
        CardIntroCandle(top=0.28, body=0.24),
        CardIntroCandle(top=0.14, body=0.33),
    )
    CANDLE_UP: ClassVar[str] = "#22c55e"
    CANDLE_DOWN: ClassVar[str] = "#ef4444"
    DESCRIPTION: ClassVar[str] = (
        "I like owning things end to end: C++ firmware on an ESP32, the Next.js dashboard that plots "
        "what it measures, and the CI that keeps both honest. By day I'm a full-stack developer at Nobears "
        "in Rotterdam, shipping and maintaining 15+ WordPress platforms. By night I trade NQ futures and "
        "I'm teaching a Python engine to trade them with me."
    )

    def render(self) -> SvgDocument:
        t, w, h, margin = self.theme, self.WIDTH, self.HEIGHT, self.MARGIN
        pipeline = self._pipeline(104)
        py, ph, gap = 190, 124, 16
        pw = (w - 64 - gap) / 2
        dx, nx = margin, margin + pw + gap
        day = CardIntroPanel(
            box=SvgBox(x=dx, y=py, width=pw, height=ph),
            label="BY DAY",
            title="Full-stack developer at Nobears",
            body="Rotterdam. I ship and maintain 15+ WordPress platforms.",
            icon=self._sun(dx + 44, py + ph / 2),
        )
        night = CardIntroPanel(
            box=SvgBox(x=nx, y=py, width=pw, height=ph),
            label="BY NIGHT",
            title="Trading NQ futures",
            body="and teaching a Python engine to trade them with me.",
            icon=self._moon(nx + 44, py + ph / 2),
            reserve_right=170,
        )
        css = (
            SvgFont.css(
                SvgEnumFont.MONO_REGULAR,
                SvgEnumFont.MONO_SEMIBOLD,
                SvgEnumFont.SANS_REGULAR,
                SvgEnumFont.SANS_SEMIBOLD,
            )
            + pipeline.css
            + "@keyframes spin{to{transform:rotate(360deg)}}#sun{animation:spin 24s linear infinite}"
            "@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}.tw{animation:tw 2.8s ease-in-out infinite}"
        )
        body = (
            self.frame(h).open(t)
            + f'<text x="34" y="46" font-family="{SvgEnumFontFamily.MONO.stack}" font-size="12" '
            f'letter-spacing="2" fill="{t.muted}">'
            "HEY, I'M SADRA · NOT SANDRA</text>"
            + f'<text x="33" y="82" font-family="{SvgEnumFontFamily.SANS.stack}" font-size="26" '
            f'font-weight="600" fill="{t.text}">'
            "I like owning things end to end.</text>"
            + pipeline.body
            + day.render(t)
            + night.render(t)
            + self._candles(nx + pw - 146, py + 20, ph - 40)
            + "</g>"
        )

        return SvgDocument(
            width=w,
            height=h,
            body=body,
            css=css,
            title="Hey, I'm Sadra",
            description=self.DESCRIPTION,
        )

    def _pipeline(self, y: float) -> SvgFragment:
        t = self.theme
        x0, x1, gap, nh = (
            self.MARGIN,
            self.WIDTH - self.MARGIN,
            44,
            56,
        )
        count = len(self.PIPELINE)
        nw = (x1 - x0 - gap * (count - 1)) / count
        mono = SvgEnumFontFamily.MONO.stack
        sans = SvgEnumFontFamily.SANS.stack
        parts, css = [], []

        for i, stage in enumerate(self.PIPELINE):
            x = x0 + i * (nw + gap)
            parts.append(
                f'<rect x="{x:.1f}" y="{y}" width="{nw:.1f}" height="{nh}" rx="12" fill="{t.panel}" '
                f'stroke="{t.border}"/>'
                f'<circle cx="{x + 20:.1f}" cy="{y + 22}" r="4" fill="{t.green}"/>'
                f'<text x="{x + 34:.1f}" y="{y + 26}" font-family="{mono}" font-size="14" font-weight="600" '
                f'fill="{t.text}">{esc(stage.name)}</text>'
                f'<text x="{x + 20:.1f}" y="{y + 45}" font-family="{sans}" font-size="13" '
                f'fill="{t.muted}">{esc(stage.detail)}</text>'
            )

            if i == count - 1:
                continue

            ax0, ax1, ay = x + nw + 6, x + nw + gap - 6, y + nh / 2
            parts.append(
                f'<line x1="{ax0:.1f}" y1="{ay}" x2="{ax1 - 4:.1f}" y2="{ay}" stroke="{t.faint}" stroke-width="1.5"/>'
                f'<path d="M{ax1 - 6:.1f} {ay - 4}L{ax1:.1f} {ay}L{ax1 - 6:.1f} {ay + 4}" fill="none" '
                f'stroke="{t.faint}" stroke-width="1.5"/>'
                f'<circle id="pk{i}" cx="{ax0:.1f}" cy="{ay}" r="3" fill="{t.green}"/>'
            )
            css.append(
                f"@keyframes pk{i}{{0%{{transform:translateX(0);opacity:0}}15%{{opacity:1}}"
                f"85%{{opacity:1}}100%{{transform:translateX({ax1 - ax0 - 8:.1f}px);opacity:0}}}}"
                f"#pk{i}{{animation:pk{i} 1.6s linear {i * 0.53:.2f}s infinite both}}"
            )

        return SvgFragment(body="".join(parts), css="".join(css))

    def _sun(self, cx: float, cy: float) -> str:
        t = self.theme
        rays = "".join(
            f'<line x1="{cx}" y1="{cy - 21}" x2="{cx}" y2="{cy - 27}" stroke="{t.yellow}" stroke-width="2.5" '
            f'stroke-linecap="round" transform="rotate({angle} {cx} {cy})"/>'
            for angle in range(0, 360, 45)
        )

        return (
            f'<g id="sun" style="transform-origin:{cx}px {cy}px">{rays}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="14" fill="{t.yellow}"/>'
        )

    def _moon(self, cx: float, cy: float) -> str:
        t = self.theme
        stars = "".join(
            f'<circle class="tw" cx="{cx + star.dx}" cy="{cy + star.dy}" r="1.6" fill="{t.muted}" '
            f'style="animation-delay:{star.delay}s"/>'
            for star in self.STARS
        )

        return (
            f'<circle cx="{cx}" cy="{cy}" r="15" fill="{t.text}"/>'
            f'<circle cx="{cx + 7}" cy="{cy - 5}" r="13" fill="{t.panel}"/>'
            + stars
        )

    def _candles(self, x: float, y: float, h: float) -> str:
        parts = []

        for i, candle in enumerate(self.CANDLES):
            color = self.CANDLE_DOWN if i % 3 == 1 else self.CANDLE_UP
            cx = x + i * 16
            by, bh = y + candle.top * h, candle.body * h
            parts.append(
                f'<line x1="{cx}" y1="{by - 6:.1f}" x2="{cx}" y2="{by + bh + 6:.1f}" stroke="{color}" '
                f'stroke-opacity=".55"/>'
                f'<rect x="{cx - 4}" y="{by:.1f}" width="8" height="{bh:.1f}" rx="1.5" fill="{color}" '
                f'fill-opacity=".55"/>'
            )

        return f'<g opacity=".7">{"".join(parts)}</g>'
