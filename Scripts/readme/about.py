"""`neofetch`, but it's me. Plays once: types the command, prints the output."""

from __future__ import annotations

from svg import MONO, MONO_ADVANCE, Theme, card_frame, clip_card, document, esc, font_css

W = 1000
FS = 15
LH = 23
CW = FS * MONO_ADVANCE

# ">_" on a 10x9 LED matrix
MATRIX = [
    "XX........",
    ".XX.......",
    "..XX......",
    "...XX.....",
    "..XX......",
    ".XX.......",
    "XX........",
    "..........",
    "....XXXXXX",
]
CELL, GAP = 15, 3

INFO = [
    ("Role", "Full-stack developer @ Nobears, Rotterdam"),
    ("Uptime", "4+ years shipping production code"),
    ("Languages", "TypeScript · Python · C++ · PHP · SQL"),
    ("Web", "Next.js · React · tRPC · Drizzle · Tailwind"),
    ("CMS", "WordPress · WooCommerce · Twig · 15+ sites live"),
    ("Firmware", "ESP32 · ESP-IDF · FreeRTOS · BME680 · I²S mics"),
    ("Quant", "PyTorch · NumPy · Pandas · Redis · Docker"),
    ("Printers", "Prusa MK3S+ · Prusa Mini+ · Vertex K8400"),
    ("Currently", "teaching a Python engine to trade NQ futures"),
    ("Known issue", "people read my name as Sandra (wontfix)"),
]


def about(t: Theme) -> str:
    x0, title_h = 36, 44
    cmd_y = title_h + 38
    out_y = cmd_y + 40
    info_x = x0 + len(MATRIX[0]) * (CELL + GAP) + 44
    rows = 2 + len(INFO) + 2  # user@host, rule, info…, gap, swatches
    prompt_y = out_y + rows * LH + 18
    H = prompt_y + 34

    css = [
        font_css(("sgm", 400), ("sgm", 600)),
        f"text{{font-family:{MONO};font-size:{FS}px}}",
        f".k{{fill:{t.text};font-weight:600}}.v{{fill:{t.muted}}}.g{{fill:{t.green}}}.f{{fill:{t.faint}}}",
        "@keyframes in{from{opacity:0}to{opacity:1}}",
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}",
    ]
    anim_n = 0

    def appear(delay: float, dur: float = 0.01) -> str:
        nonlocal anim_n
        anim_n += 1
        css.append(f".a{anim_n}{{animation:in {dur}s linear {delay:.2f}s both}}")
        return f"a{anim_n}"

    body = [
        "<defs>" + clip_card("clip", W, H, 14) + "</defs>",
        card_frame(t, W, H, 14),
        '<g clip-path="url(#clip)">',
        f'<rect width="{W}" height="{title_h}" fill="{t.panel}"/>',
        f'<line x1="0" y1="{title_h}" x2="{W}" y2="{title_h}" stroke="{t.border}"/>',
    ]
    for i, c in enumerate((t.red, t.yellow, t.green)):
        body.append(f'<circle cx="{26 + i * 20}" cy="{title_h / 2}" r="6" fill="{c}"/>')
    body.append(
        f'<text x="{W / 2}" y="{title_h / 2 + 5}" text-anchor="middle" class="f" font-size="13">'
        "sadra@rijswijk: ~</text>"
    )

    # the command, typed
    body.append(f'<text x="{x0}" y="{cmd_y}"><tspan class="g">~</tspan><tspan class="v"> $ </tspan></text>')
    cmd = "neofetch"
    for i, ch in enumerate(cmd):
        body.append(
            f'<text x="{x0 + (4 + i) * CW:.2f}" y="{cmd_y}" fill="{t.text}" '
            f'class="{appear(0.35 + i * 0.07)}">{ch}</text>'
        )
    out_t = 0.35 + len(cmd) * 0.07 + 0.35

    # logo: LEDs power on one by one, in reading order
    my = out_y - 6
    lit_i = 0
    for r, row in enumerate(MATRIX):
        for c, ch in enumerate(row):
            x, yy = x0 + c * (CELL + GAP), my + r * (CELL + GAP)
            if ch == "X":
                cls = appear(out_t + lit_i * 0.035, 0.12)
                lit_i += 1
                body.append(
                    f'<rect x="{x}" y="{yy}" width="{CELL}" height="{CELL}" rx="3" fill="{t.green}" class="{cls}"/>'
                )
            else:
                body.append(
                    f'<rect x="{x}" y="{yy}" width="{CELL}" height="{CELL}" rx="3" fill="{t.faint}" fill-opacity=".22"/>'
                )

    # info column
    y = out_y
    delay = out_t + 0.1
    body.append(
        f'<text x="{info_x:.1f}" y="{y}" class="{appear(delay)}">'
        f'<tspan class="g" font-weight="600">sadra</tspan><tspan class="v">@</tspan>'
        f'<tspan class="g" font-weight="600">rijswijk</tspan></text>'
    )
    y += LH
    body.append(f'<text x="{info_x:.1f}" y="{y}" class="f {appear(delay + 0.06)}">{"─" * 14}</text>')
    key_w = max(len(k) for k, _ in INFO) + 2
    for i, (k, v) in enumerate(INFO):
        y += LH
        body.append(
            f'<text x="{info_x:.1f}" y="{y}" class="{appear(delay + 0.12 + i * 0.07)}" xml:space="preserve">'
            f'<tspan class="k">{esc(k)}</tspan><tspan class="v" x="{info_x + key_w * CW:.1f}">{esc(v)}</tspan></text>'
        )
    y += LH * 2
    swatch_t = delay + 0.12 + len(INFO) * 0.07 + 0.1
    swatches = [t.text, t.muted, t.faint, t.border, t.red, t.yellow, t.green, "#3b82f6"]
    sw = [f'<g class="{appear(swatch_t)}">']
    for i, c in enumerate(swatches):
        sw.append(f'<rect x="{info_x + i * 30:.1f}" y="{y - 15}" width="30" height="18" fill="{c}"/>')
    sw.append("</g>")
    body.extend(sw)

    # fresh prompt with a blinking cursor
    p_cls = appear(swatch_t + 0.25)
    body.append(
        f'<g class="{p_cls}"><text x="{x0}" y="{prompt_y}"><tspan class="g">~</tspan>'
        f'<tspan class="v"> $ </tspan></text>'
        f'<rect x="{x0 + 4 * CW:.1f}" y="{prompt_y - FS * 0.82:.1f}" width="{CW * 0.9:.1f}" '
        f'height="{FS * 1.05:.1f}" fill="{t.text}" style="animation:blink 1.05s step-end infinite"/></g>'
    )
    body.append("</g>")

    return document(
        W,
        H,
        "".join(body),
        "".join(css),
        title="neofetch — sadra@rijswijk",
        desc="; ".join(f"{k}: {v}" for k, v in INFO),
    )
