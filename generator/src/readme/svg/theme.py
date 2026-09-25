from dataclasses import dataclass
from typing import Self

from readme.svg.constants import SVG_COLOR_BLACK, SVG_COLOR_WHITE
from readme.svg.enum import SvgEnumTheme


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgTheme:
    name: SvgEnumTheme
    bg: str
    panel: str
    border: str
    text: str
    muted: str
    faint: str
    dot: str
    dot_opacity: float
    red: str
    yellow: str
    green: str
    iso_top: str
    iso_left: str
    iso_right: str
    iso_edge: str
    screen: str
    screen_text: str
    photo_dim: float
    photo_grain: float
    device_shadow: str
    device_shadow_opacity: float
    name_shine_opacity: float
    showcase_spot: str
    showcase_spot_opacity: float
    showcase_frame: str
    showcase_frame_opacity: float

    @classmethod
    def of(cls, name: SvgEnumTheme) -> Self:
        match name:
            case SvgEnumTheme.DARK:
                return cls(
                    name=name,
                    bg="#000000",
                    panel="#0a0a0a",
                    border="#262626",
                    text="#fafafa",
                    muted="#a3a3a3",
                    faint="#525252",
                    dot="#ffffff",
                    dot_opacity=0.16,
                    red="#ef4444",
                    yellow="#eab308",
                    green="#22c55e",
                    iso_top="#141414",
                    iso_left="#0b0b0b",
                    iso_right="#1c1c1c",
                    iso_edge="#3a3a3a",
                    screen="#020617",
                    screen_text="#7dd3fc",
                    photo_dim=0.35,
                    photo_grain=0.2,
                    device_shadow=SVG_COLOR_WHITE,
                    device_shadow_opacity=0.07,
                    name_shine_opacity=0.55,
                    showcase_spot=SVG_COLOR_WHITE,
                    showcase_spot_opacity=0.1,
                    showcase_frame=SVG_COLOR_WHITE,
                    showcase_frame_opacity=0.16,
                )
            case SvgEnumTheme.LIGHT:
                return cls(
                    name=name,
                    bg="#ffffff",
                    panel="#fafafa",
                    border="#e5e5e5",
                    text="#0a0a0a",
                    muted="#525252",
                    faint="#a3a3a3",
                    dot="#000000",
                    dot_opacity=0.13,
                    red="#dc2626",
                    yellow="#ca8a04",
                    green="#16a34a",
                    iso_top="#f5f5f5",
                    iso_left="#e5e5e5",
                    iso_right="#fafafa",
                    iso_edge="#a3a3a3",
                    screen="#0f172a",
                    screen_text="#7dd3fc",
                    photo_dim=0.2,
                    photo_grain=0.14,
                    device_shadow=SVG_COLOR_BLACK,
                    device_shadow_opacity=0.16,
                    name_shine_opacity=0.0,
                    showcase_spot=SVG_COLOR_BLACK,
                    showcase_spot_opacity=0.05,
                    showcase_frame=SVG_COLOR_BLACK,
                    showcase_frame_opacity=0.14,
                )
