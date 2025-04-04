from pathlib import Path
from typing import Tuple

from openpecha.pecha import Pecha


class DocxAnnotationParser:
    def __init__(self):
        pass

    def add_annotation(
        self,
        pecha: Pecha,
        ann_name: str,
        ann_title: str,
        docx_url: str,
        relation_ship_data: Tuple[str, str, str],
        docx_file: Path,
    ):
        pass
