"""Terminal-window cards: `ls` of my YouTube videos and of my documents.

Both play once: the command is typed, then the output prints line by line.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass

from cards import embed_jpeg, wrap
from svg import MONO, MONO_ADVANCE, ROOT, SANS, Theme, card_frame, clip_card, document, esc, font_css


class Terminal:
    """Collects the SVG and CSS for one terminal window."""

    TITLE_H = 44

    def __init__(self, t: Theme, width: int, title: str, fs: float = 14):
        self.t, self.w, self.title, self.fs = t, width, title, fs
        self.cw = fs * MONO_ADVANCE
        self.body: list[str] = []
        self.css: list[str] = [
            "@keyframes in{from{opacity:0}to{opacity:1}}",
            "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}",
        ]
        self._n = 0

    def appear(self, delay: float, dur: float = 0.01) -> str:
        self._n += 1
        self.css.append(f".a{self._n}{{animation:in {dur}s linear {delay:.2f}s both}}")
        return f"a{self._n}"

    def prompt(self, x: float, y: float, cwd: str) -> float:
        """Draw `cwd $ ` and return the x where the command starts."""
        t = self.t
        self.body.append(
            f'<text x="{x}" y="{y}" xml:space="preserve"><tspan fill="{t.green}">{esc(cwd)}</tspan>'
            f'<tspan fill="{t.muted}"> $ </tspan></text>'
        )
        return x + (len(cwd) + 3) * self.cw

    def type(self, x: float, y: float, text: str, start: float, step: float = 0.045) -> float:
        """Type `text` one character at a time; return when typing ends."""
        for i, ch in enumerate(text):
            if ch != " ":
                self.body.append(
                    f'<text x="{x + i * self.cw:.1f}" y="{y}" fill="{self.t.text}" '
                    f'class="{self.appear(start + i * step)}">{esc(ch)}</text>'
                )
        return start + len(text) * step

    def command(self, x: float, y: float, cwd: str, command: str, comment: str | None = None) -> float:
        """Prompt + typed command, then an optional `# comment`; returns when it's all shown."""
        cx = self.prompt(x, y, cwd)
        done = self.type(cx, y, command, 0.35)
        if comment:
            done += 0.15
            self.body.append(
                f'<text x="{cx + (len(command) + 2) * self.cw:.1f}" y="{y}" fill="{self.t.green}" '
                f'class="{self.appear(done, 0.3)}"># {esc(comment)}</text>'
            )
        return done

    def cursor(self, x: float, y: float, delay: float) -> None:
        fs, cw = self.fs, self.cw
        self.body.append(
            f'<g class="{self.appear(delay)}"><rect x="{x:.1f}" y="{y - fs * 0.82:.1f}" width="{cw * 0.9:.1f}" '
            f'height="{fs * 1.05:.1f}" fill="{self.t.text}" style="animation:blink 1.05s step-end infinite"/></g>'
        )

    def render(self, height: float, fonts: tuple, desc: str) -> str:
        t, w, th = self.t, self.w, self.TITLE_H
        chrome = [
            "<defs>" + clip_card("clip", w, height, 14) + "</defs>",
            card_frame(t, w, height, 14),
            '<g clip-path="url(#clip)">',
            f'<rect width="{w}" height="{th}" fill="{t.panel}"/>',
            f'<line x1="0" y1="{th}" x2="{w}" y2="{th}" stroke="{t.border}"/>',
        ]
        for i, c in enumerate((t.red, t.yellow, t.green)):
            chrome.append(f'<circle cx="{26 + i * 20}" cy="{th / 2}" r="6" fill="{c}"/>')
        chrome.append(
            f'<text x="{w / 2}" y="{th / 2 + 5}" text-anchor="middle" fill="{t.faint}" '
            f'font-family="{MONO}" font-size="13">'
            f"{esc(self.title)}</text>"
        )
        # defaults as inherited attributes (not a CSS rule) so single elements can override them
        body = f'<g font-family="{MONO}" font-size="{self.fs}">{"".join(self.body)}</g>'
        svg = "".join(chrome) + body + "</g>"
        return document(w, height, svg, font_css(*fonts) + "".join(self.css), title=self.title, desc=desc)


