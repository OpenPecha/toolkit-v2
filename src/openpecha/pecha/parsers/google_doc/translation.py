import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Tuple, Union

import openpyxl
from docx import Document

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import InitialCreationType, Language, PechaMetaData
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

    @staticmethod
    def get_layer_enum_with_lang(lang: str):
        if lang == Language.english.value:
            return LayerEnum.english_segment

        if lang == Language.tibetan.value:
            return LayerEnum.tibetan_segment

        if lang == Language.chinese.value:
            return LayerEnum.chinese_segment

        assert f"Language not properly given in metadata path: {str(input)}."

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
        # Iterate through rows, now including ZH column
        for row in sheet.iter_rows(
            min_row=2, max_row=sheet.max_row, min_col=1, max_col=4, values_only=True
        ):
            key, bo_value, en_value, zh_value = row

            # Ensure key exists before adding to metadata
            if key:
                entry = {}
                if bo_value:
                    entry["BO"] = bo_value.strip()
                if en_value:
                    entry["EN"] = en_value.strip()
                if zh_value:
                    entry["ZH"] = zh_value.strip()

                if entry:
                    metadata[key] = entry

        language: Dict = metadata.get("language", {})
        input_lang = next(value for value in language.values() if value)
        metadata["language"] = input_lang

        metadata["title"] = metadata["title_short"]
        return metadata

    def extract_root_idx(self, input: Path):
        extracted_text = self.extract_root_idx_from_doc(input)
        self.base = "\n".join(extracted_text.values())
        count = 0

        layer_enum = self.get_layer_enum_with_lang(self.metadata["language"])

        for root_idx, base in extracted_text.items():
            curr_ann = {
                layer_enum.value: {
                    "start": count,
                    "end": count + len(base),
                },
                "root_idx_mapping": root_idx,
            }
            self.anns.append(curr_ann)
            count += len(base) + 1

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

        if self.source_path:
            self.metadata["source_path"] = self.source_path

        self.extract_root_idx(input)
        pecha, layer_path = self.create_pecha(output_path)
        return pecha, layer_path

    def create_pecha(self, output_path: Path) -> Tuple[Pecha, Path]:
        pecha = Pecha.create(output_path)
        basename = pecha.set_base(self.base)

        layer_enum = self.get_layer_enum_with_lang(self.metadata["language"])
        # Add meaning_segment layer
        meaning_segment_layer, layer_path = pecha.add_layer(basename, layer_enum)
        for ann in self.anns:
            pecha.add_annotation(meaning_segment_layer, ann, layer_enum)
        meaning_segment_layer.save()

        pecha.set_metadata(
            PechaMetaData(
                id=pecha.id,
                parser="GoogleDocTranslationParser",
                **self.metadata,
                initial_creation_type=InitialCreationType.google_docx,
            )
        )

        # Get layer path relative to Pecha Path
        index = layer_path.parts.index(
            pecha.id
        )  # Find where the key starts in the parts
        relative_layer_path = Path(*layer_path.parts[index:])

        return (pecha, relative_layer_path)
