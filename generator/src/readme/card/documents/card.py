from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.card_base import CardBase
from readme.card.constants import CARD_TERMINAL_RADIUS
from readme.card.documents.document import CardDocumentsDocument
from readme.card.enum import CardEnumName
from readme.card.terminal import CardTerminal
from readme.dock.dock import Dock
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont
from readme.svg.util import esc


@dataclass(kw_only=True, slots=True)
class CardDocuments(CardBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.DOCUMENTS
    ALT: ClassVar[str] = (
        "Terminal listing my documents: letter of recommendation, a 95-page A.I. thesis in Dutch, "
        "and my quant and full-stack resumes"
    )
    DOCK: ClassVar[Dock | None] = Dock(
        href=constants.URL_DOCUMENTS,
        rows=(
            (
                DockLink(
                    label="Resume · full-stack",
                    href=constants.URL_RESUME,
                    icon=DockEnumIcon.DOC,
                ),
                DockLink(
                    label="Resume · quant",
                    href=constants.URL_RESUME_QUANT,
                    icon=DockEnumIcon.DOC,
                ),
                DockLink(
                    label="Letter of recommendation",
                    href=constants.URL_LETTER,
                    icon=DockEnumIcon.DOC,
                ),
                DockLink(
                    label="A.I. thesis (PWS)",
                    href=constants.URL_THESIS,
                    icon=DockEnumIcon.DOC,
                ),
            ),
            (
                DockLink(
                    label="Nobears",
                    href=constants.URL_NOBEARS,
                    icon=DockEnumIcon.GLOBE,
                ),
                DockLink(
                    label="Blue Star Planning",
                    href=constants.URL_BLUE_STAR_PLANNING,
                    icon=DockEnumIcon.GLOBE,
                ),
                DockLink(
                    label="sadra.nl source",
                    href=constants.URL_REPOSITORY_SADRA_NL,
                    icon=DockEnumIcon.GITHUB,
                ),
            ),
        ),
    )
    SPACED: ClassVar[bool] = True
    RADIUS: ClassVar[int] = CARD_TERMINAL_RADIUS
    MARGIN: ClassVar[int] = 36
    ROW_HEIGHT: ClassVar[int] = 26
    CWD: ClassVar[str] = "~/Documents"
    PERMISSIONS: ClassVar[str] = "-rw-r--r-- 1 sadra"
    DOCUMENTS: ClassVar[tuple[CardDocumentsDocument, ...]] = (
        CardDocumentsDocument(
            file=constants.DOCUMENT_LETTER,
            added="Dec 15  2023",
            note="in someone else's words",
        ),
        CardDocumentsDocument(
            file=constants.DOCUMENT_THESIS,
            added="Dec 15  2023",
            note="95-page A.I. thesis, in Dutch",
        ),
        CardDocumentsDocument(
            file=constants.DOCUMENT_RESUME_QUANT,
            added="May 26 10:01",
            note="the quant / TradingBot one",
        ),
        CardDocumentsDocument(
            file=constants.DOCUMENT_RESUME,
            added="May 26 10:01",
            note="the full-stack one",
        ),
    )

    def render(self) -> SvgDocument:
        t = self.theme
        term = CardTerminal(theme=t, title=f"sadra@rijswijk: {self.CWD}")
        x0, cmd_y = self.MARGIN, 84
        done = term.command(
            x0, cmd_y, self.CWD, "ls -lho {Resume*,Letter*,PWS*}"
        )
        sizes = [
            CardDocumentsDocument.human_size(
                (self.context.repository.documents / document.file)
                .stat()
                .st_size
            )
            for document in self.DOCUMENTS
        ]
        names = [f"'{document.file}'" for document in self.DOCUMENTS]
        size_w = max(len(size) for size in sizes)
        name_w = max(len(name) for name in names)
        y = cmd_y + 34

        for i, (document, size, name) in enumerate(
            zip(self.DOCUMENTS, sizes, names, strict=True)
        ):
            meta = f"{self.PERMISSIONS} {size.rjust(size_w)} {document.added} "
            note_x = x0 + (len(meta) + name_w + 3) * term.CHAR_WIDTH
            term.body.append(
                f'<g class="{term.appear(done + 0.25 + i * 0.12)}">'
                f'<text x="{x0}" y="{y}" xml:space="preserve"><tspan fill="{t.muted}">{esc(meta)}</tspan>'
                f'<tspan fill="{t.text}" font-weight="600">{esc(name)}</tspan></text>'
                f'<text x="{note_x:.1f}" y="{y}" fill="{t.green}"># {esc(document.note)}</text></g>'
            )
            y += self.ROW_HEIGHT

        prompt_y = y + 20
        end = done + 0.25 + len(self.DOCUMENTS) * 0.12 + 0.3
        term.cursor(term.prompt(x0, prompt_y, self.CWD), prompt_y, end)

        return term.render(
            frame=self.frame(prompt_y + 30),
            fonts=(SvgEnumFont.MONO_REGULAR, SvgEnumFont.MONO_SEMIBOLD),
            description="; ".join(
                f"{document.file}: {document.note}"
                for document in self.DOCUMENTS
            ),
        )
