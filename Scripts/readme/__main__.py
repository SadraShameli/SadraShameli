"""Build the README graphics.

    python Scripts/readme static            # hand-designed cards -> Assets/Readme
    python Scripts/readme live --out DIR    # data-driven cards (GitHub + SensorHub)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from svg import ROOT, THEMES

STATIC_OUT = ROOT / "Assets" / "Readme"


def build_static(out: Path) -> None:
    from about import about
    from cards import all_cards
    from footer import footer
    from hero import hero
    from stack import stack

    out.mkdir(parents=True, exist_ok=True)
    for t in THEMES:
        files = {"hero": hero(t), "about": about(t), "stack": stack(t), "footer": footer(t), **all_cards(t)}
        for name, svg in files.items():
            (out / f"{name}-{t.name}.svg").write_text(svg, encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="readme")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("static")
    live = sub.add_parser("live")
    live.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.cmd == "static":
        build_static(STATIC_OUT)
    else:
        from live import build_live

        # a failed source keeps its previous cards, so this never fails the run
        build_live(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
