import re
from pathlib import Path
from typing import Dict, List, Tuple

from openpecha.config import PECHAS_PATH, get_logger
from openpecha.exceptions import FileNotFoundError, MetaDataValidationError
from openpecha.pecha import Pecha, annotation_path
from openpecha.pecha.annotations import SegmentationAnnotation, Span
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.metadata import InitialCreationType, PechaMetaData
from openpecha.pecha.parsers import DocxBaseParser
from openpecha.pecha.parsers.docx.utils import extract_numbered_list

logger = get_logger(__name__)


class DocxRootParser(DocxBaseParser):
    def calculate_segment_coordinates(
        self, segments: Dict[str, str]
    ) -> Tuple[List[SegmentationAnnotation], str]:
        """Calculate start and end positions for each segment and build base text.

        Args:
            segments: Dictionary mapping with index and text

        Returns:
            Tuple containing:
            - List of an Annotation model contain start/end positions for each segment and index payload
            - Combined base text with all segments
        """
        anns = []
        base = ""
        char_count = 0

        for index, segment in segments.items():
            anns.append(
                SegmentationAnnotation(
                    span=Span(start=char_count, end=char_count + len(segment)),
                    index=index,
                )
            )
            base += f"{segment}\n"
            char_count += len(segment) + 1

        return (anns, base)

    def get_segmentation_anns(
        self, docx_file: Path
    ) -> Tuple[List[SegmentationAnnotation], str]:
        """
        Extract text from docx and calculate coordinates for segments.
        """
        numbered_text = extract_numbered_list(docx_file)
        return self.calculate_segment_coordinates(numbered_text)

    def parse(
        self,
        input: str | Path,
        annotation_type: AnnotationType,
        metadata: Dict,
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

        anns, base = self.get_segmentation_anns(input)

        pecha = self.create_pecha(base, output_path, metadata, pecha_id)
        annotation_path = self.add_segmentation_layer(pecha, anns, annotation_type)

        logger.info(f"Pecha {pecha.id} is created successfully.")
        return (pecha, annotation_path)

    def create_pecha(
        self, base: str, output_path: Path, metadata: Dict, pecha_id: str | None
    ) -> Pecha:
        pecha = Pecha.create(output_path, pecha_id)
        pecha.set_base(base)

        try:
            pecha_metadata = PechaMetaData(
                id=pecha.id,
                parser=self.name,
                **metadata,
                bases={},
                initial_creation_type=InitialCreationType.google_docx,
            )
        except Exception as e:
            logger.error(f"The metadata given was not valid. {str(e)}")
            raise MetaDataValidationError(
                f"[Error] The metadata given was not valid. {str(e)}"
            )
        else:
            pecha.set_metadata(pecha_metadata.to_dict())

        return pecha

    def add_segmentation_layer(
        self, pecha: Pecha, anns: List[SegmentationAnnotation], ann_type: AnnotationType
    ) -> annotation_path:

        basename = list(pecha.bases.keys())[0]
        layer, layer_path = pecha.add_layer(basename, ann_type)
        for ann in anns:
            pecha.add_annotation(layer, ann, ann_type)
        layer.save()

        return str(layer_path.relative_to(pecha.layer_path))
