from dataclasses import dataclass

from readme.svg.theme import SvgTheme
from readme.util.repository import UtilRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class CardContext:
    theme: SvgTheme
    repository: UtilRepository
