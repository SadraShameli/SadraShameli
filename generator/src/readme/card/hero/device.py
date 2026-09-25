from dataclasses import dataclass
from typing import ClassVar

from readme.svg.box import SvgBox
from readme.svg.enum import SvgEnumFontFamily
from readme.svg.fragment import SvgFragment
from readme.svg.theme import SvgTheme
from readme.svg.util import esc, pct


@dataclass(kw_only=True, frozen=True, slots=True)
class CardHeroDevicePage:
    label: str
    value: str


@dataclass(kw_only=True, frozen=True, slots=True)
class CardHeroDeviceLed:
    id: str
    color: str


@dataclass(kw_only=True, frozen=True, slots=True)
class CardHeroDevice:
    COS_30: ClassVar[float] = 0.8660254
    SIN_30: ClassVar[float] = 0.5
    WIDTH: ClassVar[int] = 178
    DEPTH: ClassVar[int] = 128
    HEIGHT: ClassVar[int] = 64
    SEAM: ClassVar[int] = 12
    VENTS: ClassVar[int] = 5
    OLED: ClassVar[SvgBox] = SvgBox(x=26, y=24, width=92, height=58)
    PAGE_SECONDS: ClassVar[float] = 2.4
    PAGES: ClassVar[tuple[CardHeroDevicePage, ...]] = (
        CardHeroDevicePage(label=">_sadra", value="Sensor Hub"),
        CardHeroDevicePage(label="TEMP", value="19 °C"),
        CardHeroDevicePage(label="HUMIDITY", value="48 %"),
        CardHeroDevicePage(label="LOUDNESS", value="83 dB"),
        CardHeroDevicePage(label="UPLOAD", value="200 OK"),
    )
    BUTTON_BLUE: ClassVar[str] = "#3b82f6"
    UPLINK: ClassVar[str] = "POST → sadra.nl"

    theme: SvgTheme
    x: float
    y: float

    def iso(self, x: float, y: float, z: float) -> tuple[float, float]:
        return (
            self.x + (x - y) * self.COS_30,
            self.y + (x + y) * self.SIN_30 - z,
        )

    def points(self, *corners: tuple[float, float, float]) -> str:
        return " ".join(
            f"{px:.2f},{py:.2f}"
            for px, py in (self.iso(*corner) for corner in corners)
        )

    def render(self) -> SvgFragment:
        lid = self._lid()
        wifi = self._wifi()

        return SvgFragment(
            body=self._box() + lid.body + wifi.body,
            css=lid.css + wifi.css,
        )

    def _box(self) -> str:
        t, bw, bd, top = self.theme, self.WIDTH, self.DEPTH, self.HEIGHT
        sx, sy = self.iso(bw / 2, bd / 2, 0)
        seam = top - self.SEAM
        parts = [
            (
                f'<ellipse cx="{sx:.1f}" cy="{sy + 8:.1f}" rx="{(bw + bd) * 0.62:.1f}" '
                f'ry="{(bw + bd) * 0.2:.1f}" fill="url(#shadow)"/>'
            ),
            (
                f'<polygon points="{self.points((0, bd, 0), (bw, bd, 0), (bw, bd, top), (0, bd, top))}" '
                f'fill="{t.iso_left}" stroke="{t.iso_edge}" stroke-linejoin="round"/>'
            ),
            (
                f'<polygon points="{self.points((bw, 0, 0), (bw, bd, 0), (bw, bd, top), (bw, 0, top))}" '
                f'fill="{t.iso_right}" stroke="{t.iso_edge}" stroke-linejoin="round"/>'
            ),
            (
                f'<polygon points="{self.points((0, 0, top), (bw, 0, top), (bw, bd, top), (0, bd, top))}" '
                f'fill="{t.iso_top}" stroke="{t.iso_edge}" stroke-linejoin="round"/>'
            ),
            (
                f'<polyline points="{self.points((0, bd, seam), (bw, bd, seam), (bw, 0, seam))}" '
                f'fill="none" stroke="{t.iso_edge}" stroke-opacity=".7"/>'
            ),
        ]

        for i in range(self.VENTS):
            y0 = 22 + i * 18
            parts.append(
                f'<polygon points="{self.points((bw, y0, 12), (bw, y0 + 9, 12), (bw, y0 + 9, 36), (bw, y0, 36))}" '
                f'fill="{t.iso_left}" stroke="{t.iso_edge}" stroke-opacity=".8"/>'
            )

        parts.append(
            f'<polygon points="{self.points((22, bd, 14), (46, bd, 14), (46, bd, 24), (22, bd, 24))}" '
            f'fill="{t.bg}" stroke="{t.iso_edge}"/>'
        )

        return "".join(parts)

    def _lid(self) -> SvgFragment:
        t, bw, bd = self.theme, self.WIDTH, self.DEPTH
        ax, ay = self.iso(0, 0, self.HEIGHT)
        c30, s30 = self.COS_30, self.SIN_30
        parts = [
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="{t.iso_right}" stroke="{t.iso_edge}"/>'
            f'<path d="M{cx - 2.2} {cy}h4.4M{cx} {cy - 2.2}v4.4" stroke="{t.iso_edge}" stroke-width=".9"/>'
            for cx, cy in (
                (10, 10),
                (bw - 10, 10),
                (10, bd - 10),
                (bw - 10, bd - 10),
            )
        ]
        oled = self._oled()
        parts.append(oled.body)

        for i, led in enumerate(
            (
                CardHeroDeviceLed(id="lr", color=t.red),
                CardHeroDeviceLed(id="ly", color=t.yellow),
                CardHeroDeviceLed(id="lg", color=t.green),
            )
        ):
            cx, cy = 140, 30 + i * 16
            parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{led.color}" fill-opacity=".18" '
                f'stroke="{led.color}" stroke-opacity=".5"/>'
                f'<circle id="{led.id}" cx="{cx}" cy="{cy}" r="4.2" fill="{led.color}"/>'
                f'<circle id="{led.id}g" cx="{cx}" cy="{cy}" r="11" fill="{led.color}" fill-opacity=".35" '
                f'filter="url(#glow)"/>'
            )

        for i, color in enumerate((t.red, self.BUTTON_BLUE)):
            cx, cy = 56 + i * 36, 104
            parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="8" fill="{t.iso_left}" stroke="{t.iso_edge}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{color}"/>'
            )

        return SvgFragment(
            body=f'<g transform="matrix({c30},{s30},{-c30},{s30},{ax:.2f},{ay:.2f})">{"".join(parts)}</g>',
            css=oled.css
            + "@keyframes ly{0%,4%,8%,12%,16%{opacity:1}2%,6%,10%,14%,18%,100%{opacity:.15}}"
            "@keyframes lg{0%,19%{opacity:.15}20%,23%{opacity:1}24%,59%{opacity:.15}60%,63%{opacity:1}"
            "64%,100%{opacity:.15}}"
            "#ly,#lyg{animation:ly 12s step-end infinite}#lg,#lgg{animation:lg 12s step-end infinite}"
            "#lr{opacity:.15}#lrg{opacity:0}#lyg,#lgg{mix-blend-mode:screen}",
        )

    def _oled(self) -> SvgFragment:
        t, oled = self.theme, self.OLED
        sx0, sy0, sw, sh = oled.x, oled.y, oled.width, oled.height
        cycle = self.PAGE_SECONDS * len(self.PAGES)
        mono = SvgEnumFontFamily.MONO.stack
        bold, dim = 'font-weight="600"', 'fill-opacity=".7"'
        parts = [
            (
                f'<rect x="{sx0 - 5}" y="{sy0 - 5}" width="{sw + 10}" height="{sh + 10}" rx="3" '
                f'fill="{t.iso_left}" stroke="{t.iso_edge}"/>'
                f'<rect x="{sx0}" y="{sy0}" width="{sw}" height="{sh}" rx="1.5" fill="{t.screen}"/>'
            )
        ]
        css = []

        for i, page in enumerate(self.PAGES):
            on, off = i * self.PAGE_SECONDS, (i + 1) * self.PAGE_SECONDS
            big = 17 if i else 15
            css.append(
                f"@keyframes pg{i}{{0%{{opacity:0}}{pct(on, cycle)}{{opacity:1}}{pct(off, cycle)}{{opacity:0}}}}"
                f"#pg{i}{{animation:pg{i} {cycle}s step-end infinite}}"
            )
            hidden = "" if i == 0 else ' opacity="0"'
            parts.append(
                f'<g id="pg{i}"{hidden} font-family="{mono}" fill="{t.screen_text}">'
                f'<text x="{sx0 + 8}" y="{sy0 + 20}" font-size="{10 if i else big}" '
                f"{bold if i == 0 else dim}>{esc(page.label)}</text>"
                f'<text x="{sx0 + 8}" y="{sy0 + 44}" font-size="{big if i else 10}" '
                f"{bold if i else dim}>{esc(page.value)}</text></g>"
            )

        parts.append(
            f'<rect id="scan" x="{sx0}" y="{sy0}" width="{sw}" height="6" fill="{t.screen_text}" '
            f'fill-opacity=".08"/>'
        )
        css.append(
            f"@keyframes scan{{0%{{transform:translateY(0)}}100%{{transform:translateY({sh - 6}px)}}}}"
            "#scan{animation:scan 3.2s linear infinite}"
        )

        return SvgFragment(body="".join(parts), css="".join(css))

    def _wifi(self) -> SvgFragment:
        t = self.theme
        wx, wy = self.iso(self.WIDTH * 0.5, self.DEPTH * 0.2, self.HEIGHT + 40)
        arcs = "".join(
            f'<path class="arc a{i}" d="M{wx - r * 0.8:.1f} {wy - r * 0.2:.1f} '
            f'A{r} {r} 0 0 1 {wx + r * 0.8:.1f} {wy - r * 0.2:.1f}" fill="none" '
            f'stroke="{t.green}" stroke-width="2.4" stroke-linecap="round"/>'
            for i, r in enumerate((12, 22, 32))
        )
        lx, ly = wx + 58, wy - 26

        return SvgFragment(
            body=arcs
            + f'<circle cx="{wx:.1f}" cy="{wy + 5:.1f}" r="2.8" fill="{t.green}" class="arc a0"/>'
            + f'<path d="M{wx + 30:.1f} {wy - 12:.1f} Q{wx + 44:.1f} {ly:.1f} {lx - 4:.1f} {ly:.1f}" '
            f'fill="none" stroke="{t.faint}" stroke-dasharray="3 4" class="dash"/>'
            f'<text x="{lx:.1f}" y="{ly + 4:.1f}" font-family="{SvgEnumFontFamily.MONO.stack}" '
            f'font-size="12" fill="{t.muted}">{self.UPLINK}</text>',
            css="@keyframes arc{0%,19%{opacity:.12}21%{opacity:1}30%,59%{opacity:.12}61%{opacity:1}"
            "70%,100%{opacity:.12}}"
            ".arc{animation:arc 12s linear infinite}.a1{animation-delay:.12s}.a2{animation-delay:.24s}"
            "@keyframes dash{to{stroke-dashoffset:-14}}.dash{animation:dash .9s linear infinite}",
        )
