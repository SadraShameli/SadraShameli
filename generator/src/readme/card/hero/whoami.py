from dataclasses import dataclass
from typing import ClassVar

from readme.card.hero.enum import CardHeroEnumStyle
from readme.svg.constants import SVG_MONO_ADVANCE
from readme.svg.fragment import SvgFragment
from readme.svg.theme import SvgTheme
from readme.svg.util import esc, pct


@dataclass(kw_only=True, frozen=True, slots=True)
class CardHeroWhoamiChar:
    char: str
    on: float
    off: float
    y: int
    column: int
    style: CardHeroEnumStyle


@dataclass(kw_only=True, frozen=True, slots=True)
class CardHeroWhoamiCursor:
    time: float
    y: int
    column: int


@dataclass(kw_only=True, frozen=True, slots=True)
class CardHeroWhoami:
    LOOP: ClassVar[float] = 13.0
    END: ClassVar[float] = 12.3
    X: ClassVar[int] = 48
    COMMAND_Y: ClassVar[int] = 262
    OUTPUT_Y: ClassVar[int] = 296
    FONT_SIZE: ClassVar[int] = 19
    CHAR_WIDTH: ClassVar[float] = FONT_SIZE * SVG_MONO_ADVANCE
    CWD: ClassVar[str] = "~/rijswijk"
    PROMPT: ClassVar[str] = f"{CWD} $ "
    COMMAND: ClassVar[str] = "whoami"
    COMMAND_ON: ClassVar[float] = 0.8
    COMMAND_STEP: ClassVar[float] = 0.09
    NEWLINE_ON: ClassVar[float] = 1.75
    TYPO: ClassVar[str] = "sandra"
    TYPO_ON: ClassVar[float] = 2.0
    TYPO_STEP: ClassVar[float] = 0.1
    SQUIGGLE_ON: ClassVar[float] = 2.9
    SQUIGGLE_AFTER: ClassVar[float] = 0.3
    BACKSPACE_ON: ClassVar[float] = 3.5
    BACKSPACE_STEP: ClassVar[float] = 0.08
    KEPT: ClassVar[int] = 2
    FIX: ClassVar[str] = "dra"
    FIX_ON: ClassVar[float] = 4.05
    COMMENT: ClassVar[str] = "  // not sandra. never was."
    COMMENT_ON: ClassVar[float] = 4.75
    COMMENT_STEP: ClassVar[float] = 0.03

    theme: SvgTheme

    @property
    def answer(self) -> str:
        return self.TYPO[: self.KEPT] + self.FIX

    def backspaces(self) -> dict[int, float]:
        return {
            column: self.BACKSPACE_ON + step * self.BACKSPACE_STEP
            for step, column in enumerate(
                range(len(self.TYPO) - 1, self.KEPT - 1, -1)
            )
        }

    def chars(self) -> list[CardHeroWhoamiChar]:
        backspaces = self.backspaces()
        start = len(self.PROMPT)
        comment_start = len(self.answer)

        return [
            *(
                CardHeroWhoamiChar(
                    char=char,
                    on=self.COMMAND_ON + i * self.COMMAND_STEP,
                    off=self.END,
                    y=self.COMMAND_Y,
                    column=start + i,
                    style=CardHeroEnumStyle.COMMAND,
                )
                for i, char in enumerate(self.COMMAND)
            ),
            *(
                CardHeroWhoamiChar(
                    char=char,
                    on=self.TYPO_ON + i * self.TYPO_STEP,
                    off=backspaces.get(i, self.END),
                    y=self.OUTPUT_Y,
                    column=i,
                    style=CardHeroEnumStyle.OUTPUT,
                )
                for i, char in enumerate(self.TYPO)
            ),
            *(
                CardHeroWhoamiChar(
                    char=char,
                    on=self.FIX_ON + i * self.TYPO_STEP,
                    off=self.END,
                    y=self.OUTPUT_Y,
                    column=self.KEPT + i,
                    style=CardHeroEnumStyle.OUTPUT,
                )
                for i, char in enumerate(self.FIX)
            ),
            *(
                CardHeroWhoamiChar(
                    char=char,
                    on=self.COMMENT_ON + i * self.COMMENT_STEP,
                    off=self.END,
                    y=self.OUTPUT_Y,
                    column=comment_start + i,
                    style=CardHeroEnumStyle.COMMENT,
                )
                for i, char in enumerate(self.COMMENT)
            ),
        ]

    def cursors(self) -> list[CardHeroWhoamiCursor]:
        start = len(self.PROMPT)
        comment_end = len(self.answer) + len(self.COMMENT)

        return [
            CardHeroWhoamiCursor(time=0, y=self.COMMAND_Y, column=start),
            *(
                CardHeroWhoamiCursor(
                    time=self.COMMAND_ON + i * self.COMMAND_STEP,
                    y=self.COMMAND_Y,
                    column=start + i + 1,
                )
                for i in range(len(self.COMMAND))
            ),
            CardHeroWhoamiCursor(
                time=self.NEWLINE_ON, y=self.OUTPUT_Y, column=0
            ),
            *(
                CardHeroWhoamiCursor(
                    time=self.TYPO_ON + i * self.TYPO_STEP,
                    y=self.OUTPUT_Y,
                    column=i + 1,
                )
                for i in range(len(self.TYPO))
            ),
            *(
                CardHeroWhoamiCursor(time=time, y=self.OUTPUT_Y, column=column)
                for column, time in self.backspaces().items()
            ),
            *(
                CardHeroWhoamiCursor(
                    time=self.FIX_ON + i * self.TYPO_STEP,
                    y=self.OUTPUT_Y,
                    column=self.KEPT + 1 + i,
                )
                for i in range(len(self.FIX))
            ),
            CardHeroWhoamiCursor(
                time=self.COMMENT_ON + len(self.COMMENT) * self.COMMENT_STEP,
                y=self.OUTPUT_Y,
                column=comment_end,
            ),
            CardHeroWhoamiCursor(
                time=self.END, y=self.COMMAND_Y, column=start
            ),
        ]

    def render(self) -> SvgFragment:
        t, loop, cw = self.theme, self.LOOP, self.CHAR_WIDTH
        css, texts = [], []

        for n, char in enumerate(self.chars()):
            if char.char == " ":
                continue

            css.append(
                f"@keyframes k{n}{{0%{{opacity:0}}{pct(char.on, loop)}{{opacity:1}}"
                f"{pct(char.off, loop)}{{opacity:0}}100%{{opacity:0}}}}"
                f"#c{n}{{animation:k{n} {loop}s step-end infinite}}"
            )
            hidden = ' opacity="0"' if char.off < self.END else ""
            texts.append(
                f'<text id="c{n}" class="{char.style}" x="{self.X + char.column * cw:.2f}" '
                f'y="{char.y}"{hidden}>{esc(char.char)}</text>'
            )

        frames = "".join(
            f"{pct(cursor.time, loop)}{{transform:translate({cursor.column * cw:.2f}px,"
            f"{cursor.y - self.COMMAND_Y}px)}}"
            for cursor in self.cursors()
        )
        rest = len(self.answer) + len(self.COMMENT)
        css.append(
            f"@keyframes cur{{{frames}100%{{transform:translate({len(self.PROMPT) * cw:.2f}px,0px)}}}}"
            f"#cur{{animation:cur {loop}s step-end infinite;"
            f"transform:translate({rest * cw:.2f}px,{self.OUTPUT_Y - self.COMMAND_Y}px)}}"
            "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
            "#curb{animation:blink 1.05s step-end infinite}"
        )
        size = self.FONT_SIZE
        cursor = (
            f'<g id="cur"><rect id="curb" x="{self.X}" y="{self.COMMAND_Y - size * 0.82:.2f}" '
            f'width="{cw * 0.9:.2f}" height="{size * 1.05:.2f}" fill="{t.text}" opacity=".85"/></g>'
        )
        wave = "".join(
            f"q{cw / 4:.2f} {-3 if k % 2 else 3} {cw / 2:.2f} 0"
            for k in range(12)
        )
        squiggle = (
            f'<path id="sq" d="M{self.X} {self.OUTPUT_Y + 6}{wave}" fill="none" stroke="{t.red}" '
            f'stroke-width="1.6" stroke-linecap="round" opacity="0"/>'
        )
        squiggle_off = self.BACKSPACE_ON + self.SQUIGGLE_AFTER
        css.append(
            f"@keyframes sq{{0%{{opacity:0}}{pct(self.SQUIGGLE_ON, loop)}{{opacity:1}}"
            f"{pct(squiggle_off, loop)}{{opacity:0}}}}"
            f"#sq{{animation:sq {loop}s step-end infinite}}"
        )
        prompt = (
            f'<text class="{CardHeroEnumStyle.PROMPT}" x="{self.X}" y="{self.COMMAND_Y}">'
            f'<tspan fill="{t.green}">{self.CWD}</tspan><tspan fill="{t.muted}"> $ </tspan></text>'
        )

        return SvgFragment(
            body=prompt + "".join(texts) + squiggle + cursor,
            css="".join(css),
        )
