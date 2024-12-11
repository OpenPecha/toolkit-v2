from pathlib import Path
from typing import Any, Dict, Union

from docx import Document

from openpecha.config import PECHAS_PATH


class GoogleDocTranslationParser:
    def __init__(self):
        pass

    def parse_bo(self):
        pass

    def parse_bo_translation(self):
        pass

    def parse(
        self,
        input: Path,
        metadata: Union[Dict[str, Any], Path],
        output_path: Path = PECHAS_PATH,
    ):
        docs = Document(input)
        docs_texts = [para.text.strip() for para in docs.paragraphs]
        # If last element is empty, remove it
        if docs_texts and not docs_texts[-1]:
            docs_texts.pop()
        pass
