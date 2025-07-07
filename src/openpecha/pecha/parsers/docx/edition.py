from pathlib import Path
from openpecha.pecha import Pecha

from openpecha.pecha.parsers.docx.utils import extract_numbered_list

class DocxEditionParser:
    def parse_segmentation(self, input: str | Path) -> str:
        numbered_text = extract_numbered_list(input)
        anns = []
        char_count = 0

        for index, segment in numbered_text.items():
            anns.append({
                 "Span": {"start": char_count, "end": char_count + len(segment)},
                "index": index
            })
            char_count += len(segment) + 1

        return anns

    def parse_spelling_variant(self, input: str | Path) -> str:
        pass 