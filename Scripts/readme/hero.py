"""Animated hero banner.

Left: name, tagline and a terminal that types `whoami`, answers "sandra",
notices the typo, backspaces and fixes it. Right: an isometric SensorHub
unit whose OLED cycles through the real firmware's pages and whose LEDs
blink the way the firmware blinks them (yellow = connecting, green = upload).
"""

from __future__ import annotations

from dock import docked
from svg import (
    DISPLAY,
    MONO,
    MONO_ADVANCE,
    Theme,
    card_frame,
    clip_card,
    document,
    dot_grid,
    esc,
    font_css,
    pct,
)

W, H = 1000, 360
LOOP = 13.0  # seconds per typing loop

# terminal geometry
TX, TY1, TY2, FS = 48, 262, 296, 19
CW = FS * MONO_ADVANCE


def _typing(t: Theme) -> tuple[str, str]:
    """Return (svg, css) for the whoami gag."""
    prompt = "~/rijswijk $ "
    cmd = "whoami"
    chars: list[tuple[str, float, float, int, int, str]] = []  # ch, on, off, line, col, cls

    end = 12.3
    t0 = 0.8
    for i, ch in enumerate(cmd):
        chars.append((ch, t0 + i * 0.09, end, 1, len(prompt) + i, "cmd"))

    # line 2: "sandra" … backspace "ndra" … "dra"
    typo_on = 2.0
    wrong = "sandra"
    typo_times = [typo_on + i * 0.1 for i in range(len(wrong))]
    bs_start = 3.5
    bs_times = {5: bs_start, 4: bs_start + 0.08, 3: bs_start + 0.16, 2: bs_start + 0.24}
    for i, ch in enumerate(wrong):
        off = bs_times.get(i, end)
        chars.append((ch, typo_times[i], off, 2, i, "out"))
    fix_on = 4.05
    for i, ch in enumerate("dra"):
        chars.append((ch, fix_on + i * 0.1, end, 2, 2 + i, "out"))
    comment = "  // not sandra. never was."
    c_on = 4.75
    for i, ch in enumerate(comment):
        chars.append((ch, c_on + i * 0.03, end, 2, 5 + i, "cmt"))

    css = []
    els = []
    for n, (ch, on, off, line, col, cls) in enumerate(chars):
        if ch == " ":
            continue
        x = TX + col * CW
        y = TY1 if line == 1 else TY2
        # the typo'd letters rest hidden; everything else rests visible
        resting_hidden = off < end
        css.append(
            f"@keyframes k{n}{{0%{{opacity:0}}{pct(on, LOOP)}{{opacity:1}}"
            f"{pct(off, LOOP)}{{opacity:0}}100%{{opacity:0}}}}"
            f"#c{n}{{animation:k{n} {LOOP}s step-end infinite}}"
        )
        style = ' opacity="0"' if resting_hidden else ""
        els.append(f'<text id="c{n}" class="{cls}" x="{x:.2f}" y="{y}"{style}>{esc(ch)}</text>')

    # cursor: position keyframes (step-end) + blink
    events: list[tuple[float, int, int]] = [(0, 1, len(prompt))]
    for i in range(len(cmd)):
        events.append((t0 + i * 0.09, 1, len(prompt) + i + 1))
    events.append((1.75, 2, 0))
    for i in range(len(wrong)):
        events.append((typo_times[i], 2, i + 1))
    for col, tm in sorted(bs_times.items(), key=lambda kv: kv[1]):
        events.append((tm, 2, col))
    for i in range(3):
        events.append((fix_on + i * 0.1, 2, 3 + i))
    events.append((c_on + len(comment) * 0.03, 2, 5 + len(comment)))
    events.append((end, 1, len(prompt)))
    frames = "".join(
        f"{pct(tm, LOOP)}{{transform:translate({col * CW:.2f}px,{(TY1 if line == 1 else TY2) - TY1}px)}}"
        for tm, line, col in events
    )
    rest_col = 5 + len(comment)
    css.append(
        f"@keyframes cur{{{frames}100%{{transform:translate({len(prompt) * CW:.2f}px,0px)}}}}"
        f"#cur{{animation:cur {LOOP}s step-end infinite;"
        f"transform:translate({rest_col * CW:.2f}px,{TY2 - TY1}px)}}"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
        "#curb{animation:blink 1.05s step-end infinite}"
    )
    cursor = (
        f'<g id="cur"><rect id="curb" x="{TX}" y="{TY1 - FS * 0.82:.2f}" '
        f'width="{CW * 0.9:.2f}" height="{FS * 1.05:.2f}" fill="{t.text}" opacity=".85"/></g>'
    )
    # spell-checker squiggle under "sandra" right before the fix
    sq_on, sq_off = 2.9, bs_start + 0.3
    y = TY2 + 6
    wave = "".join(f"q{CW / 4:.2f} {-3 if k % 2 else 3} {CW / 2:.2f} 0" for k in range(12))
    squiggle = (
        f'<path id="sq" d="M{TX} {y}{wave}" fill="none" stroke="{t.red}" stroke-width="1.6" '
        f'stroke-linecap="round" opacity="0"/>'
    )
    css.append(
        f"@keyframes sq{{0%{{opacity:0}}{pct(sq_on, LOOP)}{{opacity:1}}{pct(sq_off, LOOP)}{{opacity:0}}}}"
        f"#sq{{animation:sq {LOOP}s step-end infinite}}"
    )
    static_prompt = (
        f'<text class="pr" x="{TX}" y="{TY1}">'
        f'<tspan fill="{t.green}">~/rijswijk</tspan><tspan fill="{t.muted}"> $ </tspan></text>'
    )
    return static_prompt + "".join(els) + squiggle + cursor, "".join(css)


