"""Project cards: wide "featured" cards and half-width tiles.

Photos are pre-cropped by prep_images.py and embedded as data URIs so each
card is a single self-contained file.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from functools import lru_cache

from dock import docked
from svg import (
    DISPLAY,
    MONO,
    ROOT,
    SANS,
    Theme,
    card_frame,
    clip_card,
    document,
    esc,
    font_css,
    measure,
)


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    eyebrow: str
    period: str
    desc: str
    link: str
    specs: tuple[tuple[str, str], ...] = ()
    image: str | None = None  # Images/Cards/<image>.jpg
    images: tuple[str, ...] = field(default_factory=tuple)  # collage


@lru_cache(maxsize=None)
def embed_jpeg(name: str) -> str:
    data = (ROOT / "Images" / "Cards" / f"{name}.jpg").read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode()


def photo(t: Theme, name: str, x: float, y: float, w: float, h: float, clip: str | None = None) -> str:
    """An embedded photo filling the box, under the same dark tint as every other photo."""
    clip_attr = f' clip-path="url(#{clip})"' if clip else ""
    return (
        f'<image href="{embed_jpeg(name)}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'preserveAspectRatio="xMidYMid slice"{clip_attr}/>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#000" '
        f'fill-opacity="{t.photo_dim}"{clip_attr}/>'
    )


def wrap(text: str, kind: str, weight: int, size: float, max_w: float) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and measure(trial, kind, weight, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def _base_css(t: Theme) -> str:
    return font_css(("sgm", 400), ("sgs", 400), ("sgs", 600), ("sor", 800)) + (
        f".eb{{font-family:{MONO};font-size:12px;letter-spacing:2px;fill:{t.muted}}}"
        f".ti{{font-family:{DISPLAY};font-weight:800;fill:{t.text}}}"
        f".de{{font-family:{SANS};font-size:16px;fill:{t.muted}}}"
        f".sk{{font-family:{MONO};font-size:13px;fill:{t.faint}}}"
        f".sv{{font-family:{MONO};font-size:13px;fill:{t.text}}}"
        f".ln{{font-family:{MONO};font-size:13px;fill:{t.text}}}"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.2}}"
    )


# ── decorations drawn over / instead of the photo ────────────────────────────


def _lidar(t: Theme, cx: float, cy: float) -> tuple[str, str]:
    """Rotating lidar sweep with range rings, centred on the robot's lidar."""
    r = 260
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#4ade80" stroke-opacity=".35" '
        f'stroke-dasharray="2 5"/>'
        for rr in (60, 120, 180, 240)
    )
    wedge = (
        f'<g id="sweep"><path d="M{cx} {cy}L{cx + r} {cy}A{r} {r} 0 0 0 {cx + r * 0.866:.1f} {cy - r * 0.5:.1f}Z" '
        f'fill="url(#wedge)"/><line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#86efac" '
        f'stroke-width="1.6"/></g>'
    )
    hits = []
    hit_css = []
    pts = [(150, -30), (95, 75), (210, 20), (175, 120), (60, -110), (230, -90), (120, 160), (40, 140)]
    for i, (dx, dy) in enumerate(pts):
        hits.append(f'<circle class="hit h{i}" cx="{cx + dx}" cy="{cy + dy}" r="3" fill="#4ade80"/>')
        hit_css.append(f".h{i}{{animation-delay:{i * 0.37:.2f}s}}")
    css = (
        f"@keyframes sweep{{to{{transform:rotate(-360deg)}}}}"
        f"#sweep{{transform-origin:{cx}px {cy}px;animation:sweep 3s linear infinite}}"
        "@keyframes hit{0%{opacity:0}8%{opacity:1}60%,100%{opacity:0}}"
        ".hit{opacity:.0;animation:hit 3s linear infinite}" + "".join(hit_css)
    )
    defs = (
        '<linearGradient id="wedge" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#22c55e" stop-opacity=".0"/>'
        '<stop offset="1" stop-color="#22c55e" stop-opacity=".45"/></linearGradient>'
    )
    return f"<defs>{defs}</defs>{rings}{wedge}{''.join(hits)}", css


