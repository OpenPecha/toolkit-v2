import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Union

from docx import Document

from openpecha.config import PECHAS_PATH


class GoogleDocTranslationParser:
    def __init__(self):
        self.root_idx_regex = r"^\d+\.\s"
        self.bo_content = OrderedDict()

    def get_docx_content(self, input):
        docs = Document(input)
        docs_texts = [para.text.strip() for para in docs.paragraphs]
        # Ignore the first element, it is title
        docs_texts = docs_texts[1:]

        # If last element is empty, remove it
        if docs_texts and not docs_texts[-1]:
            docs_texts.pop()
        return docs_texts

    def parse_bo(self, input: Path):
        docx_texts = self.get_docx_content(input)
        for text in docx_texts:
            match = re.match(self.root_idx_regex, text)
            if match:
                root_idx = match.group(0).strip()
                root_idx_int = int(root_idx.replace(".", ""))

                clean_text = text[len(root_idx) :].strip()
                self.bo_content[root_idx_int] = clean_text
        pass

    def parse_bo_translation(self):
        pass

    def parse(
        self,
        input: Path,
        metadata: Union[Dict[str, Any], Path],
        source_path: Union[str, None] = None,
        output_path: Path = PECHAS_PATH,
    ):
        """
        Inputs:
            input: Docx file path
            metadata: metadata for the file
            source_path: Tibetan file is the source, Other lang is the target and are translate from
                         the source. It should be pecha id / layer name.
            output_path: Output path

        Process:
            - Get google doc content - parse and get root mappings

        Output:
            - Create OPF

        """
        if not source_path:
            self.parse_bo(input)
        pass
