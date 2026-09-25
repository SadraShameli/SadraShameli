"""Link docks: rows of buttons that form the bottom edge of a card.

A README image can only link to one place, so every button is its own tiny
SVG. Placed flush under the card (see `readme_html`), they read as the card's
footer: the card is drawn with an open bottom and the last row of buttons
carries the bottom border and corners.
"""

from dataclasses import dataclass

from .stack import icons
from .svg import MONO, Theme, document, esc, font_css, measure

DOCK_H = 52
CARD_W = 1000

STL = "https://github.com/SadraShameli/sensorhub/blob/main/Assets/3D%20Models/Sensor%20Unit/Casing%20body.stl"
RESUME = "Documents/Resume%20-%20Sadra.pdf"
RESUME_QUANT = "Documents/Resume%20-%20Sadra%202.pdf"
LETTER = "Documents/Letter%20of%20Recommendation.pdf"
THESIS = "Documents/PWS%20-%20Artificial%20Intelligence.pdf"
EMAIL = "mailto:sadra.shameli1@gmail.com"
LINKEDIN = "https://linkedin.com/in/sadrashameli"
YOUTUBE = "https://youtube.com/@SadraShameli"


@dataclass(frozen=True)
class Link:
    label: str
    href: str
    icon: str  # key into ICONS


# card name -> (corner radius of that card, rows of links)
DOCKS: dict[str, tuple[int, list[list[Link]]]] = {
    "hero": (16, [[
        Link("sadra.nl", "https://sadra.nl", "globe"),
        Link("LinkedIn", LINKEDIN, "linkedin"),
        Link("YouTube", YOUTUBE, "youtube"),
        Link("Email", EMAIL, "mail"),
        Link("Resume.pdf", RESUME, "doc"),
    ]]),
    "project-sensorhub": (16, [[
        Link("Source code", "https://github.com/SadraShameli/sensorhub", "github"),
        Link("Spin the enclosure in 3D", STL, "cube"),
    ]]),
    "project-tradingbot": (16, [[
        Link("The quant resume", RESUME_QUANT, "doc"),
        Link("Ask me for a walkthrough", EMAIL, "mail"),
    ]]),
    "project-projectai": (16, [[
        Link("Source code", "https://github.com/SadraShameli/ProjectAI", "github"),
        Link("Watch it drive", "https://www.youtube.com/shorts/abyVlfAETG0", "play"),
    ]]),
    "youtube": (14, [[
        Link("Line detection", "https://www.youtube.com/watch?v=1142rRZ3rzc", "play"),
        Link("Lidar ranging", "https://www.youtube.com/watch?v=_C8PnLK2SWA", "play"),
        Link("Indoor test drive", "https://www.youtube.com/shorts/abyVlfAETG0", "play"),
        Link("Channel", YOUTUBE, "youtube"),
    ]]),
    "documents": (14, [
        [
            Link("Resume · full-stack", RESUME, "doc"),
            Link("Resume · quant", RESUME_QUANT, "doc"),
            Link("Letter of recommendation", LETTER, "doc"),
            Link("A.I. thesis (PWS)", THESIS, "doc"),
        ],
        [  # where I work(ed) and how to reach me
            Link("Nobears", "https://www.nobears.com", "globe"),
            Link("Blue Star Planning", "https://bluestarplanning.com", "globe"),
            Link("LinkedIn", LINKEDIN, "linkedin"),
            Link("Email", EMAIL, "mail"),
        ],
        [  # code worth reading
            Link("IMA-ADPCM encoder", "https://github.com/SadraShameli/sensorhub/blob/main/include/AdpcmRecorder.h", "github"),
            Link("Service kernel", "https://github.com/SadraShameli/sensorhub/blob/main/src/core/Kernel.cpp", "github"),
            Link("sadra.nl source", "https://github.com/SadraShameli/sadra.nl", "github"),
            Link("README generator", "src/readme", "github"),
        ],
    ]),
}

# LinkedIn isn't in simple-icons any more; this is its well-known 24x24 glyph
_LINKEDIN = (
    "M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05"
    "c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 "
    "0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45"
    "c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"
)