# ── ~/youtube ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Video:
    file: str
    title: str
    views: int
    date: str
    thumb: str  # Images/Cards/<thumb>.jpg


VIDEOS = [
    Video("line-detection.mp4", "Line detection for A.I. based on contrast difference", 2720, "Dec 2022", "yt-line-detection"),
    Video("lidar-ranging.mp4", "Range detection for A.I. based on lidar", 1197, "Dec 2022", "yt-lidar-ranging"),
    Video("indoor-test.mp4", "Testing my self-driving robot indoors", 513, "Dec 2022", "yt-indoor-test"),
]
THUMB_W, THUMB_H = 126, 224  # 9:16, the videos are vertical


def _views(n: int) -> str:
    # floor, so the number stays true as views go up
    if n >= 1000:
        return f"{math.floor(n / 100) / 10:g}k+ views"
    if n >= 100:
        return f"{n // 100 * 100}+ views"
    return f"{n} views"


def youtube(t: Theme) -> str:
    W = 1000
    term = Terminal(t, W, "sadra@rijswijk: ~/youtube")
    x0, cmd_y = 36, 84
    cx = term.prompt(x0, cmd_y, "~/youtube")
    done = term.type(cx, cmd_y, "ls --sort=views | head -3", 0.35)

    top = cmd_y + 30
    col_w = (W - 2 * x0) / len(VIDEOS)
    for i, v in enumerate(VIDEOS):
        cls = term.appear(done + 0.25 + i * 0.18, 0.35)
        x = x0 + i * col_w
        tx = x + THUMB_W + 18
        text_w = col_w - THUMB_W - 18 - 16
        pcx, pcy = x + THUMB_W / 2, top + THUMB_H / 2
        parts = [
            f'<g class="{cls}">',
            f'<clipPath id="th{i}"><rect x="{x}" y="{top}" width="{THUMB_W}" height="{THUMB_H}" rx="10"/></clipPath>',
            f'<image href="{embed_jpeg(v.thumb)}" x="{x}" y="{top}" width="{THUMB_W}" height="{THUMB_H}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#th{i})"/>',
            f'<rect x="{x + 0.5}" y="{top + 0.5}" width="{THUMB_W - 1}" height="{THUMB_H - 1}" rx="10" '
            f'fill="none" stroke="{t.border}"/>',
            f'<circle cx="{pcx}" cy="{pcy}" r="19" fill="#000" fill-opacity=".6" stroke="#fff" stroke-opacity=".5"/>',
            f'<path d="M{pcx - 5} {pcy - 8}L{pcx + 8} {pcy}L{pcx - 5} {pcy + 8}Z" fill="#fff"/>',
            f'<text x="{tx:.1f}" y="{top + 16}" fill="{t.text}" font-weight="600">{esc(v.file)}</text>',
        ]
        y = top + 44
        for line in wrap(v.title, "sans", 400, 14, text_w):
            parts.append(
                f'<text x="{tx:.1f}" y="{y}" font-family="{SANS}" font-size="14" fill="{t.muted}">{esc(line)}</text>'
            )
            y += 20
        parts.append(
            f'<text x="{tx:.1f}" y="{top + THUMB_H - 26}" font-size="12" fill="{t.green}">{esc(_views(v.views))}</text>'
            f'<text x="{tx:.1f}" y="{top + THUMB_H - 6}" font-size="12" fill="{t.faint}">{esc(v.date)}</text>'
            "</g>"
        )
        term.body.append("".join(parts))

    prompt_y = top + THUMB_H + 44
    end = done + 0.25 + len(VIDEOS) * 0.18 + 0.3
    cx = term.prompt(x0, prompt_y, "~/youtube")
    term.cursor(cx, prompt_y, end)
    desc = "; ".join(f"{v.title} ({_views(v.views)})" for v in VIDEOS)
    return term.render(prompt_y + 30, (("sgm", 400), ("sgm", 600), ("sgs", 400)), desc)


