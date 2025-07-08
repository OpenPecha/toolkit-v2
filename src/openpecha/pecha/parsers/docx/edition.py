from pathlib import Path
from openpecha.pecha import Pecha
from diff_match_patch import diff_match_patch


from openpecha.pecha.parsers.docx.utils import extract_numbered_list, read_docx

class DocxEditionParser:
    def __init__(self):
        self.dmp = diff_match_patch()
        self.dmp.Diff_Timeout = 0
        self.dmp.Diff_EditCost = 4
        self.dmp.Match_Threshold = 0.5
        self.dmp.Match_Distance = 100
        self.dmp.Patch_DeleteThreshold = 0.5
        # Patch_Margin and Match_MaxBits can remain defaults


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

    def parse_spelling_variant(self, source:str, target:str) -> str:
        diffs = self.dmp.diff_main(source, target, checklines=True)
        self.dmp.diff_cleanupSemantic(diffs)

        anns = []
        char_count = 0

        for marker, text in diffs:
            if marker == 0:
                pass 

            elif marker == 1:
                anns.append({"operation":"insertion", "start": char_count, "text": text})

            else:
                anns.append({"operation": "deletion", "start": char_count, "end": char_count + len(text)})

            char_count += len(text)
        return anns
