from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.root.number_list_root import DocxRootParser
from openpecha.pecha.pecha_types import PechaType, get_pecha_type

pecha_id = str
layer_name = str


class DocxAnnotationParser:
    def __init__(self):
        pass

    def is_root_related_pecha(self, pecha_type: PechaType) -> bool:
        """
        Returns True if the pecha type is root-related.
        """
        return pecha_type in [
            PechaType.root_pecha,
            PechaType.root_translation_pecha,
            PechaType.prealigned_root_translation_pecha,
        ]

    def is_commentary_related_pecha(self, pecha_type: PechaType) -> bool:
        """
        Returns True if the pecha type is commentary-related.
        """
        return pecha_type in [
            PechaType.commentary_pecha,
            PechaType.commentary_translation_pecha,
            PechaType.prealigned_commentary_pecha,
            PechaType.prealigned_commentary_translation_pecha,
        ]

    def add_annotation(
        self,
        pecha: Pecha,
        ann_type: LayerEnum,
        ann_title: str,
        docx_file: Path,
        metadatas: List[Dict],
        parent_layer_path: str | None = None,
    ):
        pecha_type: PechaType = get_pecha_type(metadatas)

        if self.is_root_related_pecha(pecha_type):
            parser = DocxRootParser()
            segmentation_coords = parser.extract_segmentation_coordinates(  # noqa
                docx_file
            )
            pass
        elif self.is_commentary_related_pecha(pecha_type):
            pass

        else:
            raise ValueError(f"Unknown pecha type: {pecha_type}")