# ── isometric SensorHub ──────────────────────────────────────────────────────
C30, S30 = 0.8660254, 0.5


def _iso(ox: float, oy: float, x: float, y: float, z: float) -> tuple[float, float]:
    return ox + (x - y) * C30, oy + (x + y) * S30 - z


def _pts(ox, oy, *xyz) -> str:
    return " ".join(f"{px:.2f},{py:.2f}" for px, py in (_iso(ox, oy, *p) for p in xyz))


def _device(t: Theme, ox: float, oy: float) -> tuple[str, str]:
    BW, BD, BH = 178, 128, 64  # box width (x), depth (y), height (z)
    top = BH
    parts = []
    # soft shadow
    sx, sy = _iso(ox, oy, BW / 2, BD / 2, 0)
    parts.append(
        f'<ellipse cx="{sx:.1f}" cy="{sy + 8:.1f}" rx="{(BW + BD) * 0.62:.1f}" '
        f'ry="{(BW + BD) * 0.2:.1f}" fill="url(#shadow)"/>'
    )
    # faces
    parts.append(
        f'<polygon points="{_pts(ox, oy, (0, BD, 0), (BW, BD, 0), (BW, BD, top), (0, BD, top))}" '
        f'fill="{t.iso_left}" stroke="{t.iso_edge}" stroke-linejoin="round"/>'
    )
    parts.append(
        f'<polygon points="{_pts(ox, oy, (BW, 0, 0), (BW, BD, 0), (BW, BD, top), (BW, 0, top))}" '
        f'fill="{t.iso_right}" stroke="{t.iso_edge}" stroke-linejoin="round"/>'
    )
    parts.append(
        f'<polygon points="{_pts(ox, oy, (0, 0, top), (BW, 0, top), (BW, BD, top), (0, BD, top))}" '
        f'fill="{t.iso_top}" stroke="{t.iso_edge}" stroke-linejoin="round"/>'
    )
    # lid seam
    seam = top - 12
    parts.append(
        f'<polyline points="{_pts(ox, oy, (0, BD, seam), (BW, BD, seam), (BW, 0, seam))}" '
        f'fill="none" stroke="{t.iso_edge}" stroke-opacity=".7"/>'
    )
    # vents on the right face (like the orange sensor unit)
    for i in range(5):
        y0 = 22 + i * 18
        parts.append(
            f'<polygon points="{_pts(ox, oy, (BW, y0, 12), (BW, y0 + 9, 12), (BW, y0 + 9, 36), (BW, y0, 36))}" '
            f'fill="{t.iso_left}" stroke="{t.iso_edge}" stroke-opacity=".8"/>'
        )
    # USB port on the left face
    parts.append(
        f'<polygon points="{_pts(ox, oy, (22, BD, 14), (46, BD, 14), (46, BD, 24), (22, BD, 24))}" '
        f'fill="{t.bg}" stroke="{t.iso_edge}"/>'
    )

    # everything on the lid lives in the lid's own 2-D coordinates
    ax, ay = _iso(ox, oy, 0, 0, top)
    lid = f'matrix({C30},{S30},{-C30},{S30},{ax:.2f},{ay:.2f})'
    lid_parts = []
    for cx, cy in ((10, 10), (BW - 10, 10), (10, BD - 10), (BW - 10, BD - 10)):
        lid_parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="{t.iso_right}" stroke="{t.iso_edge}"/>'
            f'<path d="M{cx - 2.2} {cy}h4.4M{cx} {cy - 2.2}v4.4" stroke="{t.iso_edge}" stroke-width=".9"/>'
        )
    # OLED
    sx0, sy0, sw, sh = 26, 24, 92, 58
    lid_parts.append(
        f'<rect x="{sx0 - 5}" y="{sy0 - 5}" width="{sw + 10}" height="{sh + 10}" rx="3" fill="{t.iso_left}" stroke="{t.iso_edge}"/>'
        f'<rect x="{sx0}" y="{sy0}" width="{sw}" height="{sh}" rx="1.5" fill="{t.screen}"/>'
    )
    pages = [
        (">_sadra", "Sensor Hub"),
        ("TEMP", "19 °C"),
        ("HUMIDITY", "48 %"),
        ("LOUDNESS", "83 dB"),
        ("UPLOAD", "200 OK"),
    ]
    page_len = 2.4
    cycle = page_len * len(pages)
    oled_css = []
    for i, (a, b) in enumerate(pages):
        on, off = i * page_len, (i + 1) * page_len
        big = 17 if i else 15
        oled_css.append(
            f"@keyframes pg{i}{{0%{{opacity:0}}{pct(on, cycle)}{{opacity:1}}{pct(off, cycle)}{{opacity:0}}}}"
            f"#pg{i}{{animation:pg{i} {cycle}s step-end infinite}}"
        )
        hidden = "" if i == 0 else ' opacity="0"'
        bold, dim = 'font-weight="600"', 'fill-opacity=".7"'
        lid_parts.append(
            f'<g id="pg{i}"{hidden} font-family="{MONO}" fill="{t.screen_text}">'
            f'<text x="{sx0 + 8}" y="{sy0 + 20}" font-size="{10 if i else big}" '
            f"{bold if i == 0 else dim}>{esc(a)}</text>"
            f'<text x="{sx0 + 8}" y="{sy0 + 44}" font-size="{big if i else 10}" '
            f"{bold if i else dim}>{esc(b)}</text></g>"
        )
    # scanline shimmer on the OLED
    lid_parts.append(
        f'<rect id="scan" x="{sx0}" y="{sy0}" width="{sw}" height="6" fill="{t.screen_text}" fill-opacity=".08"/>'
    )
    oled_css.append(
        f"@keyframes scan{{0%{{transform:translateY(0)}}100%{{transform:translateY({sh - 6}px)}}}}"
        "#scan{animation:scan 3.2s linear infinite}"
    )
    # LEDs (red, yellow, green) + two buttons
    leds = [(t.red, "lr"), (t.yellow, "ly"), (t.green, "lg")]
    for i, (col, lid_id) in enumerate(leds):
        cx, cy = 140, 30 + i * 16
        lid_parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-opacity=".5"/>'
            f'<circle id="{lid_id}" cx="{cx}" cy="{cy}" r="4.2" fill="{col}"/>'
            f'<circle id="{lid_id}g" cx="{cx}" cy="{cy}" r="11" fill="{col}" fill-opacity=".35" filter="url(#glow)"/>'
        )
    for i, col in enumerate((t.red, "#3b82f6")):
        cx, cy = 56 + i * 36, 104
        lid_parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="8" fill="{t.iso_left}" stroke="{t.iso_edge}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{col}"/>'
        )
    # firmware blink pattern: yellow flickers while "connecting", then
    # green blinks on every successful upload, red stays calm.
    led_css = (
        "@keyframes ly{0%,4%,8%,12%,16%{opacity:1}2%,6%,10%,14%,18%,100%{opacity:.15}}"
        "@keyframes lg{0%,19%{opacity:.15}20%,23%{opacity:1}24%,59%{opacity:.15}60%,63%{opacity:1}64%,100%{opacity:.15}}"
        "#ly,#lyg{animation:ly 12s step-end infinite}#lg,#lgg{animation:lg 12s step-end infinite}"
        "#lr{opacity:.15}#lrg{opacity:0}#lyg,#lgg{mix-blend-mode:screen}"
    )
    # Wi-Fi arcs above the device, pulsing with each upload
    wx, wy = _iso(ox, oy, BW * 0.5, BD * 0.2, top + 40)
    arcs = []
    for i, r in enumerate((12, 22, 32)):
        arcs.append(
            f'<path class="arc a{i}" d="M{wx - r * 0.8:.1f} {wy - r * 0.2:.1f} '
            f'A{r} {r} 0 0 1 {wx + r * 0.8:.1f} {wy - r * 0.2:.1f}" fill="none" '
            f'stroke="{t.green}" stroke-width="2.4" stroke-linecap="round"/>'
        )
    arcs.append(f'<circle cx="{wx:.1f}" cy="{wy + 5:.1f}" r="2.8" fill="{t.green}" class="arc a0"/>')
    arc_css = (
        "@keyframes arc{0%,19%{opacity:.12}21%{opacity:1}30%,59%{opacity:.12}61%{opacity:1}70%,100%{opacity:.12}}"
        ".arc{animation:arc 12s linear infinite}.a1{animation-delay:.12s}.a2{animation-delay:.24s}"
    )
    # dashed uplink with label
    lx, ly = wx + 58, wy - 26
    uplink = (
        f'<path d="M{wx + 30:.1f} {wy - 12:.1f} Q{wx + 44:.1f} {ly:.1f} {lx - 4:.1f} {ly:.1f}" fill="none" '
        f'stroke="{t.faint}" stroke-dasharray="3 4" class="dash"/>'
        f'<text x="{lx:.1f}" y="{ly + 4:.1f}" font-family="{MONO}" font-size="12" fill="{t.muted}">POST → sadra.nl</text>'
    )
    dash_css = "@keyframes dash{to{stroke-dashoffset:-14}}.dash{animation:dash .9s linear infinite}"

    svg = (
        "".join(parts)
        + f'<g transform="{lid}">{"".join(lid_parts)}</g>'
        + "".join(arcs)
        + uplink
    )
    return svg, "".join(oled_css) + led_css + arc_css + dash_css