def _icon(kind: str, x: float, cy: float, color: str) -> str:
    """A 16px icon whose left edge is at x, vertically centred on cy."""
    y = cy - 8
    if kind in ("github", "youtube", "linkedin"):
        d = _LINKEDIN if kind == "linkedin" else icons()[kind]
        return f'<path transform="translate({x:.1f} {y:.1f}) scale(.6667)" d="{d}" fill="{color}"/>'
    stroke = f'fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "globe":
        return (
            f'<g transform="translate({x:.1f} {y:.1f})" {stroke}><circle cx="8" cy="8" r="7"/>'
            '<ellipse cx="8" cy="8" rx="3" ry="7"/><path d="M1 8h14"/></g>'
        )
    if kind == "mail":
        return (
            f'<g transform="translate({x:.1f} {y:.1f})" {stroke}><rect x="1" y="3" width="14" height="10" rx="2"/>'
            '<path d="M1.5 4l6.5 5 6.5-5"/></g>'
        )
    if kind == "doc":
        return (
            f'<g transform="translate({x:.1f} {y:.1f})" {stroke}><path d="M3 1h7l3 3v11H3z"/>'
            '<path d="M10 1v3h3M5.5 8h5M5.5 11h5"/></g>'
        )
    if kind == "play":
        return f'<path transform="translate({x:.1f} {y:.1f})" d="M4 2l10 6-10 6z" fill="{color}"/>'
    if kind == "cube":
        return (
            f'<g transform="translate({x:.1f} {y:.1f})" {stroke}><path d="M8 1l6.5 3.5v7L8 15l-6.5-3.5v-7z"/>'
            '<path d="M1.5 4.5L8 8l6.5-3.5M8 8v7"/></g>'
        )
    raise ValueError(kind)


def segment(t: Theme, link: Link, width: float, radius: int, first: bool, last: bool, bottom: bool) -> str:
    w, h, r = width, DOCK_H, radius
    rl = r if first and bottom else 0
    rr = r if last and bottom else 0
    fill = (
        f'<path d="M0 0H{w:.2f}V{h - rr}'
        + (f"A{rr} {rr} 0 0 1 {w - rr:.2f} {h}" if rr else "")
        + f"H{rl}"
        + (f"A{rl} {rl} 0 0 1 0 {h - rl}" if rl else f"L0 {h}")
        + f'Z" fill="{t.panel}"/>'
    )
    lines = [f'<path d="M0 .5H{w:.2f}" stroke="{t.border}"/>']  # divider from the card / the row above
    if first:
        lines.append(
            f'<path d="M.5 0V{h - rl}' + (f"A{rl - .5} {rl - .5} 0 0 0 {rl} {h - .5}" if rl else "") + f'" '
            f'fill="none" stroke="{t.border}"/>'
        )
    lines.append(  # right edge: the card border on the last button, a separator otherwise
        f'<path d="M{w - .5:.2f} 0V{h - rr}'
        + (f"A{rr - .5} {rr - .5} 0 0 1 {w - rr:.2f} {h - .5}" if rr else "")
        + f'" fill="none" stroke="{t.border}"/>'
    )
    if bottom:
        lines.append(f'<path d="M{rl} {h - .5}H{w - rr:.2f}" stroke="{t.border}"/>')

    label_w = measure(link.label, "mono", 400, 14)
    content_w = 16 + 10 + label_w + 10 + 9
    x = (w - content_w) / 2
    cy = h / 2
    body = (
        fill
        + _icon(link.icon, x, cy, t.text)
        + f'<text x="{x + 26:.1f}" y="{cy + 5:.1f}" font-family="{MONO}" font-size="14" fill="{t.text}">'
        f"{esc(link.label)}</text>"
        + f'<text x="{x + 26 + label_w + 10:.1f}" y="{cy + 5:.1f}" font-family="{MONO}" font-size="14" '
        f'fill="{t.faint}">↗</text>'
        + "".join(lines)
    )
    return document(w, h, body, font_css(("sgm", 400)), title=link.label)


def docked(card: str) -> bool:
    return card in DOCKS


def all_docks(t: Theme) -> dict[str, str]:
    """dock/<card>-<row>-<col> -> SVG"""
    out = {}
    for card, (radius, rows) in DOCKS.items():
        for ri, row in enumerate(rows):
            width = CARD_W / len(row)
            for ci, link in enumerate(row):
                out[f"dock/{card}-{ri}-{ci}"] = segment(
                    t, link, width, radius, first=ci == 0, last=ci == len(row) - 1, bottom=ri == len(rows) - 1,
                )
    return out


def readme_html(card: str, href: str, alt: str) -> str:
    """The README markup for a card plus its dock, laid out so the pieces sit flush."""
    def pic(name: str, text: str, width: str) -> str:
        return (
            f'<picture><source media="(prefers-color-scheme: dark)" srcset="Assets/Readme/{name}-dark.svg">'
            f'<img align="top" alt="{esc(text)}" src="Assets/Readme/{name}-light.svg" width="{width}"></picture>'
        )

    _, rows = DOCKS[card]
    lines = [f'<a href="{href}">{pic(card, alt, "100%")}</a><br>']
    for ri, row in enumerate(rows):
        pct = f"{100 / len(row):.4f}".rstrip("0").rstrip(".") + "%"
        # no whitespace between buttons, or it would show up as gaps
        cells = "".join(
            f'<a href="{esc(link.href)}">{pic(f"dock/{card}-{ri}-{ci}", link.label, pct)}</a>'
            for ci, link in enumerate(row)
        )
        lines.append(cells + ("<br>" if ri < len(rows) - 1 else ""))
    return "<p>\n" + "\n".join(lines) + "\n</p>"
