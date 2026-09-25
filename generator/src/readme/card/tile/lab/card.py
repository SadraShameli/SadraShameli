from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.enum import CardEnumName
from readme.card.project.info import CardProjectInfo
from readme.card.tile.tile_base import CardTileBase
from readme.photo.enum import PhotoEnumName


@dataclass(kw_only=True, slots=True)
class CardTileLab(CardTileBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.TILE_LAB
    ALT: ClassVar[str] = (
        "The early lab: an Arduino Mega robot on a custom PCB and a 3D-printed social robot"
    )
    INFO: ClassVar[CardProjectInfo] = CardProjectInfo(
        title="The early lab",
        eyebrow="ARDUINO · PCB · 3D PRINTING",
        period="EARLY DAYS",
        description="Where it started: an Arduino Mega robot on a custom PCB packed with RFID, keypad, LCD and motor drivers, and a 3D-printed social robot with ultrasonic eyes.",
    )
    PHOTO: ClassVar[PhotoEnumName] = PhotoEnumName.SHOT_ROBOT
    HREF: ClassVar[str] = constants.URL_YOUTUBE
    LINK: ClassVar[str] = "↗ youtube.com/@SadraShameli"
