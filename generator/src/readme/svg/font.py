import base64
import json
from dataclasses import dataclass
from functools import cache
from typing import TypedDict, cast

from readme.svg.constants import (
    SVG_FONT_DIRECTORY,
    SVG_FONT_FALLBACK_GLYPH,
    SVG_FONT_METRICS,
    SVG_FONT_SUFFIX,
)
from readme.svg.enum import SvgEnumFont


class SvgFontMetricsPayload(TypedDict):
    upm: int
    adv: dict[str, int]


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgFontMetrics:
    units_per_em: int
    advances: dict[str, int]

    def advance(self, char: str) -> int:
        return self.advances.get(
            char,
            self.advances.get(SVG_FONT_FALLBACK_GLYPH, self.units_per_em // 2),
        )


class SvgFont:
    __slots__ = ()

    @staticmethod
    @cache
    def metrics(font: SvgEnumFont) -> SvgFontMetrics:
        payload = cast(
            dict[str, SvgFontMetricsPayload],
            json.loads(SVG_FONT_METRICS.read_text(encoding="utf-8")),
        )[font]

        return SvgFontMetrics(
            units_per_em=payload["upm"], advances=payload["adv"]
        )

    @staticmethod
    @cache
    def data(font: SvgEnumFont) -> str:
        return base64.b64encode(
            (SVG_FONT_DIRECTORY / f"{font}{SVG_FONT_SUFFIX}").read_bytes()
        ).decode()

    @staticmethod
    def css(*fonts: SvgEnumFont) -> str:
        return "".join(
            f"@font-face{{font-family:'{font.family}';font-weight:{font.weight};"
            f"src:url(data:font/woff2;base64,{SvgFont.data(font)}) format('woff2')}}"
            for font in fonts
        )

    @staticmethod
    def measure(
        text: str, font: SvgEnumFont, size: float, spacing: float = 0.0
    ) -> float:
        metrics = SvgFont.metrics(font)
        units = sum(metrics.advance(char) for char in text)

        return units / metrics.units_per_em * size + spacing * max(
            len(text) - 1, 0
        )

    @staticmethod
    def wrap(
        text: str, font: SvgEnumFont, size: float, width: float
    ) -> list[str]:
        lines, current = [], ""

        for word in text.split():
            trial = f"{current} {word}".strip()

            if current and SvgFont.measure(trial, font, size) > width:
                lines.append(current)
                current = word
            else:
                current = trial

        if current:
            lines.append(current)

        return lines
