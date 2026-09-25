import hashlib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from readme.card.card_base import CARD_REGISTRY, CardBase
from readme.card.constants import CARD_HASH_LENGTH, CARD_SUFFIX
from readme.card.context import CardContext
from readme.card.page import CardPage
from readme.card.picture import CardPicture
from readme.logger.logger_base import LoggerBase
from readme.svg.enum import SvgEnumTheme
from readme.svg.theme import SvgTheme
from readme.util.repository import UtilRepository


@dataclass(kw_only=True, slots=True)
class CardBuilder(LoggerBase):
    repository: UtilRepository

    def run(self) -> None:
        CARD_REGISTRY.discover()
        cards = CARD_REGISTRY.ordered()
        written = self._write(cards)
        files = {
            path for themes in written.values() for path in themes.values()
        }

        for stale in self.repository.assets.rglob(f"*{CARD_SUFFIX}"):
            if stale not in files:
                stale.unlink()

        pictures = {
            stem: CardPicture(
                dark=self.repository.relative(themes[SvgEnumTheme.DARK]),
                light=self.repository.relative(themes[SvgEnumTheme.LIGHT]),
            )
            for stem, themes in written.items()
        }
        self.repository.readme.write_text(
            CardPage(cards=cards, pictures=pictures).render(), encoding="utf-8"
        )

        self.logger.info(
            "%d cards in %s, %s written",
            len(files),
            self.repository.relative(self.repository.assets),
            self.repository.relative(self.repository.readme),
        )

    def _write(
        self, cards: tuple[type[CardBase], ...]
    ) -> dict[str, dict[SvgEnumTheme, Path]]:
        written: defaultdict[str, dict[SvgEnumTheme, Path]] = defaultdict(dict)

        for theme in SvgEnumTheme:
            context = CardContext(
                theme=SvgTheme.of(theme), repository=self.repository
            )

            for card in cards:
                for stem, document in (
                    card(context=context).documents().items()
                ):
                    svg = document.render()
                    digest = hashlib.sha1(svg.encode()).hexdigest()
                    path = self.repository.assets / (
                        f"{stem}-{theme}.{digest[:CARD_HASH_LENGTH]}{CARD_SUFFIX}"
                    )
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(svg, encoding="utf-8")
                    written[stem][theme] = path

        return written
