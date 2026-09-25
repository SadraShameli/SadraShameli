import math
from dataclasses import dataclass
from typing import ClassVar

from readme.card.btop.gauge import CardBtopGauge
from readme.card.btop.process import CardBtopProcess
from readme.card.card_base import CardBase
from readme.card.constants import CARD_TERMINAL_RADIUS
from readme.card.enum import CardEnumName
from readme.card.terminal import CardTerminal
from readme.svg.box import SvgBox
from readme.svg.constants import SVG_MONO_ADVANCE
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont
from readme.svg.util import esc, pct


@dataclass(kw_only=True, slots=True)
class CardBtop(CardBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.BTOP
    ALT: ClassVar[str] = (
        "btop --user sadra, a system monitor of me: a scrolling cpu graph; mem gauges for coffee 98%, "
        "focus 87%, ideas 112% and free time 3%; and the processes running: tradingbot live with 4 "
        "strategies, WordPress for 15+ sites at Nobears, sensorhub recording when it gets loud, agents "
        "in parallel, sadra.nl, a Prusa printing an enclosure, and a starved sleep."
    )
    RADIUS: ClassVar[int] = CARD_TERMINAL_RADIUS
    MARGIN: ClassVar[int] = 36
    FONT_SIZE: ClassVar[float] = 13.5
    OVERFLOW: ClassVar[int] = 100
    ROW_HEIGHT: ClassVar[int] = 26
    SELECT_SECONDS: ClassVar[float] = 1.8
    GAUGES: ClassVar[tuple[CardBtopGauge, ...]] = (
        CardBtopGauge(label="coffee", value=98),
        CardBtopGauge(label="focus", value=87),
        CardBtopGauge(label="ideas", value=112),
        CardBtopGauge(label="free time", value=3),
    )
    PROCESSES: ClassVar[tuple[CardBtopProcess, ...]] = (
        CardBtopProcess(
            pid=101,
            program="tradingbot",
            arguments="--live --strategies 4",
            cpu=34.1,
        ),
        CardBtopProcess(
            pid=102,
            program="wordpress",
            arguments="--sites 15+ --for nobears",
            cpu=24.8,
        ),
        CardBtopProcess(
            pid=103,
            program="sensorhub",
            arguments="--record-when-loud",
            cpu=12.6,
        ),
        CardBtopProcess(
            pid=104,
            program="agents",
            arguments="--parallel 3 --review-everything",
            cpu=11.2,
        ),
        CardBtopProcess(
            pid=105, program="next", arguments="dev sadra.nl", cpu=8.3
        ),
        CardBtopProcess(
            pid=106,
            program="prusa-mk3s",
            arguments="print enclosure.gcode",
            cpu=5.9,
        ),
        CardBtopProcess(
            pid=107, program="sleep", arguments="8h", cpu=0.3, starved=True
        ),
    )

    def render(self) -> SvgDocument:
        term = CardTerminal(theme=self.theme, title="sadra@rijswijk: ~")
        x0, x1 = self.MARGIN, self.WIDTH - self.MARGIN
        cmd_y = 84
        done = term.command(x0, cmd_y, "~", "btop --user sadra")
        top_y, top_h, gap = cmd_y + 40, 152, 18
        mem_w = 330
        cpu_w = x1 - x0 - mem_w - gap
        proc_y = top_y + top_h + gap
        proc_h = 50 + len(self.PROCESSES) * self.ROW_HEIGHT + 6
        panels = (
            self._cpu(term, SvgBox(x=x0, y=top_y, width=cpu_w, height=top_h))
            + self._mem(
                term,
                SvgBox(x=x0 + cpu_w + gap, y=top_y, width=mem_w, height=top_h),
            )
            + self._proc(
                term, SvgBox(x=x0, y=proc_y, width=x1 - x0, height=proc_h)
            )
        )
        term.body.append(
            f'<g class="{term.appear(done + 0.25, 0.4)}">{panels}</g>'
        )
        prompt_y = proc_y + proc_h + 40
        term.cursor(term.prompt(x0, prompt_y, "~"), prompt_y, done + 0.8)

        return term.render(
            frame=self.frame(prompt_y + 30),
            fonts=(SvgEnumFont.MONO_REGULAR, SvgEnumFont.MONO_SEMIBOLD),
            description=self._description(),
        )

    def _description(self) -> str:
        return (
            "btop --user sadra. mem: "
            + ", ".join(
                f"{gauge.label} {gauge.value}%" for gauge in self.GAUGES
            )
            + ". Running: "
            + ", ".join(
                f"{process.program} {process.arguments} ({process.cpu}% cpu)"
                for process in self.PROCESSES
            )
            + "."
        )

    def _mono_width(self, text: str, size: float) -> float:
        return len(text) * size * SVG_MONO_ADVANCE

    def _panel(self, box: SvgBox, title: str, right: str) -> str:
        t = self.theme
        x, y, w, h = box.x, box.y, box.width, box.height
        rw = self._mono_width(right, 12) + 12

        return (
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="none" stroke="{t.faint}" '
            f'stroke-opacity=".8"/>'
            f'<rect x="{x + 10}" y="{y - 9}" width="{self._mono_width(title, 13) + 12:.1f}" height="18" '
            f'fill="{t.bg}"/>'
            f'<text x="{x + 16}" y="{y + 4.5}" font-size="13" font-weight="600" fill="{t.text}">{esc(title)}</text>'
            f'<rect x="{x + w - 10 - rw:.1f}" y="{y - 9}" width="{rw:.1f}" height="18" fill="{t.bg}"/>'
            f'<text x="{x + w - 16}" y="{y + 4}" font-size="12" text-anchor="end" fill="{t.muted}">'
            f"{esc(right)}</text>"
        )

    def _meter_gradient(self, gradient_id: str, x: float, w: float) -> str:
        t = self.theme

        return (
            f'<linearGradient id="{gradient_id}" gradientUnits="userSpaceOnUse" x1="{x}" x2="{x + w}" '
            'y1="0" y2="0">'
            f'<stop offset="0" stop-color="{t.green}"/><stop offset=".6" stop-color="{t.yellow}"/>'
            f'<stop offset="1" stop-color="{t.red}"/></linearGradient>'
        )

    @staticmethod
    def _load(i: int, n: int) -> float:
        a = 2 * math.pi * i / n
        v = (
            0.5
            + 0.2 * math.sin(2 * a)
            + 0.14 * math.sin(5 * a + 1.3)
            + 0.09 * math.sin(11 * a + 0.4)
        )

        return min(max(v, 0.08), 0.98)

    def _cpu(self, term: CardTerminal, box: SvgBox) -> str:
        t = self.theme
        x, y, w, h = box.x, box.y, box.width, box.height
        sp, r_on, r_off = 9, 2.7, 1.4
        gx, gy = x + 18, y + 20
        cols, rows = int((w - 36) // sp), int((h - 34) // sp)
        gw, gh = cols * sp, rows * sp
        colors = [
            t.green if f <= 0.5 else t.yellow if f <= 0.8 else t.red
            for f in ((r + 1) / rows for r in range(rows))
        ]
        dots = []

        for c in range(cols * 2):
            lit = round(self._load(c % cols, cols) * rows)
            cx = gx + c * sp + sp / 2
            dots.extend(
                f'<circle cx="{cx:.1f}" cy="{gy + gh - r * sp - sp / 2:.1f}" r="{r_on}" fill="{colors[r]}"/>'
                for r in range(lit)
            )

        term.css.append(
            f"@keyframes scroll{{to{{transform:translateX(-{gw}px)}}}}"
            ".scroll{animation:scroll 18s linear infinite}"
        )

        return (
            self._panel(box, "cpu", "uptime 4+ yrs") + "<defs>"
            f'<clipPath id="graph"><rect x="{gx}" y="{gy}" width="{gw}" height="{gh}"/></clipPath>'
            f'<pattern id="off" x="{gx}" y="{gy}" width="{sp}" height="{sp}" patternUnits="userSpaceOnUse">'
            f'<circle cx="{sp / 2}" cy="{sp / 2}" r="{r_off}" fill="{t.faint}" fill-opacity=".45"/></pattern>'
            "</defs>"
            f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="url(#off)"/>'
            f'<g clip-path="url(#graph)"><g class="scroll">{"".join(dots)}</g></g>'
        )

    def _mem(self, term: CardTerminal, box: SvgBox) -> str:
        t, size = self.theme, self.FONT_SIZE
        x, y, w = box.x, box.y, box.width
        tx, bx, bw = x + 18, x + 118, w - 118 - 66
        parts = [
            self._panel(box, "mem", "of the human kind"),
            f"<defs>{self._meter_gradient('mg', bx, bw)}</defs>",
        ]

        for i, gauge in enumerate(self.GAUGES):
            ry = y + 34 + i * 27
            over = gauge.value > self.OVERFLOW
            fill_w = bw * min(gauge.value, self.OVERFLOW) / self.OVERFLOW + (
                10 if over else 0
            )
            term.css.append(
                f"@keyframes mb{i}{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(.95)}}}}"
                f".mb{i}{{transform-origin:{bx}px 0;animation:mb{i} {3.2 + i * 0.7:.1f}s ease-in-out infinite}}"
            )
            parts.append(
                f'<text x="{tx}" y="{ry + 4.5}" font-size="{size}" fill="{t.muted}">{esc(gauge.label)}</text>'
                f'<rect x="{bx}" y="{ry - 4}" width="{bw}" height="8" rx="4" fill="{t.faint}" fill-opacity=".35"/>'
                f'<rect class="mb{i}" x="{bx}" y="{ry - 4}" width="{fill_w:.1f}" height="8" rx="4" fill="url(#mg)"/>'
                f'<text x="{x + w - 18}" y="{ry + 4.5}" font-size="{size}" text-anchor="end" '
                f'fill="{t.red if over else t.text}">{gauge.value}%</text>'
            )

        return "".join(parts)

    def _proc(self, term: CardTerminal, box: SvgBox) -> str:
        t, size, rh = self.theme, self.FONT_SIZE, self.ROW_HEIGHT
        x, y, w = box.x, box.y, box.width
        col_pid, col_prog, col_args = x + 18, x + 76, x + 206
        mw = 132
        mx = x + w - 84 - mw
        row0 = y + 50
        parts = [
            self._panel(box, "proc", f"{len(self.PROCESSES)} running"),
            f"<defs>{self._meter_gradient('pg', mx, mw)}</defs>",
        ]
        period = self.SELECT_SECONDS * len(self.PROCESSES)
        frames = "".join(
            f"{pct(i * self.SELECT_SECONDS, period)}{{transform:translateY({i * rh}px)}}"
            for i in range(len(self.PROCESSES))
        )
        term.css.append(
            f"@keyframes sel{{{frames}100%{{transform:translateY(0)}}}}"
            f".sel{{animation:sel {period:.1f}s step-end infinite}}"
        )
        parts.append(
            f'<rect class="sel" x="{x + 8}" y="{row0 - 17}" width="{w - 16}" height="{rh - 2}" rx="5" '
            f'fill="{t.green}" fill-opacity=".1"/>'
        )
        parts.extend(
            f'<text x="{hx}" y="{y + 24}" font-size="11" letter-spacing="1.5" text-anchor="{anchor}" '
            f'fill="{t.faint}">{label.upper()}</text>'
            for label, hx, anchor in (
                ("pid", col_pid, "start"),
                ("program", col_prog, "start"),
                ("arguments", col_args, "start"),
                ("cpu%", x + w - 18, "end"),
            )
        )
        top = max(process.cpu for process in self.PROCESSES)

        for i, process in enumerate(self.PROCESSES):
            ry = row0 + i * rh
            term.css.append(
                f"@keyframes pj{i}{{0%,100%{{transform:scaleX(1)}}35%{{transform:scaleX(.82)}}"
                f"70%{{transform:scaleX(.93)}}}}"
                f".pj{i}{{transform-origin:{mx}px 0;animation:pj{i} {1.3 + (i * 0.37) % 1.1:.2f}s "
                "ease-in-out infinite}"
            )
            starved = (
                f'<tspan fill="{t.red}" dx="12">starved</tspan>'
                if process.starved
                else ""
            )
            parts.append(
                f'<text x="{col_pid}" y="{ry}" font-size="{size}" fill="{t.faint}">{process.pid}</text>'
                f'<text x="{col_prog}" y="{ry}" font-size="{size}" font-weight="600" fill="{t.text}">'
                f"{esc(process.program)}</text>"
                f'<text x="{col_args}" y="{ry}" font-size="{size}" fill="{t.muted}">'
                f"{esc(process.arguments)}{starved}</text>"
                f'<rect x="{mx}" y="{ry - 8}" width="{mw}" height="7" rx="3.5" fill="{t.faint}" '
                f'fill-opacity=".35"/>'
                f'<rect class="pj{i}" x="{mx}" y="{ry - 8}" width="{max(mw * process.cpu / top, 3):.1f}" '
                f'height="7" rx="3.5" fill="url(#pg)"/>'
                f'<text x="{x + w - 18}" y="{ry}" font-size="{size}" text-anchor="end" fill="{t.text}">'
                f"{process.cpu:.1f}</text>"
            )

        return "".join(parts)
