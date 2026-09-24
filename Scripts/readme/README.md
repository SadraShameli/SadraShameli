# README graphics

Everything in [`Assets/Readme`](../../Assets/Readme) comes from here. Only the Python standard library is needed.

```sh
python3 Scripts/readme static   # every card -> Assets/Readme, then repoints README.md at them
```

| File | What it draws |
|---|---|
| `intro.py` | the intro: the end-to-end pipeline and the by day / by night panels |
| `hero.py` | the banner: the `whoami` typo gag and the isometric SensorHub with its firmware's LED pattern |
| `about.py` | `neofetch`, but it's me |
| `cards.py` | project cards and tiles (edit `FEATURED` / `TILES` to change the copy) |
| `stack.py` | the tech stack chips (edit `STACK`) |
| `terminal.py` | the terminals: YouTube, documents, and the hiring / developer / robot / Sandra ones (edit `HIRING`, `DEVELOPER`, `ME`) |
| `footer.py` | the `exit` at the bottom |
| `dock.py` | the link buttons that form the bottom edge of a card (edit `DOCKS`); `readme_html()` prints the matching README markup |
| `svg.py` | themes, embedded fonts, text measuring |
| `prep_images.py` | one-off photo and thumbnail crops for the cards (needs Pillow) |

Every card is built twice, `-dark` and `-light`, and the README picks one with `<picture>`. File names carry a hash of their contents (`hero-dark.1a2b3c4d.svg`), and the build rewrites the README to match, so a browser can't mix a cached old card with new buttons. A README image can only link to one place, so each button is its own tiny SVG: the card is drawn with an open bottom and the buttons sit flush under it (`align="top"` and no whitespace between them), so together they read as one card. Animations are CSS, and each element's resting style is its final frame, so `prefers-reduced-motion` still gets a complete picture.

Fonts: [Geist](https://github.com/vercel/geist-font) and [Orbitron](https://github.com/theleagueof/orbitron), subset to the glyphs used, under the SIL Open Font License ([`Scripts/fonts`](../fonts)).
