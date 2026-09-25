"""`neofetch --stack`: the ">_" LED matrix on the left, my tech stack on the right.

Plays once: types the command, lights the matrix, then the stack chips rise in.
"""

from __future__ import annotations

from stack import STACK, stack_rows, stack_summary
from svg import MONO, MONO_ADVANCE, Theme, card_frame, clip_card, document, font_css

W = 1000
FS = 15
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



def about(t: Theme) -> str:
    x0, title_h = 36, 44
    cmd_y = title_h + 38
    out_y = cmd_y + 40
    info_x = x0 + len(MATRIX[0]) * (CELL + GAP) + 44
    cmd = "neofetch --stack"
    out_t = 0.35 + len(cmd) * 0.07 + 0.35
    my = out_y - 6
    stack_svg, stack_css, stack_bottom = stack_rows(t, info_x, W - x0, my, start=out_t + 0.3, label_w=118)
    matrix_bottom = my + len(MATRIX) * (CELL + GAP)
    prompt_y = max(stack_bottom, matrix_bottom) + 48
    H = prompt_y + 34

    css = [
        font_css(("sgm", 400), ("sgm", 600), ("sgs", 400)),
        stack_css,
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
    for i, ch in enumerate(cmd):
        if ch != " ":
            body.append(
                f'<text x="{x0 + (4 + i) * CW:.2f}" y="{cmd_y}" fill="{t.text}" '
                f'class="{appear(0.35 + i * 0.07)}">{ch}</text>'
            )

    # logo: LEDs power on one by one, in reading order
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

    # the stack, beside the matrix
    body.append(stack_svg)

    # fresh prompt with a blinking cursor
    chips = sum(len(items) for _, items in STACK)
    p_cls = appear(out_t + 0.3 + chips * 0.025 + 0.3)
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
        title="neofetch --stack",
        desc=stack_summary(),
    )