# ── ~/Documents ─────────────────────────────────────────────────────────────

# (file, added, note): `added` is how `ls -l` prints the date it was committed
DOCUMENTS = [
    ("Letter of Recommendation.pdf", "Dec 15  2023", "in someone else's words"),
    ("PWS - Artificial Intelligence.pdf", "Dec 15  2023", "95-page A.I. thesis, in Dutch"),
    ("Resume - Sadra 2.pdf", "May 26 10:01", "the quant / TradingBot one"),
    ("Resume - Sadra.pdf", "May 26 10:01", "the full-stack one"),
]


def _human(size: int) -> str:
    """`ls -h` style: powers of 1024, rounded up."""
    value, unit = float(size), ""
    for bigger in ("K", "M", "G"):
        if value < 1024:
            break
        value, unit = value / 1024, bigger
    if not unit:
        return str(size)
    return f"{math.ceil(value * 10) / 10:.1f}{unit}" if value < 10 else f"{math.ceil(value)}{unit}"


def documents(t: Theme) -> str:
    W = 1000
    term = Terminal(t, W, "sadra@rijswijk: ~/Documents", fs=14)
    x0, cmd_y = 36, 84
    cx = term.prompt(x0, cmd_y, "~/Documents")
    done = term.type(cx, cmd_y, "ls -lho {Resume*,Letter*,PWS*}", 0.35)

    rows = []
    for name, added, note in DOCUMENTS:
        size = _human((ROOT / "Documents" / name).stat().st_size)
        rows.append(("-rw-r--r-- 1 sadra", size, added, f"'{name}'", note))
    size_w = max(len(r[1]) for r in rows)
    name_w = max(len(r[3]) for r in rows)
    y = cmd_y + 34
    for i, (perm, size, added, name, note) in enumerate(rows):
        meta = f"{perm} {size.rjust(size_w)} {added} "
        note_x = x0 + (len(meta) + name_w + 3) * term.cw
        term.body.append(
            f'<g class="{term.appear(done + 0.25 + i * 0.12)}">'
            f'<text x="{x0}" y="{y}" xml:space="preserve"><tspan fill="{t.muted}">{esc(meta)}</tspan>'
            f'<tspan fill="{t.text}" font-weight="600">{esc(name)}</tspan></text>'
            f'<text x="{note_x:.1f}" y="{y}" fill="{t.green}"># {esc(note)}</text></g>'
        )
        y += 26
    prompt_y = y + 20
    end = done + 0.25 + len(rows) * 0.12 + 0.3
    cx = term.prompt(x0, prompt_y, "~/Documents")
    term.cursor(cx, prompt_y, end)
    desc = "; ".join(f"{name}: {note}" for name, _, note in DOCUMENTS)
    return term.render(prompt_y + 30, (("sgm", 400), ("sgm", 600)), desc)


# ── the "pick your path" sections ───────────────────────────────────────────

# a bullet is a list of (text, style) runs; style is "lead" (bold) or "body"
Bullet = list[tuple[str, str]]

HIRING: list[Bullet] = [
    [("4+ years in production.", "lead"), ("Next.js, React, TypeScript and PHP/WordPress at Nobears (2024 to now), "
     "React, ASP.NET and IoT at Blue Star Planning (2021 to 2023).", "body")],
    [("End-to-end ownership.", "lead"), ("I designed the 3D-printed devices, their firmware, the backend that ingests "
     "their data and the frontend that shows it. At Blue Star Planning I set up the Azure DevOps CI/CD pipeline "
     "the team still ships with.", "body")],
    [("I build tools that make teams faster.", "lead"), ("My reusable component library at Nobears saves roughly "
     "1 to 2 days on every new project.", "body")],
    [("Based in Rijswijk, NL.", "lead"), ("Resumes, a letter of recommendation and my email are one click below.", "body")],
]

