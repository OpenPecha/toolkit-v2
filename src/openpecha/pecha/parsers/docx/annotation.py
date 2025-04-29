from pathlib import Path
from typing import Dict, List, Tuple

from openpecha.config import get_logger
from openpecha.exceptions import ParseNotReadyForThisAnnotation
from openpecha.pecha import Pecha, annotation_path
from openpecha.pecha.blupdate import DiffMatchPatch
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
from openpecha.pecha.parsers.docx.root.number_list_root import DocxRootParser
from openpecha.pecha.pecha_types import (
    PechaType,
    get_pecha_type,
    is_commentary_related_pecha,
    is_root_related_pecha,
)

pecha_id = str

logger = get_logger(__name__)


class DocxAnnotationParser:
    def __init__(self):
        pass

    def get_updated_coords(
        self, coords: List[Dict[str, int]], old_base: str, new_base: str
    ):
        diff_update = DiffMatchPatch(old_base, new_base)

        updated_coords = []
        for coord in coords:
            start = int(coord["start"])
            end = int(coord["end"])

            updated_coords.append(
                {
                    "start": diff_update.get_updated_coord(start),
                    "end": diff_update.get_updated_coord(end),
                    "root_idx_mapping": coord.get("root_idx_mapping", ""),
                }
            )

        return updated_coords

    def add_annotation(
        self,
        pecha: Pecha,
        type: LayerEnum | str,
        docx_file: Path,
        metadatas: List[Dict],
    ) -> Tuple[Pecha, annotation_path]:
        pecha_type: PechaType = get_pecha_type(metadatas)

        # Accept both str and LayerEnum, convert str to LayerEnum
        if isinstance(type, str):
            try:
                type = LayerEnum(type)
            except ValueError:
                raise ParseNotReadyForThisAnnotation(f"Invalid annotation type: {type}")

        if type not in [LayerEnum.alignment, LayerEnum.segmentation]:
            raise ParseNotReadyForThisAnnotation(
                f"Parser is not ready for the annotation type: {type}"
            )

        # New Segmentation Layer should be updated to this existing base
        new_basename = list(pecha.bases.keys())[0]
        new_base = pecha.get_base(new_basename)

        if is_root_related_pecha(pecha_type):
            parser = DocxRootParser()
            coords, old_base = parser.extract_segmentation_coords(docx_file)

            updated_coords = self.get_updated_coords(coords, old_base, new_base)
            annotation_path = parser.add_segmentation_layer(pecha, updated_coords, type)
            logger.info(
                f"Alignment Annotation is successfully added to Pecha {pecha.id}"
            )
            return (pecha, annotation_path)

        elif is_commentary_related_pecha(pecha_type):
            commentary_parser = DocxSimpleCommentaryParser()
            (
                coords,
                old_base,
            ) = commentary_parser.extract_segmentation_coords(docx_file)

            updated_coords = self.get_updated_coords(coords, old_base, new_base)
            annotation_path = commentary_parser.add_segmentation_layer(
                pecha, updated_coords, type
            )
            logger.info(
                f"Alignment Annotation is successfully added to Pecha {pecha.id}"
            )
            return (pecha, annotation_path)

        else:
            raise ValueError(f"Unknown pecha type: {pecha_type}")
