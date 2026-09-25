from enum import StrEnum, auto


class CardEnumName(StrEnum):
    HERO = "hero"
    INTRO = "intro"
    BTOP = "btop"
    PROJECT_TRADINGBOT = "project-tradingbot"
    PROJECT_SENSORHUB = "project-sensorhub"
    PROJECT_PROJECTAI = "project-projectai"
    TILE_SADRA_NL = "tile-sadra-nl"
    TILE_PROP_CALCULATOR = "tile-prop-calculator"
    TILE_MINOMARKT = "tile-minomarkt"
    TILE_LAB = "tile-lab"
    YOUTUBE = "youtube"
    DOCUMENTS = "documents"
    FOOTER = "footer"


class CardEnumLayout(StrEnum):
    BLOCK = auto()
    TILE = auto()


class CardEnumDiscoveryFile(StrEnum):
    CARD = "card.py"
