from enum import IntEnum, StrEnum, auto


class SvgEnumTheme(StrEnum):
    DARK = auto()
    LIGHT = auto()


class SvgEnumFontFamily(StrEnum):
    MONO = "sgm"
    SANS = "sgs"
    DISPLAY = "sor"

    @property
    def stack(self) -> str:
        match self:
            case SvgEnumFontFamily.MONO:
                return f"'{self}',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
            case SvgEnumFontFamily.SANS:
                return f"'{self}',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
            case SvgEnumFontFamily.DISPLAY:
                return f"'{self}','{SvgEnumFontFamily.SANS}',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif"


class SvgEnumFontWeight(IntEnum):
    REGULAR = 400
    SEMIBOLD = 600
    EXTRABOLD = 800


class SvgEnumFont(StrEnum):
    MONO_REGULAR = "GeistMono-Regular"
    MONO_SEMIBOLD = "GeistMono-SemiBold"
    SANS_REGULAR = "Geist-Regular"
    SANS_SEMIBOLD = "Geist-SemiBold"
    DISPLAY_EXTRABOLD = "Orbitron-ExtraBold"

    @property
    def family(self) -> SvgEnumFontFamily:
        return SvgEnumFontFamily[self.name.partition("_")[0]]

    @property
    def weight(self) -> SvgEnumFontWeight:
        return SvgEnumFontWeight[self.name.partition("_")[2]]
