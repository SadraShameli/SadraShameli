from readme.card.project.enum import CardProjectEnumStyle
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.theme import SvgTheme


class CardProjectStyle:
    __slots__ = ()

    @staticmethod
    def css(theme: SvgTheme) -> str:
        mono = SvgEnumFontFamily.MONO.stack

        return SvgFont.css(
            SvgEnumFont.MONO_REGULAR,
            SvgEnumFont.SANS_REGULAR,
            SvgEnumFont.SANS_SEMIBOLD,
            SvgEnumFont.DISPLAY_EXTRABOLD,
        ) + (
            f".{CardProjectEnumStyle.EYEBROW}{{font-family:{mono};font-size:12px;letter-spacing:2px;fill:{theme.muted}}}"
            f".{CardProjectEnumStyle.TITLE}{{font-family:{SvgEnumFontFamily.DISPLAY.stack};font-weight:800;fill:{theme.text}}}"
            f".{CardProjectEnumStyle.DESCRIPTION}{{font-family:{SvgEnumFontFamily.SANS.stack};font-size:16px;fill:{theme.muted}}}"
            f".{CardProjectEnumStyle.SPEC_KEY}{{font-family:{mono};font-size:13px;fill:{theme.faint}}}"
            f".{CardProjectEnumStyle.SPEC_VALUE}{{font-family:{mono};font-size:13px;fill:{theme.text}}}"
            f".{CardProjectEnumStyle.LINK}{{font-family:{mono};font-size:13px;fill:{theme.text}}}"
            "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.2}}"
        )