DEVELOPER: list[Bullet] = [
    [("SensorHub records the loud moments.", "lead"), ("It keeps a 5-second pre-roll ring buffer, encodes audio "
     "with a hand-written IMA-ADPCM encoder (4:1), and streams the WAV over HTTPS while it's still recording.", "body")],
    [("Firmware as a service manifest.", "lead"), ("Every module declares its run mode, stack, priority and start "
     "condition, and a tiny kernel boots the lot as FreeRTOS tasks. The core is header-only, so its 30 unit "
     "tests run on a PC.", "body")],
    [("Type safety from Postgres to pixels.", "lead"), ("sadra.nl runs on Drizzle, Zod and tRPC, with Vitest and "
     "Playwright gating every deploy and Sentry watching production.", "body")],
    [("A backtest has to earn its way into production.", "lead"), ("TradingBot's strategies go through walk-forward "
     "validation, Monte Carlo and Bayesian optimisation before they touch real money.", "body")],
    [("This README is a build artifact.", "lead"), ("The SVGs are generated by Scripts/readme using only the Python "
     "standard library, with fonts subset and embedded so they render the same everywhere.", "body")],
]

ME = {
    "name": "Sadra Shameli",
    "not": "Sandra",
    "location": "Rijswijk, NL",
    "roles": ["full-stack developer", "futures trader", "hardware tinkerer"],
    "stack": ["TypeScript", "Python", "C++", "PHP", "SQL"],
    "links": {
        "site": "https://sadra.nl",
        "linkedin": "https://linkedin.com/in/sadrashameli",
        "youtube": "https://youtube.com/@SadraShameli",
    },
    "status": 200,
}


def _wrap_runs(runs: Bullet, width: int) -> list[list[tuple[str, str]]]:
    """Greedy word wrap by character count (it's a monospace font)."""
    lines: list[list[tuple[str, str]]] = []
    cur: list[tuple[str, str]] = []
    used = 0
    for text, style in runs:
        for word in text.split():
            need = len(word) + (1 if cur else 0)
            if cur and used + need > width:
                lines.append(cur)
                cur, used, need = [], 0, len(word)
            cur.append((word, style))
            used += need
    if cur:
        lines.append(cur)
    return lines


def _runs_svg(t: Theme, words: list[tuple[str, str]]) -> str:
    fills = {"lead": (t.text, ' font-weight="600"'), "body": (t.muted, "")}
    out, prev = [], None
    for i, (word, style) in enumerate(words):
        piece = esc(("" if i == 0 else " ") + word)
        if style == prev:
            out[-1] = out[-1][: -len("</tspan>")] + piece + "</tspan>"
        else:
            fill, weight = fills[style]
            out.append(f'<tspan fill="{fill}"{weight}>{piece}</tspan>')
        prev = style
    return "".join(out)


def notes(t: Theme, command: str, comment: str, bullets: list[Bullet], desc: str) -> str:
    W, x0, cmd_y, lh = 1000, 36, 84, 23
    term = Terminal(t, W, "sadra@rijswijk: ~")
    done = term.command(x0, cmd_y, "~", command, comment)
    width = int((W - 2 * x0) / term.cw) - 2  # minus the "- " gutter
    y = cmd_y + 36
    delay = done + 0.25
    for bullet in bullets:
        for j, line in enumerate(_wrap_runs(bullet, width)):
            dash = f'<tspan fill="{t.green}">-</tspan>' if j == 0 else ""
            term.body.append(
                f'<g class="{term.appear(delay)}">'
                + (f'<text x="{x0}" y="{y}">{dash}</text>' if dash else "")
                + f'<text x="{x0 + 2 * term.cw:.1f}" y="{y}" xml:space="preserve">{_runs_svg(t, line)}</text></g>'
            )
            y += lh
            delay += 0.05
        y += 8
    prompt_y = y + 18
    cx = term.prompt(x0, prompt_y, "~")
    term.cursor(cx, prompt_y, delay + 0.2)
    return term.render(prompt_y + 30, (("sgm", 400), ("sgm", 600)), desc)