def _pipeline(t: Theme, x: float, y: float, w: float, h: float) -> tuple[str, str]:
    """TradingBot's layers as a flow: signals travel down, validators reject some."""
    stages = ["market data", "features", "pytorch scorer", "validators", "risk engine", "broker api"]
    pw, ph = 196, 30
    gap = (h - 60 - len(stages) * ph) / (len(stages) - 1)
    cx = x + w / 2
    ys = [y + 30 + i * (ph + gap) for i in range(len(stages))]
    parts = [dot_bg(t, x, y, w, h)]
    parts.append(
        f'<line x1="{cx}" y1="{ys[0] + ph / 2}" x2="{cx}" y2="{ys[-1] + ph / 2}" stroke="{t.border}" stroke-width="2"/>'
    )
    for i, (name, sy) in enumerate(zip(stages, ys)):
        accent = t.yellow if name == "validators" else (t.red if name == "risk engine" else t.text)
        parts.append(
            f'<rect x="{cx - pw / 2}" y="{sy}" width="{pw}" height="{ph}" rx="{ph / 2}" fill="{t.panel}" '
            f'stroke="{t.border}"/>'
            f'<circle cx="{cx - pw / 2 + 16}" cy="{sy + ph / 2}" r="3.5" fill="{accent}"/>'
            f'<text x="{cx - pw / 2 + 30}" y="{sy + ph / 2 + 4.5}" font-family="{MONO}" font-size="13" '
            f'fill="{t.text}">{esc(name)}</text>'
        )
    # packets: 0..5 go the whole way, #2 and #4 are rejected at the validators
    v_y = ys[3] + ph / 2
    top, bottom = ys[0] + ph / 2, ys[-1] + ph / 2
    css = []
    period = 6.0
    for i in range(6):
        rejected = i in (1, 4)
        delay = i * 1.0
        if rejected:
            frames = (
                f"0%{{transform:translate(0,0);opacity:0}}4%{{opacity:1}}"
                f"45%{{transform:translate(0,{v_y - top:.1f}px);fill:{t.yellow}}}"
                f"55%{{transform:translate(0,{v_y - top:.1f}px);fill:{t.red};opacity:1}}"
                f"75%{{transform:translate({pw / 2 + 40}px,{v_y - top:.1f}px);fill:{t.red};opacity:0}}"
                f"100%{{opacity:0}}"
            )
        else:
            frames = (
                f"0%{{transform:translate(0,0);opacity:0}}4%{{opacity:1}}"
                f"85%{{transform:translate(0,{bottom - top:.1f}px);opacity:1;fill:{t.green}}}"
                f"100%{{transform:translate(0,{bottom - top:.1f}px);opacity:0;fill:{t.green}}}"
            )
        css.append(
            f"@keyframes p{i}{{{frames}}}"
            f"#p{i}{{animation:p{i} {period}s linear {delay}s infinite both;fill:{t.text}}}"
        )
        parts.append(f'<circle id="p{i}" cx="{cx}" cy="{top}" r="5"/>')
    parts.append(
        f'<text x="{x + 18}" y="{y + h - 14}" font-family="{MONO}" font-size="11" '
        f'fill="{t.faint}">illustrative flow, not live data</text>'
    )
    return "".join(parts), "".join(css)


def dot_bg(t: Theme, x: float, y: float, w: float, h: float) -> str:
    return (
        f'<defs><pattern id="pd" x="{x}" y="{y}" width="18" height="18" patternUnits="userSpaceOnUse">'
        f'<circle cx="9" cy="9" r="1" fill="{t.dot}" fill-opacity="{t.dot_opacity}"/></pattern></defs>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t.panel}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pd)"/>'
    )


def _chip(t: Theme, x: float, y: float, text: str, dot: str | None = None, blink: bool = False) -> str:
    w = measure(text, "mono", 400, 11, 1) + (30 if dot else 18)
    anim = ' style="animation:blink 1.2s step-end infinite"' if blink else ""
    dot_el = f'<circle cx="{x + 13}" cy="{y + 11}" r="3.5" fill="{dot}"{anim}/>' if dot else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="#000" fill-opacity=".62" '
        f'stroke="#fff" stroke-opacity=".18"/>{dot_el}'
        f'<text x="{x + (23 if dot else 9)}" y="{y + 15}" font-family="{MONO}" font-size="11" '
        f'letter-spacing="1" fill="#fff">{esc(text)}</text>'
    )


# ── layouts ─────────────────────────────────────────────────────────────────


# where the lidar puck sits in the prepared Project A.I. photo, as a fraction of it
LIDAR_AT = (0.476, 0.357)
PHOTO_W, PHOTO_H = 400, 320  # frame the photos are prepared for


def _in_frame(fx: float, fy: float, fw: float, fh: float) -> tuple[float, float]:
    """Map a point of a prepared photo into a frame it fills with xMidYMid slice."""
    scale = max(fw / PHOTO_W, fh / PHOTO_H)
    dw, dh = PHOTO_W * scale, PHOTO_H * scale
    return (fw - dw) / 2 + fx * dw, (fh - dh) / 2 + fy * dh


