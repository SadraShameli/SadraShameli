from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.enum import CardEnumName
from readme.card.project.info import CardProjectInfo
from readme.card.tile.tile_base import CardTileBase
from readme.photo.enum import PhotoEnumName


@dataclass(kw_only=True, slots=True)
class CardTilePropCalculator(CardTileBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.TILE_PROP_CALCULATOR
    ALT: ClassVar[str] = (
        "Prop Calculator: Monte Carlo simulation against each futures prop firm's rules"
    )
    INFO: ClassVar[CardProjectInfo] = CardProjectInfo(
        title="Prop Calculator",
        eyebrow="MONTE CARLO · FUTURES",
        period="LIVE",
        description="Runs your trading system through a Monte Carlo against each prop firm's real drawdown, daily-loss and consistency rules to estimate pass odds, costs and payouts.",
    )
    PHOTO: ClassVar[PhotoEnumName] = PhotoEnumName.SHOT_PROP_CALCULATOR
    HREF: ClassVar[str] = constants.URL_PROP_CALCULATOR
    LINK: ClassVar[str] = "↗ sadra.nl/prop-calculator"
