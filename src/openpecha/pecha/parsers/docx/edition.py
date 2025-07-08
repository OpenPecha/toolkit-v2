from pathlib import Path

from diff_match_patch import diff_match_patch

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import (
    SegmentationAnnotation,
    Span,
    SpellingVariantAnnotation,
)
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers.docx.utils import extract_numbered_list, update_coords


class DocxEditionParser:
    """
    Parser for extracting segmentation and spelling variant annotations from DOCX files.
    Only used in test context.
    """

    def __init__(self) -> None:
        self.dmp = diff_match_patch()
        self.dmp.Diff_Timeout = 0
        self.dmp.Diff_EditCost = 4
        self.dmp.Match_Threshold = 0.5
        self.dmp.Match_Distance = 100
        self.dmp.Patch_DeleteThreshold = 0.5
        # Patch_Margin and Match_MaxBits can remain defaults

    def parse_segmentation_from_text(
        self, numbered_text: dict
    ) -> list[SegmentationAnnotation]:
        """
        Create segmentation annotations from numbered text segments.
        """
        anns = []
        char_count = 0
        for index, segment in numbered_text.items():
            anns.append(
                SegmentationAnnotation(
                    span=Span(start=char_count, end=char_count + len(segment)),
                    index=index,
                )
            )
            char_count += len(segment) + 1  # +1 for newline or separator
        return anns

    def parse_segmentation(self, input: str | Path) -> list[SegmentationAnnotation]:
        """
        Extract text from docx and calculate coordinates for segments.
        """
        numbered_text = extract_numbered_list(input)
        return self.parse_segmentation_from_text(numbered_text)

    def parse_spelling_variant(
        self, source: str, target: str
    ) -> list[SpellingVariantAnnotation]:
        """
        Compute spelling variant annotations (insertions/deletions) between source and target strings.
        """
        diffs = self.dmp.diff_main(source, target, checklines=True)
        self.dmp.diff_cleanupSemantic(diffs)

        anns = []
        char_count = 0
        for marker, text in diffs:
            if marker == 0:
                char_count += len(text)

            elif marker == 1:
                # Insertion
                anns.append(
                    SpellingVariantAnnotation(
                        span=Span(start=char_count, end=char_count),
                        operation="insertion",
                        text=text,
                    )
                )
            else:
                # Deletion
                anns.append(
                    SpellingVariantAnnotation(
                        span=Span(start=char_count, end=char_count + len(text)),
                        operation="deletion",
                    )
                )
                char_count += len(text)
        return anns

    def parse(self, pecha: Pecha, input: str | Path):
        """
        Parse the DOCX file and add segmentation and spelling variant layers to the Pecha.
        Returns the relative paths to the created layers.
        """
        old_basename = list(pecha.bases.keys())[0]
        old_base = pecha.get_base(old_basename)

        numbered_text = extract_numbered_list(input)
        new_base = "\n".join(list(numbered_text.values()))

        seg_anns = self.parse_segmentation(input)
        updated_seg_anns = update_coords(seg_anns, old_base, new_base)
        spelling_var_anns = self.parse_spelling_variant(old_base, new_base)

        seg_layer_path = self.add_segmentation_layer(pecha, updated_seg_anns)
        spelling_variant_path = self.add_spelling_variant_layer(
            pecha, spelling_var_anns
        )

        return seg_layer_path, spelling_variant_path

    def add_segmentation_layer(
        self, pecha: Pecha, anns: list[SegmentationAnnotation]
    ) -> str:
        """
        Add a segmentation layer to the Pecha and return its relative path.
        """
        basename = list(pecha.bases.keys())[0]
        layer, layer_path = pecha.add_layer(basename, AnnotationType.SEGMENTATION)
        for ann in anns:
            pecha.add_annotation(layer, ann, AnnotationType.SEGMENTATION)
        layer.save()
        return str(layer_path.relative_to(pecha.layer_path))

    def add_spelling_variant_layer(
        self, pecha: Pecha, anns: list[SpellingVariantAnnotation]
    ) -> str:
        """
        Add a spelling variant layer to the Pecha and return its relative path.
        """
        basename = list(pecha.bases.keys())[0]
        layer, layer_path = pecha.add_layer(basename, AnnotationType.SPELLING_VARIANT)
        for ann in anns:
            pecha.add_annotation(layer, ann, AnnotationType.SPELLING_VARIANT)
        layer.save()
        return str(layer_path.relative_to(pecha.layer_path))
