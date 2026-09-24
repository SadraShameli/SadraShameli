"""A terminal that logs out politely. Plays once."""

from __future__ import annotations

from svg import MONO, MONO_ADVANCE, Theme, card_frame, clip_card, document, esc, font_css

W, H, FS = 1000, 132, 16
CW = FS * MONO_ADVANCE


def footer(t: Theme) -> str:
    x0, y1, y2 = 36, 56, 88
    cmd = "exit"
    css = [
        font_css(("sgm", 400)),
        f"text{{font-family:{MONO};font-size:{FS}px}}",
        "@keyframes in{from{opacity:0}to{opacity:1}}",
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}",
    ]
    body = [
        "<defs>" + clip_card("clip", W, H, 14) + "</defs>",
        card_frame(t, W, H, 14),
        '<g clip-path="url(#clip)">',
        f'<text x="{x0}" y="{y1}"><tspan fill="{t.green}">~</tspan><tspan fill="{t.muted}"> $ </tspan></text>',
    ]
    for i, ch in enumerate(cmd):
        d = 0.6 + i * 0.12
        css.append(f".e{i}{{animation:in .01s linear {d:.2f}s both}}")
        body.append(f'<text x="{x0 + (4 + i) * CW:.1f}" y="{y1}" fill="{t.text}" class="e{i}">{ch}</text>')
    out_d = 0.6 + len(cmd) * 0.12 + 0.4
    css.append(f".o{{animation:in .3s ease-out {out_d:.2f}s both}}")
    msg = "logout. thanks for scrolling, come say hi at "
    body.append(
        f'<text x="{x0}" y="{y2}" class="o" fill="{t.muted}">{esc(msg)}'
        f'<tspan fill="{t.text}">sadra.nl</tspan></text>'
    )
    body.append(
        f'<text x="{W - x0}" y="{y2}" class="o" text-anchor="end" fill="{t.faint}" font-size="13">'
        "[process completed]</text>"
    )
    cur_x = x0 + (len(msg) + len("sadra.nl") + 1) * CW
    css.append(f".cu{{animation:in .01s linear {out_d + 0.3:.2f}s both}}")
    body.append(
        f'<g class="cu"><rect x="{cur_x:.1f}" y="{y2 - FS * 0.82:.1f}" width="{CW * 0.9:.1f}" '
        f'height="{FS * 1.05:.1f}" fill="{t.text}" style="animation:blink 1.05s step-end infinite"/></g>'
    )
    body.append("</g>")
    return document(W, H, "".join(body), "".join(css), title="exit", desc="logout. thanks for scrolling.")
