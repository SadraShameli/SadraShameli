"""The intro, drawn instead of written: an end-to-end pipeline, then by day / by night."""

from __future__ import annotations

from cards import wrap
from svg import MONO, SANS, Theme, card_frame, clip_card, document, esc, font_css

W, H = 1000, 340

PIPELINE = [
    ("firmware", "C++ on an ESP32"),
    ("backend", "tRPC + Postgres"),
    ("dashboard", "Next.js, plots it all"),
    ("ci", "keeps both honest"),
]


def _palette(t: Theme) -> dict:
    """Both panels follow the page theme; only the sun and moon tell day from night."""
    return {"bg": t.panel, "border": t.border, "label": t.muted, "title": t.text, "body": t.muted}


def _pipeline(t: Theme, y: float) -> tuple[str, str]:
    x0, x1, gap, nh = 32, W - 32, 44, 56
    nw = (x1 - x0 - gap * (len(PIPELINE) - 1)) / len(PIPELINE)
    parts, css = [], []
    for i, (name, sub) in enumerate(PIPELINE):
        x = x0 + i * (nw + gap)
        parts.append(
            f'<rect x="{x:.1f}" y="{y}" width="{nw:.1f}" height="{nh}" rx="12" fill="{t.panel}" stroke="{t.border}"/>'
            f'<circle cx="{x + 20:.1f}" cy="{y + 22}" r="4" fill="{t.green}"/>'
            f'<text x="{x + 34:.1f}" y="{y + 26}" font-family="{MONO}" font-size="14" font-weight="600" '
            f'fill="{t.text}">{esc(name)}</text>'
            f'<text x="{x + 20:.1f}" y="{y + 45}" font-family="{SANS}" font-size="13" fill="{t.muted}">{esc(sub)}</text>'
        )
        if i < len(PIPELINE) - 1:
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
    return "".join(parts), "".join(css)


def _panel(
    x: float, y: float, w: float, h: float, pal: dict, label: str, title: str, body: str, icon: str,
    reserve_right: float = 24,
) -> str:
    tx = x + 88
    lines = wrap(body, "sans", 400, 14, w - 88 - reserve_right)[:2]
    out = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{pal["bg"]}" stroke="{pal["border"]}"/>',
        icon,
        f'<text x="{tx}" y="{y + 32}" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{pal["label"]}">'
        f"{esc(label)}</text>",
        f'<text x="{tx}" y="{y + 60}" font-family="{SANS}" font-size="19" font-weight="600" fill="{pal["title"]}">'
        f"{esc(title)}</text>",
    ]
    for i, line in enumerate(lines):
        out.append(
            f'<text x="{tx}" y="{y + 86 + i * 20}" font-family="{SANS}" font-size="14" fill="{pal["body"]}">'
            f"{esc(line)}</text>"
        )
    return "".join(out)


def _sun(t: Theme, cx: float, cy: float) -> str:
    rays = "".join(
        f'<line x1="{cx}" y1="{cy - 21}" x2="{cx}" y2="{cy - 27}" stroke="{t.yellow}" stroke-width="2.5" '
        f'stroke-linecap="round" transform="rotate({a} {cx} {cy})"/>'
        for a in range(0, 360, 45)
    )
    return (
        f'<g id="sun" style="transform-origin:{cx}px {cy}px">{rays}</g>'
        f'<circle cx="{cx}" cy="{cy}" r="14" fill="{t.yellow}"/>'
    )


def _moon(t: Theme, cx: float, cy: float) -> str:
    stars = [(-26, -18, 0.0), (24, -24, 0.7), (30, 14, 1.4), (-22, 22, 2.1)]
    star_svg = "".join(
        f'<circle class="tw" cx="{cx + dx}" cy="{cy + dy}" r="1.6" fill="{t.muted}" '
        f'style="animation-delay:{d}s"/>'
        for dx, dy, d in stars
    )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="15" fill="{t.text}"/>'
        f'<circle cx="{cx + 7}" cy="{cy - 5}" r="13" fill="{t.panel}"/>' + star_svg
    )


def _candles(x: float, y: float, h: float) -> str:
    """Decorative, made-up candles. Not market data."""
    shape = [(0.55, 0.30), (0.42, 0.35), (0.48, 0.22), (0.30, 0.40), (0.36, 0.28), (0.22, 0.35), (0.28, 0.24), (0.14, 0.33)]
    out = []
    for i, (top, body) in enumerate(shape):
        up = i % 3 != 1
        color = "#22c55e" if up else "#ef4444"
        cx = x + i * 16
        by, bh = y + top * h, body * h
        out.append(
            f'<line x1="{cx}" y1="{by - 6:.1f}" x2="{cx}" y2="{by + bh + 6:.1f}" stroke="{color}" stroke-opacity=".55"/>'
            f'<rect x="{cx - 4}" y="{by:.1f}" width="8" height="{bh:.1f}" rx="1.5" fill="{color}" fill-opacity=".55"/>'
        )
    return f'<g opacity=".7">{"".join(out)}</g>'


def intro(t: Theme) -> str:
    pipe_svg, pipe_css = _pipeline(t, 104)
    py, ph, gap = 190, 124, 16
    pw = (W - 64 - gap) / 2
    dx, nx = 32, 32 + pw + gap
    pal = _palette(t)
    day = _panel(
        dx, py, pw, ph, pal, "BY DAY", "Full-stack developer at Nobears",
        "Rotterdam. I ship and maintain 15+ WordPress platforms.", _sun(t, dx + 44, py + ph / 2),
    )
    night = _panel(
        nx, py, pw, ph, pal, "BY NIGHT", "Trading NQ futures",
        "and teaching a Python engine to trade them with me.", _moon(t, nx + 44, py + ph / 2),
        reserve_right=170,
    ) + _candles(nx + pw - 146, py + 20, ph - 40)

    css = (
        font_css(("sgm", 400), ("sgm", 600), ("sgs", 400), ("sgs", 600))
        + pipe_css
        + "@keyframes spin{to{transform:rotate(360deg)}}#sun{animation:spin 24s linear infinite}"
        "@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}.tw{animation:tw 2.8s ease-in-out infinite}"
    )
    body = (
        "<defs>" + clip_card("clip", W, H) + "</defs>" + card_frame(t, W, H) + '<g clip-path="url(#clip)">'
        + f'<text x="34" y="46" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t.muted}">'
        "HEY, I'M SADRA · NOT SANDRA</text>"
        + f'<text x="33" y="82" font-family="{SANS}" font-size="26" font-weight="600" fill="{t.text}">'
        "I like owning things end to end.</text>"
        + pipe_svg + day + night + "</g>"
    )
    return document(
        W, H, body, css,
        title="Hey, I'm Sadra",
        desc="I like owning things end to end: C++ firmware on an ESP32, the Next.js dashboard that plots "
        "what it measures, and the CI that keeps both honest. By day I'm a full-stack developer at Nobears "
        "in Rotterdam, shipping and maintaining 15+ WordPress platforms. By night I trade NQ futures and "
        "I'm teaching a Python engine to trade them with me.",
    )