def hero(t: Theme) -> str:
    typing_svg, typing_css = _typing(t)
    device_svg, device_css = _device(t, ox=730, oy=172)

    css = (
        font_css(("sgm", 400), ("sgm", 600), ("sor", 800))
        + f".cmd,.out,.pr{{font-family:{MONO};font-size:{FS}px;fill:{t.text}}}"
        f".pr{{fill:{t.muted}}}"
        f".cmt{{font-family:{MONO};font-size:{FS}px;fill:{t.faint}}}"
        + typing_css
        + device_css
        + "@keyframes shine{0%{transform:translateX(-700px)}60%,100%{transform:translateX(900px)}}"
        "#shine{animation:shine 7s ease-in-out infinite}"
    )
    body = (
        "<defs>"
        + clip_card("clip", W, H, open_bottom=docked("hero"))
        + '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<mask id="nameMask"><rect width="1000" height="360" fill="#000"/>'
        f'<text x="46" y="170" font-family="{DISPLAY}" font-weight="800" font-size="50" letter-spacing="1" fill="#fff">SADRA SHAMELI</text></mask>'
        f'<radialGradient id="shadow"><stop offset="0" stop-color="{"#000" if t.name == "light" else "#fff"}" stop-opacity="{".16" if t.name == "light" else ".07"}"/>'
        '<stop offset="1" stop-opacity="0"/></radialGradient>'
        '<filter id="glow" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="3.2"/></filter>'
        "</defs>"
        + card_frame(t, W, H, open_bottom=docked("hero"))
        + '<g clip-path="url(#clip)">'
        + dot_grid(t, "dots", W, H)
        # logo + coordinates
        + f'<text x="48" y="62" font-family="{DISPLAY}" font-weight="800" font-size="20" fill="{t.text}">&gt;_sadra</text>'
        + f'<text x="952" y="60" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{t.muted}">'
        f"RIJSWIJK, NL  ·  52.04°N 4.32°E</text>"
        # name with a light sweep
        + f'<text x="46" y="170" font-family="{DISPLAY}" font-weight="800" font-size="50" letter-spacing="1" fill="{t.text}">SADRA SHAMELI</text>'
        + f'<g mask="url(#nameMask)" opacity="{".55" if t.name == "dark" else ".0"}"><rect id="shine" x="0" y="110" width="160" height="80" fill="url(#sh)"/></g>'
        + f'<text x="48" y="206" font-family="{MONO}" font-size="15" fill="{t.muted}">'
        "full-stack developer  ·  futures trader  ·  hardware tinkerer</text>"
        + typing_svg
        + device_svg
        + "</g>"
    )
    return document(
        W,
        H,
        body,
        css,
        title="Sadra Shameli — full-stack developer, futures trader, hardware tinkerer",
        desc="A terminal types whoami, answers sandra, fixes the typo to sadra. "
        "Next to it an isometric SensorHub device blinks its LEDs.",
    )
