from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.enum import CardEnumName
from readme.card.project.info import CardProjectInfo
from readme.card.tile.tile_base import CardTileBase
from readme.photo.enum import PhotoEnumName


@dataclass(kw_only=True, slots=True)
class CardTileMinomarkt(CardTileBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.TILE_MINOMARKT
    ALT: ClassVar[str] = (
        "Mino Markt: WooCommerce storefront for a Persian market and grill in Alkmaar"
    )
    INFO: ClassVar[CardProjectInfo] = CardProjectInfo(
        title="Mino Markt",
        eyebrow="WOOCOMMERCE · PHP · TWIG",
        period="2024 — NOW",
        description="Storefront for a Persian market & grill in Alkmaar: online ordering, in-store pickup, loyalty points, subscriptions and live store availability.",
    )
    PHOTO: ClassVar[PhotoEnumName] = PhotoEnumName.SHOT_MINOMARKT_NL
    HREF: ClassVar[str] = constants.URL_MINOMARKT
    LINK: ClassVar[str] = "↗ minomarkt.nl"
