from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.enum import CardEnumName
from readme.card.project.info import CardProjectInfo
from readme.card.tile.tile_base import CardTileBase
from readme.photo.enum import PhotoEnumName


@dataclass(kw_only=True, slots=True)
class CardTileSadraNl(CardTileBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.TILE_SADRA_NL
    ALT: ClassVar[str] = (
        "sadra.nl: portfolio, live SensorHub dashboard, trading journal and more"
    )
    INFO: ClassVar[CardProjectInfo] = CardProjectInfo(
        title="sadra.nl",
        eyebrow="NEXT.JS 16 · TRPC · DRIZZLE",
        period="2024 — NOW",
        description="My corner of the web. One auth, API and design system shared by a portfolio, the live SensorHub dashboard, a trading journal, a resume generator and more.",
    )
    PHOTO: ClassVar[PhotoEnumName] = PhotoEnumName.SHOT_SADRA_NL
    HREF: ClassVar[str] = constants.URL_SITE
    LINK: ClassVar[str] = "↗ sadra.nl"
