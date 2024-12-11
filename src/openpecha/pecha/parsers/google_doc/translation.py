import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Union

import openpyxl
from docx import Document

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import PechaMetaData
from openpecha.pecha.parsers import BaseParser


class GoogleDocTranslationParser(BaseParser):
    def __init__(self, source_path: Union[str, None] = None):
        """
        source_path: Normaly, Tibetan file is the source i.e other lang files are translated based
                     on the tibetan file.
                     If tibetan lang file, set to None by default.
                     Else: source_path should be in this format=> pecha id / layer name.

        """
        self.root_idx_regex = r"^\d+\.\s"
        self.source_path = source_path
        self.anns: List[Dict] = []
        self.base = ""
        self.metadata: Dict = {}

    def get_docx_content(self, input):
        docs = Document(input)
        docs_texts = [para.text.strip() for para in docs.paragraphs]
        # Ignore the first element, it is title
        docs_texts = docs_texts[1:]

        # If last element is empty, remove it
        if docs_texts and not docs_texts[-1]:
            docs_texts.pop()
        return docs_texts

    def extract_root_idx_from_doc(self, input):
        docx_texts = self.get_docx_content(input)

        content = OrderedDict()
        for text in docx_texts:
            match = re.match(self.root_idx_regex, text)
            if match:
                root_idx = match.group(0).strip()
                root_idx_int = int(root_idx.replace(".", ""))  # This is an integer

                clean_text = text[len(root_idx) :].strip()
                content[
                    str(root_idx_int)
                ] = clean_text  # Store root_idx as string in extracted_text
        return content

    def extract_metadata_from_xlsx(self, input: Path):
        workbook = openpyxl.load_workbook(input)
        sheet = workbook.active

        metadata = {}
        for row in sheet.iter_rows(
            min_row=2, max_row=sheet.max_row, min_col=1, max_col=3, values_only=True
        ):
            key, bo_value, en_value = row

            # Ensure key exists before adding to metadata
            if key:
                entry = {}
                if bo_value:
                    entry["BO"] = bo_value.strip()
                if en_value:
                    entry["EN"] = en_value.strip()

                if entry:
                    metadata[key] = entry

        language: Dict = metadata.get("language", {})
        input_lang = next(value for value in language.values() if value)
        metadata["language"] = input_lang
        return metadata

    def extract_root_idx(self, input: Path):

        extracted_text = self.extract_root_idx_from_doc(input)
        self.base = "\n".join(extracted_text.values())
        count = 0
        for root_idx, base in extracted_text.items():
            curr_ann = {
                LayerEnum.root_segment.value: {
                    "start": count,
                    "end": count + len(base),
                },
                "root_idx_mapping": root_idx,
            }
            self.anns.append(curr_ann)
            count += len(base) + 1

        pass

    def parse(
        self,
        input: Path,
        metadata: Union[Dict, Path],
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
        if isinstance(metadata, Path):
            self.metadata = self.extract_metadata_from_xlsx(metadata)

        else:
            self.metadata = metadata

        self.extract_root_idx(input)
        self.create_pecha(output_path)

        pass

    def create_pecha(self, output_path: Path) -> Pecha:
        pecha = Pecha.create(output_path)
        basename = pecha.set_base(self.base)

        # Add meaning_segment layer
        meaning_segment_layer, _ = pecha.add_layer(basename, LayerEnum.root_segment)
        for ann in self.anns:
            pecha.add_annotation(meaning_segment_layer, ann, LayerEnum.root_segment)
        meaning_segment_layer.save()

        pecha.set_metadata(
            PechaMetaData(
                id=pecha.id, parser="GoogleDocTranslationParser", **self.metadata
            )
        )

        return pecha
