import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Tuple, Union

from docx import Document

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import InitialCreationType, Language, PechaMetaData
from openpecha.pecha.parsers import BaseParser
from openpecha.pecha.parsers.parser_utils import extract_metadata_from_xlsx


class GoogleDocTranslationParser(BaseParser):
    def __init__(self, source_path: Union[str, None] = None):
        """
        source_path: Normaly, Tibetan file is the source i.e other lang files are translated based
                     on the tibetan file.
                     If tibetan lang file, set to None by default.
                     Else: source_path should be in this format=> pecha id / layer name.

        """
        self.root_idx_regex = r"^\d+\."
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

    def extract_root_idx(self, input: Path):
        extracted_text = self.extract_root_idx_from_doc(input)
        extracted_segments = list(extracted_text.values())
        extracted_segments = [segment for segment in extracted_segments if segment]

        self.base = "\n".join(extracted_segments)

        layer_enum = self.get_layer_enum_with_lang(self.metadata["language"])

        count = 0
        for root_idx, segment in extracted_text.items():
            curr_ann = {
                layer_enum.value: {
                    "start": count,
                    "end": count + len(segment),
                },
                "root_idx_mapping": root_idx,
            }
            self.anns.append(curr_ann)
            count += len(segment)

            if segment and count + 1 < len(self.base):
                count += 1

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
            self.metadata = extract_metadata_from_xlsx(metadata)

        else:
            self.metadata = metadata

        self.extract_root_idx(input)
        pecha, layer_path = self.create_pecha(output_path)
        return pecha, layer_path

    def update_alignment_in_source_pecha(self, target_pecha_layer: str):
        """
        Mapping should be updated on source pecha, when translation pecha is created.
        Such that 'translation_alignments' in the pecha metadata.
        Input: source_pecha_layer contains the path to source layer.

        Eg: "I3717024E/layers/345F/Tibetan_Segment-4C61.json"
                -I3717024E -> Pecha id,
                -345F -> Basename
                -Tibetan_Segment-4C61.json -> Layer Name
        """
        assert isinstance(self.source_path, str)
        source_pecha_layer = Path(self.source_path)
        pecha_id = source_pecha_layer.parts[0]

        pecha = Pecha.from_id(pecha_id=pecha_id)
        pecha_metadata = pecha.metadata

        new_translation_alignment = {
            "source": self.source_path,
            "target": target_pecha_layer,
        }

        if "translation_alignments" in pecha_metadata.source_metadata:
            pecha_metadata.source_metadata["translation_alignments"].append(
                new_translation_alignment
            )
        else:
            pecha_metadata.source_metadata["translation_alignments"] = [
                new_translation_alignment
            ]
        pecha.set_metadata(pecha_metadata=pecha_metadata)

        # Update remote pecha
        pecha.publish()

    def create_pecha(self, output_path: Path) -> Tuple[Pecha, Path]:
        pecha = Pecha.create(output_path)
        basename = pecha.set_base(self.base)

        layer_enum = self.get_layer_enum_with_lang(self.metadata["language"])

        # Add meaning_segment layer
        meaning_segment_layer, layer_path = pecha.add_layer(basename, layer_enum)
        for ann in self.anns:
            pecha.add_annotation(meaning_segment_layer, ann, layer_enum)
        meaning_segment_layer.save()

        # set base metadata
        bases = [
            {
                basename: {
                    "source_metadata": {"total_segments": len(self.anns)},
                    "base_file": f"{basename}.txt",
                }
            }
        ]

        # Get layer path relative to Pecha Path
        index = layer_path.parts.index(pecha.id)
        relative_layer_path = Path(*layer_path.parts[index:])

        if self.source_path:
            self.update_alignment_in_source_pecha(str(relative_layer_path))

        # Set source path in translation alignment
        if self.source_path:
            self.metadata["translation_alignments"] = [
                {"source": self.source_path, "target": str(relative_layer_path)}
            ]

        pecha.set_metadata(
            PechaMetaData(
                id=pecha.id,
                parser="GoogleDocTranslationParser",
                **self.metadata,
                bases=bases,
                initial_creation_type=InitialCreationType.google_docx,
            )
        )

        return (pecha, relative_layer_path)
