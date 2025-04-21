from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser


class DocxAnnotationUpdate:
    def update_annotation(
        self, pecha: Pecha, layer_name: str, docx_file: Path, metadatas: List[Dict]
    ):
        parser = DocxAnnotationParser()

        ann_type = LayerEnum.alignment
        parser.add_annotation(pecha, ann_type, docx_file, metadatas)
