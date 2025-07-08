from pathlib import Path
from openpecha.pecha import Pecha
from diff_match_patch import diff_match_patch


from openpecha.pecha.parsers.docx.utils import extract_numbered_list
from openpecha.pecha.annotations import SegmentationAnnotation, Span, SpellingVariantAnnotation

class DocxEditionParser:
    def __init__(self):
        self.dmp = diff_match_patch()
        self.dmp.Diff_Timeout = 0
        self.dmp.Diff_EditCost = 4
        self.dmp.Match_Threshold = 0.5
        self.dmp.Match_Distance = 100
        self.dmp.Patch_DeleteThreshold = 0.5
        # Patch_Margin and Match_MaxBits can remain defaults

    def parse_segmentation_from_text(self, numbered_text: dict):
        anns = []
        char_count = 0
        for index, segment in numbered_text.items():
            anns.append(
                SegmentationAnnotation(
                    span=Span(start=char_count, end=char_count + len(segment)),
                    index=index,
                )
            )
            char_count += len(segment) + 1

        return anns


    def parse_segmentation(self, input: str | Path) -> str:
        """
        Extract text from docx and calculate coordinates for segments.
        """
        numbered_text = extract_numbered_list(input)
        anns = self.parse_segmentation_from_text(numbered_text)
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
                anns.append(
                    SpellingVariantAnnotation(
                        span=Span(start=char_count, end=char_count),
                        operation="insertion",
                        text=text
                    )
                )

            else:
                anns.append(
                    SpellingVariantAnnotation(
                        span=Span(start=char_count, end=char_count + len(text)),
                        operation="deletion"
                    )
                )

            char_count += len(text)
        return anns
