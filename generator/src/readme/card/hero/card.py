from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.card_base import CardBase
from readme.card.enum import CardEnumName
from readme.card.hero.device import CardHeroDevice
from readme.card.hero.enum import CardHeroEnumStyle
from readme.card.hero.whoami import CardHeroWhoami
from readme.dock.dock import Dock
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink
from readme.svg.constants import SVG_COLOR_BLACK, SVG_COLOR_WHITE
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont


@dataclass(kw_only=True, slots=True)
class CardHero(CardBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.HERO
    ALT: ClassVar[str] = (
        "Sadra Shameli: full-stack developer, futures trader, hardware tinkerer. "
        "A terminal types whoami, answers sandra, then fixes the typo to sadra."
    )
    DOCK: ClassVar[Dock | None] = Dock(
        href=constants.URL_SITE,
        rows=(
            (
                DockLink(
                    label="sadra.nl",
                    href=constants.URL_SITE,
                    icon=DockEnumIcon.GLOBE,
                ),
                DockLink(
                    label="LinkedIn",
                    href=constants.URL_LINKEDIN,
                    icon=DockEnumIcon.LINKEDIN,
                ),
                DockLink(
                    label="YouTube",
                    href=constants.URL_YOUTUBE,
                    icon=DockEnumIcon.YOUTUBE,
                ),
                DockLink(
                    label="Email",
                    href=constants.URL_EMAIL,
                    icon=DockEnumIcon.MAIL,
                ),
                DockLink(
                    label="Resume.pdf",
                    href=constants.URL_RESUME,
                    icon=DockEnumIcon.DOC,
                ),
            ),
        ),
    )
    HEIGHT: ClassVar[int] = 360
    FULL_NAME: ClassVar[str] = "SADRA SHAMELI"
    TITLE: ClassVar[str] = (
        "Sadra Shameli — full-stack developer, futures trader, hardware tinkerer"
    )
    DESCRIPTION: ClassVar[str] = (
        "A terminal types whoami, answers sandra, fixes the typo to sadra. "
        "Next to it an isometric SensorHub device blinks its LEDs."
    )
    DOT_SPACING: ClassVar[int] = 22
    DEVICE_X: ClassVar[int] = 730
    DEVICE_Y: ClassVar[int] = 172

    def render(self) -> SvgDocument:
        t, w, h = self.theme, self.WIDTH, self.HEIGHT
        whoami = CardHeroWhoami(theme=t).render()
        device = CardHeroDevice(
            theme=t, x=self.DEVICE_X, y=self.DEVICE_Y
        ).render()
        mono = SvgEnumFontFamily.MONO.stack
        display = SvgEnumFontFamily.DISPLAY.stack
        size = CardHeroWhoami.FONT_SIZE
        css = (
            SvgFont.css(
                SvgEnumFont.MONO_REGULAR,
                SvgEnumFont.MONO_SEMIBOLD,
                SvgEnumFont.DISPLAY_EXTRABOLD,
            )
            + f".{CardHeroEnumStyle.COMMAND},.{CardHeroEnumStyle.OUTPUT},.{CardHeroEnumStyle.PROMPT}"
            f"{{font-family:{mono};font-size:{size}px;fill:{t.text}}}"
            f".{CardHeroEnumStyle.PROMPT}{{fill:{t.muted}}}"
            f".{CardHeroEnumStyle.COMMENT}{{font-family:{mono};font-size:{size}px;fill:{t.faint}}}"
            + whoami.css
            + device.css
            + "@keyframes shine{0%{transform:translateX(-700px)}60%,100%{transform:translateX(900px)}}"
            "#shine{animation:shine 7s ease-in-out infinite}"
        )
        defs = (
            f'<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{SVG_COLOR_WHITE}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{SVG_COLOR_WHITE}" stop-opacity=".9"/>'
            f'<stop offset="1" stop-color="{SVG_COLOR_WHITE}" stop-opacity="0"/></linearGradient>'
            f'<mask id="nameMask"><rect width="{w}" height="{h}" fill="{SVG_COLOR_BLACK}"/>'
            + self._name(SVG_COLOR_WHITE)
            + "</mask>"
            f'<radialGradient id="shadow"><stop offset="0" stop-color="{t.device_shadow}" '
            f'stop-opacity="{t.device_shadow_opacity}"/>'
            '<stop offset="1" stop-opacity="0"/></radialGradient>'
            '<filter id="glow" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="3.2"/></filter>'
        )
        body = (
            self.frame(h).open(t, defs)
            + self._dot_grid()
            + f'<text x="48" y="62" font-family="{display}" font-weight="800" font-size="20" '
            f'fill="{t.text}">&gt;_sadra</text>'
            + f'<text x="952" y="60" text-anchor="end" font-family="{mono}" font-size="12" '
            f'letter-spacing="1.5" fill="{t.muted}">RIJSWIJK, NL  ·  52.04°N 4.32°E</text>'
            + self._name(t.text)
            + f'<g mask="url(#nameMask)" opacity="{t.name_shine_opacity}"><rect id="shine" x="0" y="110" '
            f'width="160" height="80" fill="url(#sh)"/></g>'
            + f'<text x="48" y="206" font-family="{mono}" font-size="15" fill="{t.muted}">'
            "full-stack developer  ·  futures trader  ·  hardware tinkerer</text>"
            + whoami.body
            + device.body
            + "</g>"
        )

        return SvgDocument(
            width=w,
            height=h,
            body=body,
            css=css,
            title=self.TITLE,
            description=self.DESCRIPTION,
        )

    def _name(self, fill: str) -> str:
        return (
            f'<text x="46" y="170" font-family="{SvgEnumFontFamily.DISPLAY.stack}" font-weight="800" '
            f'font-size="50" letter-spacing="1" fill="{fill}">{self.FULL_NAME}</text>'
        )

    def _dot_grid(self) -> str:
        t, w, h, spacing = (
            self.theme,
            self.WIDTH,
            self.HEIGHT,
            self.DOT_SPACING,
        )

        return (
            f'<defs><pattern id="dots" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse">'
            f'<circle cx="{spacing / 2}" cy="{spacing / 2}" r="1" fill="{t.dot}" '
            f'fill-opacity="{t.dot_opacity}"/></pattern>'
            '<radialGradient id="dots-f" cx="50%" cy="45%" r="75%">'
            f'<stop offset="0" stop-color="{SVG_COLOR_WHITE}" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="{SVG_COLOR_WHITE}" stop-opacity="0"/></radialGradient>'
            f'<mask id="dots-m"><rect width="{w}" height="{h}" fill="url(#dots-f)"/></mask></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#dots)" mask="url(#dots-m)"/>'
        )
