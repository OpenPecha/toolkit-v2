from pathlib import Path
from typing import Tuple

from openpecha.pecha import Pecha

relationship = str
pecha_id = str
layer_name = str


class DocxAnnotationParser:
    def __init__(self):
        pass

    def add_annotation(
        self,
        pecha: Pecha,
        ann_name: str,
        ann_title: str,
        docx_url: str,
        relation_ship_map: Tuple[relationship, pecha_id, layer_name],
        docx_file: Path,
    ):
        pass
