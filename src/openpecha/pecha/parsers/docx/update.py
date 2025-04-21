from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum


class DocxAnnotationUpdate:
    def update_annotation(
        self, pecha: Pecha, ann_type: LayerEnum, docx_file: Path, metadatas: List[Dict]
    ):
        pass

    def update_root_pecha_layer(
        self, pecha: Pecha, ann_type: LayerEnum, docx_file: Path, metadatas: List[Dict]
    ):
        pass

    def update_commentary_pecha_layer(
        self, pecha: Pecha, ann_type: LayerEnum, docx_file: Path, metadatas: List[Dict]
    ):
        pass
