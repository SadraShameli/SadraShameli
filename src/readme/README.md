# readme

Draws every card in [`Assets/Readme`](../../Assets/Readme) and keeps the profile `README.md` pointing at them. It's a [uv](https://docs.astral.sh/uv/) project on Python 3.14, and drawing the cards needs nothing beyond the standard library.

```sh
uv run readme          # draw every card, then repoint README.md at them
uv run readme photos   # re-crop the photos in Images/Cards, after adding or changing one
```

On the first run uv fetches Python 3.14 and the dev group (Pillow, only used by `photos`).

| File | What it does |
|---|---|
| `cli.py` | the `readme` command: builds every card, deletes stale ones, repoints the README |
| `hero.py` | the banner: the `whoami` typo gag and the isometric SensorHub with its firmware's LED pattern |
| `intro.py` | the intro: the end-to-end pipeline and the by day / by night panels |
| `about.py` | `neofetch --stack`: the `>_` LED matrix with the tech stack chips beside it |
| `stack.py` | the tech stack chip rows drawn inside the `neofetch` card (edit `STACK`) |
| `cards.py` | project cards and tiles (edit `FEATURED` / `TILES` to change the copy) |
| `terminal.py` | the terminals: YouTube, documents, and the hiring / developer / robot ones (edit `HIRING`, `DEVELOPER`, `ME`) |
| `dock.py` | the link buttons that form the bottom edge of a card (edit `DOCKS`); `readme_html()` prints the matching README markup |
| `footer.py` | the `exit` at the bottom |
| `svg.py` | themes, embedded fonts, text measuring |
| `photos.py` | the photo and thumbnail crops the cards embed (`uv run readme photos`) |
| `paths.py` | where the repo, the generated cards and the photos live |

Every card is built twice, `-dark` and `-light`, and the README picks one with `<picture>`. File names carry a hash of their contents (`hero-dark.1a2b3c4d.svg`), and the build rewrites the README to match, so a browser can't mix a cached old card with new buttons. A README image can only link to one place, so each button is its own tiny SVG: the card is drawn with an open bottom and the buttons sit flush under it (`align="top"` and no whitespace between them), so together they read as one card. Animations are CSS, and each element's resting style is its final frame, so `prefers-reduced-motion` still gets a complete picture.

Fonts: [Geist](https://github.com/vercel/geist-font) and [Orbitron](https://github.com/theleagueof/orbitron), subset to the glyphs used, under the SIL Open Font License ([`fonts`](fonts)).
