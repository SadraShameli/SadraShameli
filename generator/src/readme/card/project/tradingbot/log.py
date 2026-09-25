from dataclasses import dataclass
from typing import ClassVar

from readme.card.project.tradingbot.enum import (
    CardProjectTradingbotEnumStage,
    CardProjectTradingbotEnumTone,
)
from readme.svg.box import SvgBox
from readme.svg.constants import SVG_MONO_ADVANCE
from readme.svg.enum import SvgEnumFontFamily
from readme.svg.fragment import SvgFragment
from readme.svg.theme import SvgTheme
from readme.svg.util import esc, pct


@dataclass(kw_only=True, frozen=True, slots=True)
class CardProjectTradingbotLogRun:
    text: str
    tone: CardProjectTradingbotEnumTone


@dataclass(kw_only=True, frozen=True, slots=True)
class CardProjectTradingbotLogLine:
    time: str
    stage: CardProjectTradingbotEnumStage
    runs: tuple[CardProjectTradingbotLogRun, ...]


@dataclass(kw_only=True, frozen=True, slots=True)
class CardProjectTradingbotLog:
    FONT_SIZE: ClassVar[float] = 11.5
    CHAR_WIDTH: ClassVar[float] = FONT_SIZE * SVG_MONO_ADVANCE
    LINE_HEIGHT: ClassVar[int] = 22
    LINE_SECONDS: ClassVar[float] = 1.15
    STAGE_SECONDS: ClassVar[float] = 0.45
    DOT_SPACING: ClassVar[int] = 18
    LINES: ClassVar[tuple[CardProjectTradingbotLogLine, ...]] = (
        CardProjectTradingbotLogLine(
            time="14:30:00",
            stage=CardProjectTradingbotEnumStage.DATA,
            runs=(
                CardProjectTradingbotLogRun(
                    text="NQ 1m bar closed",
                    tone=CardProjectTradingbotEnumTone.TEXT,
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:30:00",
            stage=CardProjectTradingbotEnumStage.FEAT,
            runs=(
                CardProjectTradingbotLogRun(
                    text="42 features", tone=CardProjectTradingbotEnumTone.TEXT
                ),
                CardProjectTradingbotLogRun(
                    text=" · from cache",
                    tone=CardProjectTradingbotEnumTone.DIM,
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:30:00",
            stage=CardProjectTradingbotEnumStage.SCORE,
            runs=(
                CardProjectTradingbotLogRun(
                    text="long ", tone=CardProjectTradingbotEnumTone.TEXT
                ),
                CardProjectTradingbotLogRun(
                    text="0.71", tone=CardProjectTradingbotEnumTone.GOOD
                ),
                CardProjectTradingbotLogRun(
                    text=" · pytorch", tone=CardProjectTradingbotEnumTone.DIM
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:30:00",
            stage=CardProjectTradingbotEnumStage.CHECK,
            runs=(
                CardProjectTradingbotLogRun(
                    text="regime ", tone=CardProjectTradingbotEnumTone.DIM
                ),
                CardProjectTradingbotLogRun(
                    text="ok", tone=CardProjectTradingbotEnumTone.GOOD
                ),
                CardProjectTradingbotLogRun(
                    text=" · spread ", tone=CardProjectTradingbotEnumTone.DIM
                ),
                CardProjectTradingbotLogRun(
                    text="ok", tone=CardProjectTradingbotEnumTone.GOOD
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:30:00",
            stage=CardProjectTradingbotEnumStage.RISK,
            runs=(
                CardProjectTradingbotLogRun(
                    text="size 2 · kill switch armed",
                    tone=CardProjectTradingbotEnumTone.TEXT,
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:30:01",
            stage=CardProjectTradingbotEnumStage.ORDER,
            runs=(
                CardProjectTradingbotLogRun(
                    text="buy 2 NQ · ", tone=CardProjectTradingbotEnumTone.TEXT
                ),
                CardProjectTradingbotLogRun(
                    text="filled", tone=CardProjectTradingbotEnumTone.GOOD
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:31:00",
            stage=CardProjectTradingbotEnumStage.DATA,
            runs=(
                CardProjectTradingbotLogRun(
                    text="ES 5m bar closed",
                    tone=CardProjectTradingbotEnumTone.TEXT,
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:31:00",
            stage=CardProjectTradingbotEnumStage.SCORE,
            runs=(
                CardProjectTradingbotLogRun(
                    text="short ", tone=CardProjectTradingbotEnumTone.TEXT
                ),
                CardProjectTradingbotLogRun(
                    text="0.38", tone=CardProjectTradingbotEnumTone.DIM
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:31:00",
            stage=CardProjectTradingbotEnumStage.CHECK,
            runs=(
                CardProjectTradingbotLogRun(
                    text="regime ", tone=CardProjectTradingbotEnumTone.DIM
                ),
                CardProjectTradingbotLogRun(
                    text="fail", tone=CardProjectTradingbotEnumTone.BAD
                ),
                CardProjectTradingbotLogRun(
                    text=" → skip", tone=CardProjectTradingbotEnumTone.BAD
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:32:00",
            stage=CardProjectTradingbotEnumStage.DATA,
            runs=(
                CardProjectTradingbotLogRun(
                    text="NQ 1m bar closed",
                    tone=CardProjectTradingbotEnumTone.TEXT,
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:32:00",
            stage=CardProjectTradingbotEnumStage.SCORE,
            runs=(
                CardProjectTradingbotLogRun(
                    text="long ", tone=CardProjectTradingbotEnumTone.TEXT
                ),
                CardProjectTradingbotLogRun(
                    text="0.66", tone=CardProjectTradingbotEnumTone.GOOD
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:32:00",
            stage=CardProjectTradingbotEnumStage.CHECK,
            runs=(
                CardProjectTradingbotLogRun(
                    text="news window ", tone=CardProjectTradingbotEnumTone.DIM
                ),
                CardProjectTradingbotLogRun(
                    text="fail", tone=CardProjectTradingbotEnumTone.BAD
                ),
                CardProjectTradingbotLogRun(
                    text=" → skip", tone=CardProjectTradingbotEnumTone.BAD
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:33:00",
            stage=CardProjectTradingbotEnumStage.RISK,
            runs=(
                CardProjectTradingbotLogRun(
                    text="drawdown within limits",
                    tone=CardProjectTradingbotEnumTone.TEXT,
                ),
            ),
        ),
        CardProjectTradingbotLogLine(
            time="14:33:00",
            stage=CardProjectTradingbotEnumStage.ORDER,
            runs=(
                CardProjectTradingbotLogRun(
                    text="trail stop · ",
                    tone=CardProjectTradingbotEnumTone.TEXT,
                ),
                CardProjectTradingbotLogRun(
                    text="moved", tone=CardProjectTradingbotEnumTone.GOOD
                ),
            ),
        ),
    )

    theme: SvgTheme
    box: SvgBox

    def stage_color(self, stage: CardProjectTradingbotEnumStage) -> str:
        match stage:
            case (
                CardProjectTradingbotEnumStage.DATA
                | CardProjectTradingbotEnumStage.FEAT
            ):
                return self.theme.muted
            case CardProjectTradingbotEnumStage.SCORE:
                return self.theme.text
            case (
                CardProjectTradingbotEnumStage.CHECK
                | CardProjectTradingbotEnumStage.RISK
            ):
                return self.theme.yellow
            case CardProjectTradingbotEnumStage.ORDER:
                return self.theme.green

    def tone_color(self, tone: CardProjectTradingbotEnumTone) -> str:
        match tone:
            case CardProjectTradingbotEnumTone.TEXT:
                return self.theme.text
            case CardProjectTradingbotEnumTone.DIM:
                return self.theme.muted
            case CardProjectTradingbotEnumTone.GOOD:
                return self.theme.green
            case CardProjectTradingbotEnumTone.BAD:
                return self.theme.red

    def render(self) -> SvgFragment:
        t, mono = self.theme, SvgEnumFontFamily.MONO.stack
        x, y, w, h = self.box.x, self.box.y, self.box.width, self.box.height
        stages = self._stages(x + 18, y + 46, w)
        top = y + 46 + 34
        log_h = y + h - top

        return SvgFragment(
            body=self._dots()
            + f'<circle id="live" cx="{x + 24}" cy="{y + 26}" r="4" fill="{t.green}"/>'
            f'<text x="{x + 36}" y="{y + 30}" font-family="{mono}" font-size="12.5" font-weight="600" '
            f'fill="{t.text}">tradingbot --live</text>'
            f'<text x="{x + w - 18}" y="{y + 30}" font-family="{mono}" font-size="11.5" text-anchor="end" '
            f'fill="{t.muted}">4 strategies</text>' + stages.body + "<defs>"
            f'<clipPath id="logclip"><rect x="{x}" y="{top}" width="{w}" height="{log_h}"/></clipPath>'
            '<linearGradient id="logfade" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t.panel}"/><stop offset=".14" stop-color="{t.panel}" stop-opacity="0"/>'
            f'<stop offset=".82" stop-color="{t.panel}" stop-opacity="0"/><stop offset="1" stop-color="{t.panel}"/>'
            "</linearGradient></defs>"
            f'<g clip-path="url(#logclip)"><g class="tlog">{self._lines(x + 18, top)}</g></g>'
            f'<rect x="{x}" y="{top}" width="{w}" height="{log_h}" fill="url(#logfade)"/>',
            css="@keyframes live{0%,100%{opacity:1}50%{opacity:.25}}"
            "#live{animation:live 1.6s ease-in-out infinite}"
            + stages.css
            + f"@keyframes tlog{{to{{transform:translateY(-{len(self.LINES) * self.LINE_HEIGHT}px)}}}}"
            f".tlog{{animation:tlog {len(self.LINES) * self.LINE_SECONDS:.1f}s linear infinite}}",
        )

    def _dots(self) -> str:
        t, spacing = self.theme, self.DOT_SPACING
        x, y, w, h = self.box.x, self.box.y, self.box.width, self.box.height

        return (
            f'<defs><pattern id="pd" x="{x}" y="{y}" width="{spacing}" height="{spacing}" '
            'patternUnits="userSpaceOnUse">'
            f'<circle cx="{spacing // 2}" cy="{spacing // 2}" r="1" fill="{t.dot}" '
            f'fill-opacity="{t.dot_opacity}"/></pattern></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t.panel}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pd)"/>'
        )

    def _stages(self, sx: float, sy: float, w: float) -> SvgFragment:
        t, mono, gap = self.theme, SvgEnumFontFamily.MONO.stack, 5
        stages = tuple(CardProjectTradingbotEnumStage)
        sw = (w - 36 - gap * (len(stages) - 1)) / len(stages)
        step = self.STAGE_SECONDS
        period = step * len(stages)
        parts, css = [], []

        for i, stage in enumerate(stages):
            cx, color = sx + i * (sw + gap), self.stage_color(stage)
            parts.append(
                f'<rect x="{cx:.1f}" y="{sy}" width="{sw:.1f}" height="20" rx="5" fill="{t.bg}" '
                f'stroke="{t.border}"/>'
                f'<rect class="st{i}" x="{cx:.1f}" y="{sy}" width="{sw:.1f}" height="20" rx="5" '
                f'fill="{color}" fill-opacity=".16" stroke="{color}" stroke-opacity=".6" opacity="0"/>'
                f'<text x="{cx + sw / 2:.1f}" y="{sy + 14}" font-family="{mono}" font-size="10.5" '
                f'text-anchor="middle" fill="{color}">{stage}</text>'
            )
            css.append(
                f"@keyframes st{i}{{0%{{opacity:0}}{pct(i * step, period)}{{opacity:1}}"
                f"{pct((i + 1) * step, period)}{{opacity:0}}100%{{opacity:0}}}}"
                f".st{i}{{animation:st{i} {period:.2f}s step-end infinite}}"
            )

        return SvgFragment(body="".join(parts), css="".join(css))

    def _lines(self, x: float, top: float) -> str:
        t, mono = self.theme, SvgEnumFontFamily.MONO.stack
        size, cw = self.FONT_SIZE, self.CHAR_WIDTH
        tag_w = 5 * cw + 10
        parts = []

        for n in range(len(self.LINES) * 2):
            line = self.LINES[n % len(self.LINES)]
            ly = top + 16 + n * self.LINE_HEIGHT
            color = self.stage_color(line.stage)
            runs = "".join(
                f'<tspan fill="{self.tone_color(run.tone)}">{esc(run.text)}</tspan>'
                for run in line.runs
            )
            parts.append(
                f'<text x="{x}" y="{ly}" font-family="{mono}" font-size="{size}" fill="{t.faint}">'
                f"{line.time}</text>"
                f'<rect x="{x + 9 * cw:.1f}" y="{ly - 11}" width="{tag_w:.1f}" height="15" rx="4" '
                f'fill="{color}" fill-opacity=".12"/>'
                f'<text x="{x + 9 * cw + tag_w / 2:.1f}" y="{ly}" font-family="{mono}" font-size="{size - 1}" '
                f'text-anchor="middle" fill="{color}">{line.stage}</text>'
                f'<text x="{x + 9 * cw + tag_w + 10:.1f}" y="{ly}" font-family="{mono}" font-size="{size}" '
                f'xml:space="preserve">{runs}</text>'
            )

        return "".join(parts)
