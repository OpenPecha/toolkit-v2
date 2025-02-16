import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Tuple, Union

from docx import Document

from openpecha.config import PECHAS_PATH
from openpecha.exceptions import InvalidLanguageEnumError
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import InitialCreationType, Language, PechaMetaData
from openpecha.pecha.parsers import BaseParser


class GoogleDocTranslationParser(BaseParser):
    def __init__(self):
        """
        source_path: Normaly, Tibetan file is the source i.e other lang files are translated based
                     on the tibetan file.
                     If tibetan lang file, set to None by default.
                     Else: source_path should be in this format=> pecha id / layer name.

        """
        self.root_idx_regex = r"^\d+\."

    @staticmethod
    def get_layer_enum_with_lang(lang: str):
        if lang == Language.english.value:
            return LayerEnum.english_segment

        if lang == Language.tibetan.value:
            return LayerEnum.tibetan_segment

        if lang == Language.chinese.value:
            return LayerEnum.chinese_segment

        if lang == Language.sanskrit.value:
            return LayerEnum.sanskrit_segment

        if lang == Language.italian.value:
            return LayerEnum.italian_segment

        raise InvalidLanguageEnumError(
            f"[Error] The language enum '{lang}' from metadata is invalid."
        )

    def get_docx_content(self, input):
        docs = Document(input)
        docs_texts = [
            para.text.strip() for para in docs.paragraphs if para.text.strip()
        ]

        # Remove the Byte Order Mark (BOM) if present
        if docs_texts[0].startswith("\ufeff"):
            docs_texts[0] = docs_texts[0][1:]

        return docs_texts

    def get_txt_content(self, input):
        # Read the text content from the input file
        text = input.read_text(encoding="utf-8")

        # Remove the Byte Order Mark (BOM) if present
        if text.startswith("\ufeff"):
            text = text[1:]

        # Split the text into lines, strip whitespace, and ignore empty lines
        texts = [line.strip() for line in text.splitlines() if line.strip()]

        return texts

    def remove_unwanted_annotations(self, text: List[str]):
        """
        Remove annotations.(Mostly annotations not needed or parser not build for it yet)
        """
        # Remove foot note annotations
        text = [re.sub(r"\[\d+\]", "", line) for line in text]
        return text

    def extract_root_idx_from_doc(self, input: Path):
        if input.name.endswith(".docx"):
            docx_texts = self.get_docx_content(input)

        else:
            docx_texts = self.get_txt_content(input)

        docx_texts = self.remove_unwanted_annotations(docx_texts)

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

    def extract_root_idx(
        self,
        input: Path,
        metadata: Dict,
    ) -> Tuple[List[Dict], str]:
        """
        1.Extract root idx from the input file .docx or .txt
        2.Return
            i)Root annotations
            ii)base text with no root annotations,

        """
        extracted_text = self.extract_root_idx_from_doc(input)
        extracted_segments = list(extracted_text.values())
        extracted_segments = [segment for segment in extracted_segments if segment]

        base = "\n".join(extracted_segments)

        layer_enum = self.get_layer_enum_with_lang(metadata["language"])

        count = 0
        anns: List[Dict] = []
        for root_idx, segment in extracted_text.items():
            curr_ann = {
                layer_enum.value: {
                    "start": count,
                    "end": count + len(segment),
                },
                "root_idx_mapping": root_idx,
            }
            anns.append(curr_ann)
            count += len(segment)

            if segment and count + 1 < len(base):
                count += 1
        return (anns, base)

    def parse(
        self,
        input: Union[str, Path],
        metadata: Dict,
        output_path: Path = PECHAS_PATH,
        pecha_id: Union[str, None] = None,
    ) -> "Pecha":
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
        input = Path(input)
        anns, base = self.extract_root_idx(input, metadata)
        pecha, _ = self.create_pecha(
            anns, base, metadata, output_path, pecha_id  # type: ignore
        )
        return pecha

    def create_pecha(
        self,
        anns: List[Dict],
        base: str,
        metadata: Dict,
        output_path: Path,
        pecha_id: str,
    ) -> Tuple[Pecha, Path]:
        pecha = Pecha.create(output_path, pecha_id)
        basename = pecha.set_base(base)

        layer_enum = self.get_layer_enum_with_lang(metadata["language"])

        # Add meaning_segment layer
        meaning_segment_layer, layer_path = pecha.add_layer(basename, layer_enum)
        for ann in anns:
            pecha.add_annotation(meaning_segment_layer, ann, layer_enum)
        meaning_segment_layer.save()

        # set base metadata
        bases = [
            {
                basename: {
                    "source_metadata": {"total_segments": len(anns)},
                    "base_file": f"{basename}.txt",
                }
            }
        ]

        # Get layer path relative to Pecha Path
        index = layer_path.parts.index(pecha.id)
        relative_layer_path = Path(*layer_path.parts[index:])

        pecha.set_metadata(
            PechaMetaData(
                id=pecha.id,
                parser="GoogleDocTranslationParser",
                **metadata,
                bases=bases,
                initial_creation_type=InitialCreationType.google_docx,
            )
        )

        return (pecha, relative_layer_path)
