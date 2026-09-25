"""Tech stack as rows of monochrome icon chips, grouped by what I use them for.

Drawn inside the `neofetch --stack` terminal (about.py)."""

import json
from functools import lru_cache

from .paths import ICONS
from .svg import MONO, SANS, Theme, esc, measure

# (label, simple-icons slug or None). Sources: resumes, the old README, sadra.nl's
# package.json, the SensorHub repo and the Project A.I. thesis.
STACK: list[tuple[str, list[tuple[str, str | None]]]] = [
    ("languages", [
        ("TypeScript", "typescript"), ("JavaScript", "javascript"), ("Python", "python"), ("C++", "cplusplus"),
        ("C", "c"), ("C#", None), ("PHP", "php"), ("SQL", None), ("HTML & CSS", "html5"),
    ]),
    ("web", [
        ("React", "react"), ("Next.js", "nextdotjs"), ("Tailwind CSS", "tailwindcss"), ("shadcn/ui", "shadcnui"),
        ("Radix UI", "radixui"), ("Sass", "sass"), ("Bootstrap", "bootstrap"), ("Material UI", "mui"),
        ("daisyUI", "daisyui"), ("Framer Motion", "framer"), ("TanStack Query", "reactquery"),
        ("TanStack Table", "reacttable"), ("React Hook Form", "reacthookform"), ("Recharts", None),
    ]),
    ("backend", [
        ("Node.js", "nodedotjs"), ("Bun", "bun"), ("tRPC", "trpc"), ("Zod", "zod"), ("Better Auth", "betterauth"),
        ("NextAuth.js", None), ("ASP.NET", "dotnet"), ("Entity Framework", None), ("REST APIs", None),
        ("WordPress", "wordpress"), ("WooCommerce", "woocommerce"), ("Twig", None), ("Resend", "resend"),
        ("Google Maps API", "googlemaps"),
    ]),
    ("data", [
        ("PostgreSQL", "postgresql"), ("MySQL", "mysql"), ("SQL Server", None), ("Redis", "redis"),
        ("Drizzle", "drizzle"), ("Prisma", "prisma"),
    ]),
    ("firmware", [
        ("ESP-IDF", "espressif"), ("FreeRTOS", None), ("Arduino", "arduino"), ("PlatformIO", "platformio"),
        ("MicroPython", "micropython"), ("Raspberry Pi", "raspberrypi"), ("CMake", "cmake"), ("I²C · I²S", None),
    ]),
    ("ml & quant", [
        ("PyTorch", "pytorch"), ("TensorFlow", "tensorflow"), ("TensorFlow Lite", "tensorflow"), ("Keras", "keras"),
        ("OpenCV", "opencv"), ("NumPy", "numpy"), ("Pandas", "pandas"), ("Pydantic", "pydantic"),
    ]),
    ("ship it", [
        ("Git", "git"), ("GitHub Actions", "githubactions"), ("Azure DevOps", None), ("Docker", "docker"),
        ("Linux", "linux"), ("Vercel", "vercel"), ("Sentry", "sentry"), ("Vitest", "vitest"),
        ("Playwright", None), ("ESLint", "eslint"), ("Prettier", "prettier"), ("clang-tidy", "llvm"),
    ]),
    ("make it", [
        ("Fusion 360", "autodesk"), ("Blender", "blender"), ("PrusaSlicer", None), ("Ultimaker Cura", None),
        ("Altium", None), ("Proteus", None), ("Prusa MK3S+", None), ("Prusa Mini+", None), ("Vertex K8400", None),
    ]),
    ("graphics", [("DirectX 12", None), ("Ray tracing", None)]),
]


@lru_cache(maxsize=None)
def icons() -> dict[str, str]:
    return json.loads(ICONS.read_text())


def stack_rows(
    t: Theme,
    left: float,
    right: float,
    top: float,
    start: float = 0.15,
    label_w: float = 132,
    wrap_left: float | None = None,
    wrap_below: float = 0,
) -> tuple[str, str, float]:
    """The chip rows, laid out between `left` and `right` from `top` down.

    A group that starts below `wrap_below` moves out to `wrap_left`, so the rows can
    flow around something drawn to their left (the neofetch logo).
    Returns (svg, css, bottom y). Chips rise in one after another from `start` seconds.
    Needs the "sgm" 400 and "sgs" 400 fonts embedded by the caller.
    """
    x_max = right
    chip_h, gap, row_gap = 30, 7, 12
    fs = 13
    rows_svg: list[str] = []
    css = [
        f".lb{{font-family:{MONO};font-size:12px;letter-spacing:1.5px;fill:{t.muted}}}"
        f".cl{{font-family:{SANS};font-size:{fs}px;fill:{t.text}}}"
        "@keyframes up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}",
    ]
    y = top
    n = 0
    for label, items in STACK:
        if wrap_left is not None and y >= wrap_below:
            left = wrap_left
        x0 = left + label_w
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
                    f'<path transform="translate({x + 12:.1f} {y + (chip_h - 16) / 2}) scale({s:.4f})" '
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