def featured(t: Theme, p: Project, visual: str) -> str:
    # with a dock the links live in the buttons under the card, so the card drops its link row
    open_bottom = docked(f"project-{p.slug}")
    W, H, PW = 1000, (320 if open_bottom else 364), 400
    css = [_base_css(t)]
    body = [
        "<defs>" + clip_card("clip", W, H, open_bottom=open_bottom) + "</defs>",
        card_frame(t, W, H, open_bottom=open_bottom),
        '<g clip-path="url(#clip)">',
    ]

    if visual == "pipeline":
        svg, vcss = _pipeline(t, 0, 0, PW, H)
        body.append(svg)
        css.append(vcss)
    else:
        body.append(photo(t, p.image, 0, 0, PW, H))
        if visual == "lidar":
            svg, vcss = _lidar(t, *(round(v) for v in _in_frame(*LIDAR_AT, PW, H)))
            body.append(f'<g clip-path="url(#photo)">{svg}</g>')
            body.insert(0, f'<defs><clipPath id="photo"><rect width="{PW}" height="{H}"/></clipPath></defs>')
            css.append(vcss)
            body.append(_chip(t, 16, H - 38, "LIDAR SCAN", "#4ade80", blink=True))
        elif visual == "leds":
            body.append(_chip(t, 16, H - 38, "ESP32 · FREERTOS · 3D PRINTED", "#22c55e", blink=True))
    # seam between photo and content
    body.append(
        f'<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{t.bg}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{t.bg}"/></linearGradient></defs>'
        f'<rect x="{PW - 70}" y="0" width="71" height="{H}" fill="url(#fade)"/>'
        f'<line x1="{PW}" y1="0" x2="{PW}" y2="{H}" stroke="{t.border}"/>'
    )

    x, right = PW + 44, W - 40
    body.append(f'<text x="{x}" y="58" class="eb">{esc(p.eyebrow)}</text>')
    body.append(f'<text x="{right}" y="58" class="eb" text-anchor="end">{esc(p.period)}</text>')
    body.append(f'<text x="{x - 2}" y="104" class="ti" font-size="34">{esc(p.title)}</text>')
    y = 138
    for line in wrap(p.desc, "sans", 400, 16, right - x):
        body.append(f'<text x="{x}" y="{y}" class="de">{esc(line)}</text>')
        y += 23
    y += 12
    key_w = max((len(k) for k, _ in p.specs), default=0) + 2
    for k, v in p.specs:
        body.append(
            f'<text x="{x}" y="{y}"><tspan class="sk">{esc(k)}</tspan>'
            f'<tspan class="sv" x="{x + key_w * 7.8:.1f}">{esc(v)}</tspan></text>'
        )
        y += 22
    if not open_bottom:
        body.append(
            f'<line x1="{x}" y1="{H - 52}" x2="{right}" y2="{H - 52}" stroke="{t.border}"/>'
            f'<text x="{x}" y="{H - 26}" class="ln">{esc(p.link)}</text>'
        )
    body.append("</g>")
    return document(W, H, "".join(body), "".join(css), title=p.title, desc=p.desc)


TILE_W, TILE_H, IMG_H = 490, 452, 250


def tile(t: Theme, p: Project) -> str:
    W, H = TILE_W, TILE_H
    css = [_base_css(t)]
    body = ["<defs>" + clip_card("clip", W, H) + "</defs>", card_frame(t, W, H), '<g clip-path="url(#clip)">']
    if p.images:
        half = W / len(p.images)
        for i, name in enumerate(p.images):
            body.append(photo(t, name, i * half, 0, half, IMG_H))
        body.append(f'<line x1="{half:.1f}" y1="0" x2="{half:.1f}" y2="{IMG_H}" stroke="{t.bg}" stroke-width="3"/>')
    else:
        body.append(photo(t, p.image, 0, 0, W, IMG_H))
    body.append(f'<line x1="0" y1="{IMG_H}" x2="{W}" y2="{IMG_H}" stroke="{t.border}"/>')
    x, right = 28, W - 28
    body.append(f'<text x="{x}" y="{IMG_H + 38}" class="eb" font-size="11">{esc(p.eyebrow)}</text>')
    body.append(f'<text x="{x - 1}" y="{IMG_H + 74}" class="ti" font-size="24">{esc(p.title)}</text>')
    body.append(f'<text x="{right}" y="{IMG_H + 74}" class="eb" text-anchor="end">{esc(p.period)}</text>')
    y = IMG_H + 104
    for line in wrap(p.desc, "sans", 400, 15, right - x)[:4]:
        body.append(f'<text x="{x}" y="{y}" class="de" font-size="15">{esc(line)}</text>')
        y += 21
    body.append(f'<text x="{x}" y="{H - 24}" class="ln">{esc(p.link)}</text>')
    body.append("</g>")
    return document(W, H, "".join(body), "".join(css), title=p.title, desc=p.desc)


