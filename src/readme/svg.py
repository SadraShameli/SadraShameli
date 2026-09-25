"""Shared SVG plumbing: themes, embedded fonts, text measuring, escaping.

Everything here is stdlib-only, so building needs nothing installed.
"""

import base64
import json
from dataclasses import dataclass
from functools import lru_cache
from xml.sax.saxutils import escape

from .paths import FONTS


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str  # card background
    panel: str  # raised surface inside a card
    border: str
    text: str
    muted: str
    faint: str
    dot: str  # dot-grid colour
    dot_opacity: float
    red: str
    yellow: str
    green: str
    # isometric device shading (top, left, right faces) + edge colour
    iso_top: str
    iso_left: str
    iso_right: str
    iso_edge: str
    screen: str
    screen_text: str
    photo_dim: float  # opacity of the black tint over every photo


DARK = Theme(
    name="dark",
    bg="#000000",
    panel="#0a0a0a",
    border="#262626",
    text="#fafafa",
    muted="#a3a3a3",
    faint="#525252",
    dot="#ffffff",
    dot_opacity=0.16,
    red="#ef4444",
    yellow="#eab308",
    green="#22c55e",
    iso_top="#141414",
    iso_left="#0b0b0b",
    iso_right="#1c1c1c",
    iso_edge="#3a3a3a",
    screen="#020617",
    screen_text="#7dd3fc",
    photo_dim=0.35,
)

LIGHT = Theme(
    name="light",
    bg="#ffffff",
    panel="#fafafa",
    border="#e5e5e5",
    text="#0a0a0a",
    muted="#525252",
    faint="#a3a3a3",
    dot="#000000",
    dot_opacity=0.13,
    red="#dc2626",
    yellow="#ca8a04",
    green="#16a34a",
    iso_top="#f5f5f5",
    iso_left="#e5e5e5",
    iso_right="#fafafa",
    iso_edge="#a3a3a3",
    screen="#0f172a",
    screen_text="#7dd3fc",
    photo_dim=0.2,
)

THEMES = (DARK, LIGHT)

MONO = "'sgm',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "'sgs',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
DISPLAY = "'sor','sgs',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"

# css family -> {weight: font file stem}
_FAMILIES = {
    "sgm": {400: "GeistMono-Regular", 600: "GeistMono-SemiBold"},
    "sgs": {400: "Geist-Regular", 600: "Geist-SemiBold"},
    "sor": {600: "Orbitron-SemiBold", 800: "Orbitron-ExtraBold"},
}
_STEM_TO_METRICS = {
    ("mono", 400): "GeistMono-Regular",
    ("mono", 600): "GeistMono-SemiBold",
    ("sans", 400): "Geist-Regular",
    ("sans", 600): "Geist-SemiBold",
    ("display", 600): "Orbitron-SemiBold",
    ("display", 800): "Orbitron-ExtraBold",
}


@lru_cache(maxsize=None)
def _font_b64(stem: str) -> str:
    return base64.b64encode((FONTS / f"{stem}.woff2").read_bytes()).decode()


def font_css(*faces: tuple[str, int]) -> str:
    """@font-face rules for the given (family, weight) pairs, e.g. ("sgm", 400)."""
    rules = []
    for family, weight in faces:
        stem = _FAMILIES[family][weight]
        rules.append(
            f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{_font_b64(stem)}) format('woff2')}}"
        )
    return "".join(rules)


@lru_cache(maxsize=None)
def _metrics() -> dict:
    return json.loads((FONTS / "metrics.json").read_text(encoding="utf-8"))


def measure(text: str, kind: str, weight: int, size: float, spacing: float = 0.0) -> float:
    """Approximate rendered width of `text` (no kerning) in px."""
    m = _metrics()[_STEM_TO_METRICS[(kind, weight)]]
    fallback = m["adv"].get("n", m["upm"] // 2)
    units = sum(m["adv"].get(ch, fallback) for ch in text)
    return units / m["upm"] * size + spacing * max(len(text) - 1, 0)


MONO_ADVANCE = 0.6  # Geist Mono advance width in em


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def reduced_motion_css() -> str:
    # Every animated element's resting style is its final frame, so switching
    # animations off still leaves a complete, readable image.
    return "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def dot_grid(t: Theme, pid: str, w: float, h: float, spacing: int = 22, fade: bool = True) -> str:
    """The dotted backdrop used on sadra.nl, optionally faded towards the edges."""
    defs = (
        f'<pattern id="{pid}" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse">'
        f'<circle cx="{spacing / 2}" cy="{spacing / 2}" r="1" fill="{t.dot}" '
        f'fill-opacity="{t.dot_opacity}"/></pattern>'
    )
    if not fade:
        return f"<defs>{defs}</defs>" f'<rect width="{w}" height="{h}" fill="url(#{pid})"/>'
    defs += (
        f'<radialGradient id="{pid}-f" cx="50%" cy="45%" r="75%">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="{pid}-m"><rect width="{w}" height="{h}" fill="url(#{pid}-f)"/></mask>'
    )
    return (
        f"<defs>{defs}</defs>"
        f'<rect width="{w}" height="{h}" fill="url(#{pid})" mask="url(#{pid}-m)"/>'
    )


def document(w: float, h: float, body: str, css: str, title: str, desc: str = "") -> str:
    desc_el = f"<desc>{esc(desc)}</desc>" if desc else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" '
        f'viewBox="0 0 {w:g} {h:g}" role="img" aria-labelledby="t">'
        f'<title id="t">{esc(title)}</title>{desc_el}'
        f"<style>{css}{reduced_motion_css()}</style>{body}</svg>\n"
    )


def card_frame(t: Theme, w: float, h: float, radius: int = 16, open_bottom: bool = False) -> str:
    """The card outline. `open_bottom` leaves the bottom edge to a dock of link buttons below it."""
    if not open_bottom:
        return (
            f'<rect x=".5" y=".5" width="{w - 1:g}" height="{h - 1:g}" rx="{radius}" '
            f'fill="{t.bg}" stroke="{t.border}"/>'
        )
    r, ri = radius, radius - 0.5
    return (
        f'<path d="M0 {h:g}V{r}A{r} {r} 0 0 1 {r} 0H{w - r:g}A{r} {r} 0 0 1 {w:g} {r}V{h:g}Z" fill="{t.bg}"/>'
        f'<path d="M.5 {h:g}V{r}A{ri} {ri} 0 0 1 {r} .5H{w - r:g}A{ri} {ri} 0 0 1 {w - 0.5:g} {r}V{h:g}" '
        f'fill="none" stroke="{t.border}"/>'
    )


def clip_card(cid: str, w: float, h: float, radius: int = 16, open_bottom: bool = False) -> str:
    extra = f'<rect x="1" y="{h / 2:g}" width="{w - 2:g}" height="{h / 2:g}"/>' if open_bottom else ""
    return (
        f'<clipPath id="{cid}"><rect x="1" y="1" width="{w - 2:g}" height="{h - 2:g}" '
        f'rx="{radius - 1}"/>{extra}</clipPath>'
    )


def pct(t: float, total: float) -> str:
    return f"{min(max(t / total * 100, 0), 100):.3f}".rstrip("0").rstrip(".") + "%"
