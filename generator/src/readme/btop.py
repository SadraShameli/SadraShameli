"""`btop --user sadra`: a system monitor of me, instead of a list of frameworks.

cpu is a scrolling LED dot graph, mem is coffee / focus / ideas / free time, and proc
is what's running. The percentages are for fun; the processes are the real projects.
"""

import math

from .svg import MONO_ADVANCE, Theme, esc, pct
from .terminal import Terminal

W = 1000
X0, X1 = 36, W - 36
FS = 13.5  # body text inside the boxes

MEM = [("coffee", 98), ("focus", 87), ("ideas", 112), ("free time", 3)]

# pid, program, arguments, cpu %
PROCS = [
    (101, "tradingbot", "--live --strategies 4", 34.1),
    (102, "wordpress", "--sites 15+ --for nobears", 24.8),
    (103, "sensorhub", "--record-when-loud", 12.6),
    (104, "agents", "--parallel 3 --review-everything", 11.2),
    (105, "next", "dev sadra.nl", 8.3),
    (106, "prusa-mk3s", "print enclosure.gcode", 5.9),
    (107, "sleep", "8h", 0.3),
]


def _mono_w(text: str, size: float = FS) -> float:
    return len(text) * size * MONO_ADVANCE


def _box(
    t: Theme,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    right: str = "",
) -> str:
    """A rounded btop panel with its title set into the top border."""
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="none" stroke="{t.faint}" stroke-opacity=".8"/>',
        f'<rect x="{x + 10}" y="{y - 9}" width="{_mono_w(title, 13) + 12:.1f}" height="18" fill="{t.bg}"/>',
        f'<text x="{x + 16}" y="{y + 4.5}" font-size="13" font-weight="600" fill="{t.text}">{esc(title)}</text>',
    ]
    if right:
        rw = _mono_w(right, 12) + 12
        parts.append(
            f'<rect x="{x + w - 10 - rw:.1f}" y="{y - 9}" width="{rw:.1f}" height="18" fill="{t.bg}"/>'
            f'<text x="{x + w - 16}" y="{y + 4}" font-size="12" text-anchor="end" fill="{t.muted}">{esc(right)}</text>'
        )
    return "".join(parts)


def _load(i: int, n: int) -> float:
    """A made-up but periodic load curve, so the scrolling graph loops seamlessly."""
    a = 2 * math.pi * i / n
    v = (
        0.5
        + 0.2 * math.sin(2 * a)
        + 0.14 * math.sin(5 * a + 1.3)
        + 0.09 * math.sin(11 * a + 0.4)
    )
    return min(max(v, 0.08), 0.98)


def _cpu(
    t: Theme, term: Terminal, x: float, y: float, w: float, h: float
) -> str:
    sp, r_on, r_off = 9, 2.7, 1.4
    gx, gy = x + 18, y + 20
    cols, rows = int((w - 36) // sp), int((h - 34) // sp)
    gw, gh = cols * sp, rows * sp
    colors = [
        t.green if f <= 0.5 else t.yellow if f <= 0.8 else t.red
        for f in ((r + 1) / rows for r in range(rows))
    ]
    dots = []
    for c in range(
        cols * 2
    ):  # two periods, so shifting by one period loops seamlessly
        lit = round(_load(c % cols, cols) * rows)
        cx = gx + c * sp + sp / 2
        for r in range(lit):
            dots.append(
                f'<circle cx="{cx:.1f}" cy="{gy + gh - r * sp - sp / 2:.1f}" r="{r_on}" fill="{colors[r]}"/>'
            )
    term.css.append(
        f"@keyframes scroll{{to{{transform:translateX(-{gw}px)}}}}.scroll{{animation:scroll 18s linear infinite}}"
    )
    return (
        _box(t, x, y, w, h, "cpu", "uptime 4+ yrs") + "<defs>"
        f'<clipPath id="graph"><rect x="{gx}" y="{gy}" width="{gw}" height="{gh}"/></clipPath>'
        f'<pattern id="off" x="{gx}" y="{gy}" width="{sp}" height="{sp}" patternUnits="userSpaceOnUse">'
        f'<circle cx="{sp / 2}" cy="{sp / 2}" r="{r_off}" fill="{t.faint}" fill-opacity=".45"/></pattern>'
        "</defs>"
        f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="url(#off)"/>'
        f'<g clip-path="url(#graph)"><g class="scroll">{"".join(dots)}</g></g>'
    )


def _meter_gradient(t: Theme, gid: str, x: float, w: float) -> str:
    return (
        f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x}" x2="{x + w}" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{t.green}"/><stop offset=".6" stop-color="{t.yellow}"/>'
        f'<stop offset="1" stop-color="{t.red}"/></linearGradient>'
    )