# ── content ─────────────────────────────────────────────────────────────────

FEATURED = [
    (
        Project(
            slug="sensorhub",
            title="SensorHub",
            eyebrow="IOT · FIRMWARE · HARDWARE",
            period="2024 — NOW",
            desc="Sensor units I design in Fusion 360, 3D-print and program. They measure climate "
            "and loudness, record audio when it gets loud, and report to sadra.nl over HTTPS.",
            specs=(
                ("firmware", "C++ · ESP-IDF 6 · FreeRTOS service kernel"),
                ("sensors", "BME680 climate · INMP441 mic · SSD1306 OLED"),
                ("audio", "own IMA-ADPCM encoder · 5 s pre-roll"),
                ("ci", "30 host-side unit tests · clang-tidy · cppcheck"),
            ),
            link="↗ github.com/SadraShameli/sensorhub",
            image="sensorhub",
        ),
        "leds",
    ),
    (
        Project(
            slug="tradingbot",
            title="TradingBot",
            eyebrow="QUANT · PYTHON · ML",
            period="2025 — NOW",
            desc="The modular quant framework I trade my own capital with: four uncorrelated strategies "
            "across tickers and timeframes, where a backtest has to earn its way into production.",
            specs=(
                ("scoring", "PyTorch position scoring · chained validators"),
                ("validation", "walk-forward · Monte Carlo · Bayesian opt."),
                ("risk", "drawdown kill switches · adaptive sizing"),
                ("runtime", "multiprocess pipeline · Redis cache · Docker"),
            ),
            link="→ private repo · happy to give you a walkthrough",
        ),
        "pipeline",
    ),
    (
        Project(
            slug="projectai",
            title="Project A.I.",
            eyebrow="ROBOTICS · COMPUTER VISION",
            period="2022",
            desc="A self-driving robot car that follows a course and dodges obstacles with on-device "
            "TensorFlow inference. No cloud: lidar, a camera and a 3D-printed chassis.",
            specs=(
                ("vision", "line detection · lidar range detection"),
                ("firmware", "multithreaded C++ control loop"),
                ("override", "PS4 / PS5 controller as a safety net"),
                ("research", "school thesis (PWS) on artificial intelligence"),
            ),
            link="↗ github.com/SadraShameli/ProjectAI",
            image="projectai",
        ),
        "lidar",
    ),
]

TILES = [
    Project(
        slug="sadra-nl",
        title="sadra.nl",
        eyebrow="NEXT.JS 16 · TRPC · DRIZZLE",
        period="2024 — NOW",
        desc="My corner of the web. One auth, API and design system shared by a portfolio, the live "
        "SensorHub dashboard, a trading journal, a resume generator and more.",
        link="↗ sadra.nl",
        image="sadra-nl",
    ),
    Project(
        slug="prop-calculator",
        title="Prop Calculator",
        eyebrow="MONTE CARLO · FUTURES",
        period="LIVE",
        desc="Runs your trading system through a Monte Carlo against each prop firm's real drawdown, "
        "daily-loss and consistency rules to estimate pass odds, costs and payouts.",
        link="↗ sadra.nl/prop-calculator",
        image="prop-calculator",
    ),
    Project(
        slug="minomarkt",
        title="Mino Markt",
        eyebrow="WOOCOMMERCE · PHP · TWIG",
        period="2024 — NOW",
        desc="Storefront for a Persian market & grill in Alkmaar: online ordering, in-store pickup, "
        "loyalty points, subscriptions and live store availability.",
        link="↗ minomarkt.nl",
        image="minomarkt-nl",
    ),
    Project(
        slug="lab",
        title="The early lab",
        eyebrow="ARDUINO · PCB · 3D PRINTING",
        period="EARLY DAYS",
        desc="Where it started: an Arduino Mega robot on a custom PCB packed with RFID, keypad, LCD "
        "and motor drivers, and a 3D-printed social robot with ultrasonic eyes.",
        link="↗ youtube.com/@SadraShameli",
        images=("robot", "socialrobot"),
    ),
]


def all_cards(t: Theme) -> dict[str, str]:
    out = {f"project-{p.slug}": featured(t, p, visual) for p, visual in FEATURED}
    out.update({f"tile-{p.slug}": tile(t, p) for p in TILES})
    return out
