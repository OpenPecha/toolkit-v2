from pathlib import Path

from openpecha.config import PECHAS_PATH
from openpecha.pecha.parsers import BaseParser, Document


class ChonjukPlainTextParser(BaseParser):
    def __init__(self, text: str):
        super().__init__(text)
        self.components = [ChapterParser()]

    def parse(self, output_path: Path = PECHAS_PATH):
        doc = Document(text=self.text)
        for component in self.components:
            doc = component(doc)

        return doc


class ChapterParser:
    def __call__(self, doc: Document):
        return doc