def _mem(
    t: Theme, term: Terminal, x: float, y: float, w: float, h: float
) -> str:
    tx, bx, bw = x + 18, x + 118, w - 118 - 66
    parts = [
        _box(t, x, y, w, h, "mem", "of the human kind"),
        f"<defs>{_meter_gradient(t, 'mg', bx, bw)}</defs>",
    ]
    for i, (label, value) in enumerate(MEM):
        ry = y + 34 + i * 27
        fill_w = bw * min(value, 100) / 100 + (10 if value > 100 else 0)
        term.css.append(
            f"@keyframes mb{i}{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(.95)}}}}"
            f".mb{i}{{transform-origin:{bx}px 0;animation:mb{i} {3.2 + i * 0.7:.1f}s ease-in-out infinite}}"
        )
        parts.append(
            f'<text x="{tx}" y="{ry + 4.5}" font-size="{FS}" fill="{t.muted}">{esc(label)}</text>'
            f'<rect x="{bx}" y="{ry - 4}" width="{bw}" height="8" rx="4" fill="{t.faint}" fill-opacity=".35"/>'
            f'<rect class="mb{i}" x="{bx}" y="{ry - 4}" width="{fill_w:.1f}" height="8" rx="4" fill="url(#mg)"/>'
            f'<text x="{x + w - 18}" y="{ry + 4.5}" font-size="{FS}" text-anchor="end" '
            f'fill="{t.red if value > 100 else t.text}">{value}%</text>'
        )
    return "".join(parts)


def _proc(
    t: Theme, term: Terminal, x: float, y: float, w: float, h: float
) -> str:
    col_pid, col_prog, col_args = x + 18, x + 76, x + 206
    mw = 132
    mx = x + w - 84 - mw
    row0, rh = y + 50, 26
    parts = [
        _box(t, x, y, w, h, "proc", f"{len(PROCS)} running"),
        f"<defs>{_meter_gradient(t, 'pg', mx, mw)}</defs>",
    ]
    # btop's selection bar, stepping down the list
    period = 1.8 * len(PROCS)
    frames = "".join(
        f"{pct(i * 1.8, period)}{{transform:translateY({i * rh}px)}}"
        for i in range(len(PROCS))
    )
    term.css.append(
        f"@keyframes sel{{{frames}100%{{transform:translateY(0)}}}}"
        f".sel{{animation:sel {period:.1f}s step-end infinite}}"
    )
    parts.append(
        f'<rect class="sel" x="{x + 8}" y="{row0 - 17}" width="{w - 16}" height="{rh - 2}" rx="5" '
        f'fill="{t.green}" fill-opacity=".1"/>'
    )
    head_y = y + 24
    for label, hx, anchor in (
        ("pid", col_pid, "start"),
        ("program", col_prog, "start"),
        ("arguments", col_args, "start"),
        ("cpu%", x + w - 18, "end"),
    ):
        parts.append(
            f'<text x="{hx}" y="{head_y}" font-size="11" letter-spacing="1.5" text-anchor="{anchor}" '
            f'fill="{t.faint}">{label.upper()}</text>'
        )
    top = max(p for *_, p in PROCS)
    for i, (pid, prog, args, cpu) in enumerate(PROCS):
        ry = row0 + i * rh
        starved = prog == "sleep"
        term.css.append(
            f"@keyframes pj{i}{{0%,100%{{transform:scaleX(1)}}35%{{transform:scaleX(.82)}}70%{{transform:scaleX(.93)}}}}"
            f".pj{i}{{transform-origin:{mx}px 0;animation:pj{i} {1.3 + (i * 0.37) % 1.1:.2f}s ease-in-out infinite}}"
        )
        parts.append(
            f'<text x="{col_pid}" y="{ry}" font-size="{FS}" fill="{t.faint}">{pid}</text>'
            f'<text x="{col_prog}" y="{ry}" font-size="{FS}" font-weight="600" fill="{t.text}">{esc(prog)}</text>'
            f'<text x="{col_args}" y="{ry}" font-size="{FS}" fill="{t.muted}">{esc(args)}'
            + (
                f'<tspan fill="{t.red}" dx="12">starved</tspan>'
                if starved
                else ""
            )
            + "</text>"
            f'<rect x="{mx}" y="{ry - 8}" width="{mw}" height="7" rx="3.5" fill="{t.faint}" fill-opacity=".35"/>'
            f'<rect class="pj{i}" x="{mx}" y="{ry - 8}" width="{max(mw * cpu / top, 3):.1f}" height="7" rx="3.5" '
            f'fill="url(#pg)"/>'
            f'<text x="{x + w - 18}" y="{ry}" font-size="{FS}" text-anchor="end" fill="{t.text}">{cpu:.1f}</text>'
        )
    return "".join(parts)


def btop(t: Theme) -> str:
    term = Terminal(t, W, "sadra@rijswijk: ~")
    cmd_y = 84
    done = term.command(X0, cmd_y, "~", "btop --user sadra")

    top_y, top_h, gap = cmd_y + 40, 152, 18
    mem_w = 330
    cpu_w = X1 - X0 - mem_w - gap
    proc_y = top_y + top_h + gap
    proc_h = 50 + len(PROCS) * 26 + 6
    panels = (
        _cpu(t, term, X0, top_y, cpu_w, top_h)
        + _mem(t, term, X0 + cpu_w + gap, top_y, mem_w, top_h)
        + _proc(t, term, X0, proc_y, X1 - X0, proc_h)
    )
    term.body.append(
        f'<g class="{term.appear(done + 0.25, 0.4)}">{panels}</g>'
    )

    prompt_y = proc_y + proc_h + 40
    cx = term.prompt(X0, prompt_y, "~")
    term.cursor(cx, prompt_y, done + 0.8)
    desc = (
        "btop --user sadra. mem: "
        + ", ".join(f"{k} {v}%" for k, v in MEM)
        + ". Running: "
        + ", ".join(
            f"{prog} {args} ({cpu}% cpu)" for _, prog, args, cpu in PROCS
        )
        + "."
    )
    return term.render(prompt_y + 30, (("sgm", 400), ("sgm", 600)), desc)
