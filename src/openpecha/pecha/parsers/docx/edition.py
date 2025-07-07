from pathlib import Path
from openpecha.pecha import Pecha

from openpecha.pecha.parsers.docx.utils import extract_numbered_list, read_docx
from openpecha.pecha.blupdate import DiffMatchPatch

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

    def parse_spelling_variant(self, pecha: Pecha, input: str | Path) -> str:
        basename = list(pecha.bases.keys())[0]
        old_base = pecha.get_base(basename)
        new_base = read_docx(input)
        
        blupdate = DiffMatchPatch(old_base, new_base)
        diffs = blupdate.diffs

        pass 

