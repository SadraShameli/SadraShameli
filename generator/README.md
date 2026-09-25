# readme

Draws every card in [`Assets/Readme`](../Assets/Readme) and writes the profile [`README.md`](../README.md) around them. It's a [uv](https://docs.astral.sh/uv/) project on Python 3.14 with a [click](https://click.palletsprojects.com/) CLI. The cards are plain SVG drawn with the standard library; Pillow is only used to crop the photos.

```sh
cd generator
make build     # uv run readme build: draw every card, write README.md
make photos    # uv run readme photos: re-crop Images/Cards after adding or changing a photo
make tests     # uv run pytest
make lint      # ruff format, then the pre-push hooks: ruff, ty, uv lock --check, yaml/toml/json
```

From the repo root it's `uv run --project generator readme`. Every push to `main` runs [`.github/workflows/readme.yml`](../.github/workflows/readme.yml): it runs the hooks and the tests, rebuilds, and commits the cards and the README if anything changed. Run `uv run pre-commit install` once to get the same hooks on `git push`.

## Layout

Everything lives in `src/readme/`. Class names mirror the folder path (`card/project/photo_base.py` holds `CardProjectPhotoBase`), and `tests/` mirrors `src/readme/` file for file.

| Folder | What it does |
|---|---|
| `card/` | `CardBase` and one plugin per card, found through `CARD_REGISTRY`. `CardEnumName` is the page order; `CardBuilder` renders every card for both themes, prunes stale files and writes the README with `CardPage` |
| `card/hero/` | the banner: the `whoami` typo gag and the isometric SensorHub blinking its firmware's LED pattern |
| `card/intro/`, `card/btop/` | the pipeline with the by day / by night panels, and `btop --user sadra` |
| `card/project/` | the wide project cards; photo cards get the Vercel-style showcase, TradingBot its live log |
| `card/tile/` | the half-width tiles |
| `card/youtube/`, `card/documents/`, `card/footer/` | the terminal cards and the `exit` |
| `dock/` | the link buttons that form the bottom edge of a card |
| `svg/` | themes, embedded fonts and text measuring, frames, photos, the showcase |
| `photo/` | the crops the cards embed (`readme photos`) |
| `plugin/`, `logger/`, `util/`, `command/` | the registry, logging, locating the repository, and the CLI |

To add a card, add a `CardEnumName` member where it belongs on the page and a `card/<name>/card.py` whose class subclasses `CardBase` and sets `NAME`. Links under a card go in its `DOCK`.

Every card is built twice, `-dark` and `-light`, and the README picks one with `<picture>`. File names carry a hash of their contents (`hero-dark.1a2b3c4d.svg`), so a browser can't mix a cached old card with new buttons. A README image can only link to one place, so each button is its own tiny SVG: the card is drawn with an open bottom and the buttons sit flush under it (`align="top"` and no whitespace between them), so together they read as one card. Animations are CSS, and each element's resting style is its final frame, so `prefers-reduced-motion` still gets a complete picture.

Fonts: [Geist](https://github.com/vercel/geist-font) and [Orbitron](https://github.com/theleagueof/orbitron), subset to the glyphs used, under the SIL Open Font License ([`fonts`](src/readme/svg/fonts)).
