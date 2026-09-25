from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.enum import CardEnumName
from readme.card.project.info import CardProjectInfo, CardProjectInfoSpec
from readme.card.project.project_base import CardProjectBase
from readme.card.project.tradingbot.log import CardProjectTradingbotLog
from readme.dock.dock import Dock
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink
from readme.svg.box import SvgBox
from readme.svg.fragment import SvgFragment


@dataclass(kw_only=True, slots=True)
class CardProjectTradingbot(CardProjectBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.PROJECT_TRADINGBOT
    ALT: ClassVar[str] = (
        "TradingBot: the modular quant framework I trade my own capital with. Private repository."
    )
    DOCK: ClassVar[Dock | None] = Dock(
        href=constants.URL_RESUME_QUANT,
        rows=(
            (
                DockLink(
                    label="The quant resume",
                    href=constants.URL_RESUME_QUANT,
                    icon=DockEnumIcon.DOC,
                ),
                DockLink(
                    label="Ask me for a walkthrough",
                    href=constants.URL_EMAIL,
                    icon=DockEnumIcon.MAIL,
                ),
            ),
        ),
    )
    SPACED: ClassVar[bool] = True
    INFO: ClassVar[CardProjectInfo] = CardProjectInfo(
        title="TradingBot",
        eyebrow="QUANT · PYTHON · ML",
        period="2025 — NOW",
        description="The modular quant framework I trade my own capital with: four uncorrelated strategies "
        "across tickers and timeframes, where a backtest has to earn its way into production.",
        specs=(
            CardProjectInfoSpec(
                key="scoring",
                value="PyTorch position scoring · chained validators",
            ),
            CardProjectInfoSpec(
                key="validation",
                value="walk-forward · Monte Carlo · Bayesian opt.",
            ),
            CardProjectInfoSpec(
                key="risk", value="drawdown kill switches · adaptive sizing"
            ),
            CardProjectInfoSpec(
                key="runtime",
                value="multiprocess pipeline · Redis cache · Docker",
            ),
        ),
    )

    def visual(self) -> SvgFragment:
        return CardProjectTradingbotLog(
            theme=self.theme,
            box=SvgBox(x=0, y=0, width=self.PANEL_WIDTH, height=self.HEIGHT),
        ).render()
