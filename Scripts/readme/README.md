# README graphics

Everything in [`Assets/Readme`](../../Assets/Readme) comes from here. Only the Python standard library is needed.

```sh
python3 Scripts/readme static   # hero, neofetch, projects, stack, youtube, documents, footer -> Assets/Readme
```

| File | What it draws |
|---|---|
| `hero.py` | the banner: the `whoami` typo gag and the isometric SensorHub with its firmware's LED pattern |
| `about.py` | `neofetch`, but it's me |
| `cards.py` | project cards and tiles (edit `FEATURED` / `TILES` to change the copy) |
| `stack.py` | the tech stack chips (edit `STACK`) |
| `terminal.py` | the `ls` terminals for YouTube and the documents |
| `footer.py` | the `exit` at the bottom |
| `svg.py` | themes, embedded fonts, text measuring |
| `prep_images.py` | one-off photo and thumbnail crops for the cards (needs Pillow) |

Every card is built twice, `-dark` and `-light`, and the README picks one with `<picture>`. Animations are CSS, and each element's resting style is its final frame, so `prefers-reduced-motion` still gets a complete picture.

Fonts: [Geist](https://github.com/vercel/geist-font) and [Orbitron](https://github.com/theleagueof/orbitron), subset to the glyphs used, under the SIL Open Font License ([`Scripts/fonts`](../fonts)).
