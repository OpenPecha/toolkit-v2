import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Union

import openpyxl
from docx import Document

from openpecha.config import PECHAS_PATH


class GoogleDocTranslationParser:
    def __init__(self):
        self.root_idx_regex = r"^\d+\.\s"
        self.bo_data = {}

    def get_docx_content(self, input):
        docs = Document(input)
        docs_texts = [para.text.strip() for para in docs.paragraphs]
        # Ignore the first element, it is title
        docs_texts = docs_texts[1:]

        # If last element is empty, remove it
        if docs_texts and not docs_texts[-1]:
            docs_texts.pop()
        return docs_texts

    def extract_metadata_from_xlsx(self, input: Path):
        # Load the workbook
        workbook = openpyxl.load_workbook(input)

        # Access the first sheet
        sheet = workbook.active

        # Initialize a dictionary to store metadata
        metadata = {}

        # Extract entries from the sheet
        for row in sheet.iter_rows(
            min_row=2, max_row=sheet.max_row, min_col=1, max_col=3, values_only=True
        ):
            key, bo_value, en_value = row

            # Ensure key exists before adding to metadata
            if key:
                metadata[key] = {
                    "BO": bo_value.strip() if bo_value else None,
                    "EN": en_value.strip() if en_value else None,
                }

        language: Dict = metadata.get("language", {})
        input_lang = next(value for value in language.values() if value)
        metadata["language"] = input_lang
        return metadata

    def parse_bo(self, input: Path):
        docx_texts = self.get_docx_content(input)

        bo_content = OrderedDict()
        for text in docx_texts:
            match = re.match(self.root_idx_regex, text)
            if match:
                root_idx = match.group(0).strip()
                root_idx_int = int(root_idx.replace(".", ""))  # This is an integer

                clean_text = text[len(root_idx) :].strip()
                bo_content[
                    str(root_idx_int)
                ] = clean_text  # Store root_idx as string in bo_content

        bo_base = "\n".join(bo_content.values())
        anns = []
        count = 0
        for root_idx, base in bo_content.items():
            curr_ann = {
                "Span": {"start": count, "end": count + len(base)},
                "root_idx_mapping": root_idx,
            }
            anns.append(curr_ann)
            count += len(base) + 1

        self.bo_data["base"] = bo_base
        self.bo_data["anns"] = anns
        pass

    def parse_bo_translation(self):
        pass

    def parse(
        self,
        input: Path,
        metadata: Path,
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
        metadata = self.extract_metadata_from_xlsx(metadata)
        if not source_path:
            self.parse_bo(input)
            self.bo_metadata = metadata
        else:
            self.parse_bo_translation()
        pass
