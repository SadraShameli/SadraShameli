"""Tech stack as rows of monochrome icon chips, grouped by what I use them for.

Drawn inside the `neofetch --stack` terminal (about.py)."""

import json
from functools import lru_cache

from .paths import ICONS
from .svg import MONO, SANS, Theme, esc, measure

# (label, simple-icons slug or None)
STACK: list[tuple[str, list[tuple[str, str | None]]]] = [
    ("web", [
        ("TypeScript", "typescript"), ("React", "react"), ("Next.js", "nextdotjs"),
        ("Tailwind CSS", "tailwindcss"), ("shadcn/ui", "shadcnui"), ("tRPC", "trpc"),
        ("TanStack Query", "reactquery"), ("Zod", "zod"), ("Better Auth", "betterauth"),
    ]),
    ("backend", [
        ("PHP", "php"), ("WordPress", "wordpress"), ("WooCommerce", "woocommerce"), ("Twig", None),
        (".NET", "dotnet"), ("Node.js", "nodedotjs"), ("Bun", "bun"),
    ]),
    ("data", [("PostgreSQL", "postgresql"), ("Drizzle", "drizzle"), ("MySQL", "mysql"), ("Redis", "redis")]),
    ("firmware", [
        ("C++", "cplusplus"), ("ESP-IDF", "espressif"), ("FreeRTOS", None), ("Arduino", "arduino"),
        ("PlatformIO", "platformio"),
    ]),
    ("quant & ml", [
        ("Python", "python"), ("PyTorch", "pytorch"), ("NumPy", "numpy"), ("Pandas", "pandas"),
        ("Pydantic", "pydantic"), ("TensorFlow", "tensorflow"),
    ]),
    ("ship it", [
        ("Docker", "docker"), ("GitHub Actions", "githubactions"), ("Vercel", "vercel"),
        ("Sentry", "sentry"), ("Vitest", "vitest"), ("Playwright", None), ("Git", "git"),
    ]),
    ("make it", [
        ("Fusion 360", "autodesk"), ("Blender", "blender"), ("PrusaSlicer", None),
        ("Prusa MK3S+", None), ("Prusa Mini+", None), ("Vertex K8400", None),
    ]),
]

@lru_cache(maxsize=None)
def icons() -> dict[str, str]:
    return json.loads(ICONS.read_text())


def stack_rows(t: Theme, left: float, right: float, top: float, start: float = 0.15,
               label_w: float = 132) -> tuple[str, str, float]:
    """The chip rows, laid out between `left` and `right` from `top` down.

    Returns (svg, css, bottom y). Chips rise in one after another from `start` seconds.
    Needs the "sgm" 400 and "sgs" 400 fonts embedded by the caller.
    """
    x0, x_max = left + label_w, right
    chip_h, gap, row_gap = 32, 8, 14
    fs = 13.5
    rows_svg: list[str] = []
    css = [
        f".lb{{font-family:{MONO};font-size:12px;letter-spacing:1.5px;fill:{t.muted}}}"
        f".cl{{font-family:{SANS};font-size:{fs}px;fill:{t.text}}}"
        "@keyframes up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}",
    ]
    y = top
    n = 0
    for label, items in STACK:
        rows_svg.append(f'<text x="{left}" y="{y + chip_h / 2 + 4}" class="lb">{esc(label.upper())}</text>')
        x = x0
        for name, slug in items:
            text_w = measure(name, "sans", 400, fs)
            w = text_w + (48 if slug else 34)
            if x + w > x_max:
                x = x0
                y += chip_h + gap
            n += 1
            css.append(f".c{n}{{animation:up .45s ease-out {start + n * 0.025:.3f}s both}}")
            chip = [
                f'<g class="c{n}"><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{chip_h}" rx="8" '
                f'fill="{t.panel}" stroke="{t.border}"/>'
            ]
            if slug:
                s = 16 / 24
                chip.append(
                    f'<path transform="translate({x + 12:.1f} {y + 8}) scale({s:.4f})" '
                    f'd="{icons()[slug]}" fill="{t.text}"/>'
                )
                tx = x + 36
            else:
                chip.append(
                    f'<rect x="{x + 12:.1f}" y="{y + chip_h / 2 - 3}" width="6" height="6" rx="1.5" '
                    f'fill="{t.faint}"/>'
                )
                tx = x + 24
            chip.append(f'<text x="{tx:.1f}" y="{y + chip_h / 2 + 4.6:.1f}" class="cl">{esc(name)}</text></g>')
            rows_svg.append("".join(chip))
            x += w + gap
        y += chip_h + row_gap
        rows_svg.append(
            f'<line x1="{left}" y1="{y - row_gap / 2:.1f}" x2="{x_max}" y2="{y - row_gap / 2:.1f}" '
            f'stroke="{t.border}" stroke-opacity=".6" stroke-dasharray="2 4"/>'
        )
        y += row_gap / 2
    # no separator under the last group
    return "".join(rows_svg[:-1]), "".join(css), y - row_gap * 1.5


def stack_summary() -> str:
    return "; ".join(f"{label}: {', '.join(n for n, _ in items)}" for label, items in STACK)
