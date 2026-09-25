"""Terminal-window cards: `ls` of my YouTube videos and of my documents.

Both play once: the command is typed, then the output prints line by line.
"""

import math
from dataclasses import dataclass

from .cards import photo, wrap
from .dock import docked
from .paths import DOCUMENTS_DIR
from .svg import (
    MONO,
    MONO_ADVANCE,
    SANS,
    Theme,
    card_frame,
    clip_card,
    document,
    esc,
    font_css,
)


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
        self.css.append(
            f".a{self._n}{{animation:in {dur}s linear {delay:.2f}s both}}"
        )
        return f"a{self._n}"

    def prompt(self, x: float, y: float, cwd: str) -> float:
        """Draw `cwd $ ` and return the x where the command starts."""
        t = self.t
        self.body.append(
            f'<text x="{x}" y="{y}" xml:space="preserve"><tspan fill="{t.green}">{esc(cwd)}</tspan>'
            f'<tspan fill="{t.muted}"> $ </tspan></text>'
        )
        return x + (len(cwd) + 3) * self.cw

    def type(
        self, x: float, y: float, text: str, start: float, step: float = 0.045
    ) -> float:
        """Type `text` one character at a time; return when typing ends."""
        for i, ch in enumerate(text):
            if ch != " ":
                self.body.append(
                    f'<text x="{x + i * self.cw:.1f}" y="{y}" fill="{self.t.text}" '
                    f'class="{self.appear(start + i * step)}">{esc(ch)}</text>'
                )
        return start + len(text) * step

    def command(
        self,
        x: float,
        y: float,
        cwd: str,
        command: str,
        comment: str | None = None,
    ) -> float:
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

    def render(
        self, height: float, fonts: tuple, desc: str, open_bottom: bool = False
    ) -> str:
        t, w, th = self.t, self.w, self.TITLE_H
        chrome = [
            "<defs>"
            + clip_card("clip", w, height, 14, open_bottom)
            + "</defs>",
            card_frame(t, w, height, 14, open_bottom),
            '<g clip-path="url(#clip)">',
            f'<rect width="{w}" height="{th}" fill="{t.panel}"/>',
            f'<line x1="0" y1="{th}" x2="{w}" y2="{th}" stroke="{t.border}"/>',
        ]
        for i, c in enumerate((t.red, t.yellow, t.green)):
            chrome.append(
                f'<circle cx="{26 + i * 20}" cy="{th / 2}" r="6" fill="{c}"/>'
            )
        chrome.append(
            f'<text x="{w / 2}" y="{th / 2 + 5}" text-anchor="middle" fill="{t.faint}" '
            f'font-family="{MONO}" font-size="13">'
            f"{esc(self.title)}</text>"
        )
        # defaults as inherited attributes (not a CSS rule) so single elements can override them
        body = f'<g font-family="{MONO}" font-size="{self.fs}">{"".join(self.body)}</g>'
        svg = "".join(chrome) + body + "</g>"
        return document(
            w,
            height,
            svg,
            font_css(*fonts) + "".join(self.css),
            title=self.title,
            desc=desc,
        )


# ── ~/youtube ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Video:
    file: str
    title: str
    views: int
    date: str
    thumb: str  # Images/Cards/<thumb>.jpg


VIDEOS = [
    Video(
        "line-detection.mp4",
        "Line detection for A.I. based on contrast difference",
        2720,
        "Dec 2022",
        "yt-line-detection",
    ),
    Video(
        "lidar-ranging.mp4",
        "Range detection for A.I. based on lidar",
        1197,
        "Dec 2022",
        "yt-lidar-ranging",
    ),
    Video(
        "indoor-test.mp4",
        "Testing my self-driving robot indoors",
        513,
        "Dec 2022",
        "yt-indoor-test",
    ),
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
    done = term.command(x0, cmd_y, "~/youtube", "ls --sort=views | head -3")

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
            photo(t, v.thumb, x, top, THUMB_W, THUMB_H, clip=f"th{i}"),
            (
                f'<rect x="{x + 0.5}" y="{top + 0.5}" width="{THUMB_W - 1}" height="{THUMB_H - 1}" rx="10" '
                f'fill="none" stroke="{t.border}"/>'
            ),
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
    return term.render(
        prompt_y + 30,
        (("sgm", 400), ("sgm", 600), ("sgs", 400)),
        desc,
        docked("youtube"),
    )


# ── ~/Documents ─────────────────────────────────────────────────────────────

# (file, added, note): `added` is how `ls -l` prints the date it was committed
DOCUMENTS = [
    (
        "Letter of Recommendation.pdf",
        "Dec 15  2023",
        "in someone else's words",
    ),
    (
        "PWS - Artificial Intelligence.pdf",
        "Dec 15  2023",
        "95-page A.I. thesis, in Dutch",
    ),
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
    return (
        f"{math.ceil(value * 10) / 10:.1f}{unit}"
        if value < 10
        else f"{math.ceil(value)}{unit}"
    )


def documents(t: Theme) -> str:
    W = 1000
    term = Terminal(t, W, "sadra@rijswijk: ~/Documents", fs=14)
    x0, cmd_y = 36, 84
    done = term.command(
        x0, cmd_y, "~/Documents", "ls -lho {Resume*,Letter*,PWS*}"
    )

    rows = []
    for name, added, note in DOCUMENTS:
        size = _human((DOCUMENTS_DIR / name).stat().st_size)
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
    return term.render(
        prompt_y + 30, (("sgm", 400), ("sgm", 600)), desc, docked("documents")
    )
