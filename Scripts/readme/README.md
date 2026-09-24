# README graphics

Everything in [`Assets/Readme`](../../Assets/Readme) and the live cards on the `output` branch come from here. Only the Python standard library is needed.

```sh
python3 Scripts/readme static            # hero, neofetch card, project cards, stack, footer -> Assets/Readme
python3 Scripts/readme live --out dist   # GitHub stats + SensorHub readings (needs STATS_TOKEN or GITHUB_TOKEN)
```

| File | What it draws |
|---|---|
| `hero.py` | the banner: the `whoami` typo gag and the isometric SensorHub with its firmware's LED pattern |
| `about.py` | `neofetch`, but it's me |
| `cards.py` | project cards and tiles (edit `FEATURED` / `TILES` to change the copy) |
| `stack.py` | the tech stack chips (edit `STACK`) |
| `footer.py` | the `exit` at the bottom |
| `live.py` | `contributions.wav`, the stats card and the SensorHub readings |
| `svg.py` | themes, embedded fonts, text measuring |
| `prep_images.py` | one-off photo crops for the cards (needs Pillow) |

Every card is built twice, `-dark` and `-light`, and the README picks one with `<picture>`. Animations are CSS, and each element's resting style is its final frame, so `prefers-reduced-motion` still gets a complete picture.

The [`README cards`](../../.github/workflows/readme.yml) workflow runs `live` every hour and force-pushes the result to the orphan `output` branch. If a source is down, its previous card stays. Add a personal access token as the `STATS_TOKEN` secret to include private contributions and repos.

Fonts: [Geist](https://github.com/vercel/geist-font) and [Orbitron](https://github.com/theleagueof/orbitron), subset to the glyphs used, under the SIL Open Font License ([`Scripts/fonts`](../fonts)).
