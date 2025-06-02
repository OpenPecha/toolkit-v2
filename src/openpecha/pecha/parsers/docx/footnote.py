from pathlib import Path
from typing import List

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import FootnoteAnnotation
from openpecha.pecha.parsers.docx.utils import read_docx


class DocxFootnoteParser:
    def extract_footnote(self, text: str) -> List[FootnoteAnnotation]:
        pass

    def parse(self, pecha: Pecha, input: str | Path):
        text = read_docx(input)
        anns = self.extract_footnote(text)
        pass
