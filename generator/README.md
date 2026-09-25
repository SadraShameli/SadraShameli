# readme

Draws every card in [`Assets/Readme`](../Assets/Readme) and keeps the profile `README.md` pointing at them. It's a [uv](https://docs.astral.sh/uv/) project on Python 3.14, and drawing the cards needs nothing beyond the standard library.

```sh
cd generator
uv run readme          # draw every card, then repoint README.md at them
uv run readme photos   # re-crop the photos in Images/Cards, after adding or changing one
```

From the repo root it's `uv run --project generator readme`. On the first run uv fetches Python 3.14 and the dev group: Pillow (only `photos` uses it), ruff, ty and pre-commit.

Every push to `main` runs [`.github/workflows/readme.yml`](../.github/workflows/readme.yml): it checks the code, rebuilds the cards and commits them if anything changed. The same checks run locally before a push:

```sh
uv run pre-commit install                                  # once; hooks run on git push
uv run pre-commit run --all-files --hook-stage pre-push    # or run them now: ruff, ty, uv lock --check, yaml/toml/json
uv run ruff format && uv run ruff check && uv run ty check # or one at a time
```

Everything below lives in `src/readme/`.

| File | What it does |
|---|---|
| `cli.py` | the `readme` command: builds every card, deletes stale ones, repoints the README |
| `hero.py` | the banner: the `whoami` typo gag and the isometric SensorHub with its firmware's LED pattern |
| `intro.py` | the intro: the end-to-end pipeline and the by day / by night panels |
| `btop.py` | `btop --user sadra`: a system monitor of me, with a scrolling LED cpu graph, mem gauges and the projects as processes (edit `MEM`, `PROCS`) |
| `cards.py` | project cards and tiles (edit `FEATURED` / `TILES` to change the copy) |
| `terminal.py` | the YouTube and documents terminals (edit `VIDEOS`, `DOCUMENTS`) |
| `dock.py` | the link buttons that form the bottom edge of a card (edit `DOCKS`); `readme_html()` prints the matching README markup |
| `footer.py` | the `exit` at the bottom |
| `svg.py` | themes, embedded fonts, text measuring |
| `photos.py` | the photo and thumbnail crops the cards embed (`uv run readme photos`) |
| `paths.py` | where the repo, the generated cards and the photos live |

Every card is built twice, `-dark` and `-light`, and the README picks one with `<picture>`. File names carry a hash of their contents (`hero-dark.1a2b3c4d.svg`), and the build rewrites the README to match, so a browser can't mix a cached old card with new buttons. A README image can only link to one place, so each button is its own tiny SVG: the card is drawn with an open bottom and the buttons sit flush under it (`align="top"` and no whitespace between them), so together they read as one card. Animations are CSS, and each element's resting style is its final frame, so `prefers-reduced-motion` still gets a complete picture.

Fonts: [Geist](https://github.com/vercel/geist-font) and [Orbitron](https://github.com/theleagueof/orbitron), subset to the glyphs used, under the SIL Open Font License ([`fonts`](src/readme/fonts)).