def _json_lines(value, indent: int = 0, key: str | None = None, last: bool = True) -> list[tuple[int, str]]:
    """Pretty-print like the README used to: objects expanded, lists on one line."""
    pad = indent
    head = f"{json.dumps(key)}: " if key is not None else ""
    comma = "" if last else ","
    if isinstance(value, dict):
        lines = [(pad, head + "{")]
        items = list(value.items())
        for i, (k, v) in enumerate(items):
            lines += _json_lines(v, indent + 2, k, i == len(items) - 1)
        return lines + [(pad, "}" + comma)]
    if isinstance(value, list):
        return [(pad, head + "[" + ", ".join(json.dumps(v) for v in value) + "]" + comma)]
    return [(pad, head + json.dumps(value) + comma)]


def _json_svg(t: Theme, text: str) -> str:
    out = []
    for m in re.finditer(r'("(?:[^"\\]|\\.)*")(\s*:)?|(-?\d+(?:\.\d+)?)|([{}\[\],:])|(\s+)', text):
        s, is_key, num, punct, space = m.groups()
        if s is not None:
            color = t.green if is_key else t.text
            out.append(f'<tspan fill="{color}">{esc(s)}</tspan>')
            if is_key:
                out.append(f'<tspan fill="{t.muted}">{esc(is_key)}</tspan>')
        elif num is not None:
            out.append(f'<tspan fill="{t.yellow}">{num}</tspan>')
        elif punct is not None:
            out.append(f'<tspan fill="{t.muted}">{esc(punct)}</tspan>')
        else:
            out.append(esc(space))
    return "".join(out)


def robot(t: Theme) -> str:
    W, x0, cmd_y, lh = 1000, 36, 84, 23
    term = Terminal(t, W, "sadra@rijswijk: ~")
    done = term.command(x0, cmd_y, "~", "cat sadra.json | jq", "robot? machine-readable me")
    y = cmd_y + 36
    delay = done + 0.25
    for pad, line in _json_lines(ME):
        term.body.append(
            f'<text x="{x0 + pad * term.cw:.1f}" y="{y}" xml:space="preserve" '
            f'class="{term.appear(delay)}">{_json_svg(t, line)}</text>'
        )
        y += lh
        delay += 0.04
    prompt_y = y + 18
    cx = term.prompt(x0, prompt_y, "~")
    term.cursor(cx, prompt_y, delay + 0.2)
    return term.render(prompt_y + 30, (("sgm", 400), ("sgm", 600)), "sadra.json: " + ", ".join(f"{k}: {v}" for k, v in ME.items()))


def sandra(t: Theme) -> str:
    W, x0, cmd_y = 1000, 36, 84
    term = Terminal(t, W, "sadra@rijswijk: ~")
    done = term.command(x0, cmd_y, "~", "whois sandra", "looking for sandra?")
    lines = [
        (f'<tspan fill="{t.text}">No match for "SANDRA".</tspan>', 0.3),
        (f'<tspan fill="{t.green}"># wrong profile, but honestly, I get that a lot. good luck finding her &lt;3</tspan>', 0.5),
    ]
    y = cmd_y + 36
    delay = done
    for svg, gap in lines:
        delay += gap
        term.body.append(f'<text x="{x0}" y="{y}" class="{term.appear(delay)}">{svg}</text>')
        y += 26
    prompt_y = y + 16
    cx = term.prompt(x0, prompt_y, "~")
    term.cursor(cx, prompt_y, delay + 0.3)
    return term.render(prompt_y + 30, (("sgm", 400),), "whois sandra: no match. Wrong profile, but I get that a lot.")


def paths(t: Theme) -> dict[str, str]:
    return {
        "sh-hiring": notes(
            t, "cat hiring.md", "hiring? the 30-second version", HIRING,
            "The 30-second version for people who are hiring.",
        ),
        "sh-developer": notes(
            t, "cat interesting-bits.md", "developer? the interesting bits", DEVELOPER,
            "The interesting technical bits.",
        ),
        "sh-robot": robot(t),
        "sh-sandra": sandra(t),
    }
