from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.blupdate import DiffMatchPatch
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
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
            segmentation_coords, old_base = parser.extract_segmentation_coordinates(
                docx_file
            )

            new_basename = list(pecha.bases.keys())[0]
            new_base = pecha.get_base(new_basename)

            diff_update = DiffMatchPatch(old_base, new_base)

            updated_coords = []
            for coord in segmentation_coords:
                start = int(coord["start"])
                end = int(coord["end"])

                updated_coords.append(
                    {
                        "start": diff_update.get_updated_coord(start),
                        "end": diff_update.get_updated_coord(end),
                        "root_idx_mapping": coord.get("root_idx_mapping", ""),
                    }
                )
            layer_path = parser.add_segmentation_annotations(
                pecha, updated_coords, ann_type
            )
            pecha.add_annotation_metadata(
                new_basename,
                layer_path.stem,
                {"annotation_title": ann_title, "annotation_type": ann_type.value},
            )
            return layer_path

        elif self.is_commentary_related_pecha(pecha_type):
            commentary_parser = DocxSimpleCommentaryParser()
            (
                segmentation_coords,
                old_base,
            ) = commentary_parser.extract_segmentation_coordinates(docx_file)
            new_basename = list(pecha.bases.keys())[0]
            new_base = pecha.get_base(new_basename)

            diff_update = DiffMatchPatch(old_base, new_base)

            updated_coords = []
            for coord in segmentation_coords:
                start = int(coord["start"])
                end = int(coord["end"])

                updated_coords.append(
                    {
                        "start": diff_update.get_updated_coord(start),
                        "end": diff_update.get_updated_coord(end),
                        "root_idx_mapping": coord.get("root_idx_mapping", ""),
                    }
                )
            layer_path = commentary_parser.add_segmentation_annotations(
                pecha, updated_coords, ann_type
            )

            pecha_id = parent_layer_path.split("/")[0] if parent_layer_path else None
            pecha.add_annotation_metadata(
                new_basename,
                layer_path.stem,
                {
                    "annotation_title": ann_title,
                    "relationship": ["commentary_of", pecha_id, parent_layer_path],
                    "annotation_type": ann_type.value,
                },
            )
            return layer_path

        else:
            raise ValueError(f"Unknown pecha type: {pecha_type}")
