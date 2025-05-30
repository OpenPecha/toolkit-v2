import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from openpecha.config import PECHAS_PATH, get_logger
from openpecha.exceptions import FileNotFoundError
from openpecha.pecha import Pecha, annotation_path
from openpecha.pecha.annotations import (
    AlignmentAnnotation,
    SegmentationAnnotation,
    Span,
)
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers import DocxBaseParser
from openpecha.pecha.parsers.docx.utils import extract_numbered_list

logger = get_logger(__name__)


class DocxSimpleCommentaryParser(DocxBaseParser):
    def __init__(self):
        self.root_alignment_index_regex = r"^([\d\-,]+)\s(.*)"

    def validate_annotation_type(self, annotation_type: AnnotationType):
        if annotation_type not in [
            AnnotationType.SEGMENTATION,
            AnnotationType.ALIGNMENT,
        ]:
            raise NotImplementedError(
                f"Annotation type {annotation_type} is not supported to extract segmentation."
            )

    def calculate_segment_coordinates(
        self, segments: Dict[str, str], annotation_type: AnnotationType
    ) -> Tuple[List[SegmentationAnnotation | AlignmentAnnotation], str]:
        """Calculate start and end positions for each segment and build base text.

        Args:
            segments: Dictionary mapping with index and text

        Returns:
            Tuple containing:
            - List of dicts with start/end positions for each segment
            - Combined base text with all segments
        """
        self.validate_annotation_type(annotation_type)

        anns = []
        base = ""
        char_count = 0

        if annotation_type == AnnotationType.SEGMENTATION:
            for index, segment in segments.items():
                anns.append(
                    SegmentationAnnotation(
                        span=Span(start=char_count, end=char_count + len(segment)),
                        index=index,
                    )
                )
                base += f"{segment}\n"
                char_count += len(segment) + 1

        else:
            for index, segment in segments.items():
                match = re.match(self.root_alignment_index_regex, segment)

                alignment_index = match.group(1) if match else index
                segment = match.group(2) if match else segment

                anns.append(
                    AlignmentAnnotation(
                        span=Span(start=char_count, end=char_count + len(segment)),
                        index=index,
                        alignment_index=alignment_index,
                    )
                )
                base += f"{segment}\n"

                char_count += len(segment) + 1

        return (anns, base)

    def get_segmentation_anns(
        self, docx_file: Path, annotation_type: AnnotationType
    ) -> Tuple[List[SegmentationAnnotation | AlignmentAnnotation], str]:
        """
        Extract text from docx and calculate coordinates for segments.
        """
        numbered_text = extract_numbered_list(docx_file)
        return self.calculate_segment_coordinates(numbered_text, annotation_type)

    def parse(
        self,
        input: str | Path,
        annotation_type: AnnotationType,
        metadata: Dict[str, Any],
        output_path: Path = PECHAS_PATH,
        pecha_id: str | None = None,
    ) -> Tuple[Pecha, annotation_path]:
        """
        Parse a docx file and create a pecha.
        Steps:
            1. Extract text and calculate coordinates
            2. Extract segmentation annotations
            3. Initialize pecha with annotations and metadata
        """
        input = Path(input)
        if not input.exists():
            logger.error(f"The input docx file {str(input)} does not exist.")
            raise FileNotFoundError(
                f"[Error] The input docx file '{str(input)}' does not exist."
            )

        output_path.mkdir(parents=True, exist_ok=True)

        anns, base = self.get_segmentation_anns(input, annotation_type)

        pecha = self.create_pecha(base, output_path, metadata, pecha_id)
        annotation_path = self.add_segmentation_layer(pecha, anns, annotation_type)

        logger.info(f"Pecha {pecha.id} is created successfully.")
        return (pecha, annotation_path)
