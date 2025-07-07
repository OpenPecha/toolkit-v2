from pathlib import Path
from openpecha.pecha import Pecha

from openpecha.pecha.parsers.docx.utils import extract_numbered_list

class DocxEditionParser:
    def parse_segmentation(self, input: str | Path) -> str:
        numbered_text = extract_numbered_list(input)
        return numbered_text

    def parse_spelling_variant(self, pecha: Pecha, input: str | Path) -> str:
        pass 