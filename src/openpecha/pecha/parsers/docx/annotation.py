from pathlib import Path
from typing import Dict, List, Tuple

from openpecha.pecha import Pecha

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
        docx_file: Path,
        metadata_chain: List[Dict],
        relation_ship_map: Tuple[pecha_id, layer_name] | None = None,
    ):
        pass
