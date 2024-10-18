import re
from pathlib import Path
from typing import Dict, List, Optional, Union

from docx import Document

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import PechaMetaData
from openpecha.pecha.parsers import BaseParser
from openpecha.utils import read_json


class GoogleDocParser(BaseParser):
    def __init__(self, source_type: str, root_path: Optional[str] = None):
        self.source_type = source_type
        self.root_path = root_path
        self.root_segment_splitter = "\n"
        self.commentary_segment_splitter = "\n\n"
        self.anns: List[Dict] = []
        self.base = ""
        self.metadata: Dict = {}

    def normalize_text(self, text: str):
        text = self.normalize_whitespaces(text)
        text = self.normalize_newlines(text)
        return text

    @staticmethod
    def normalize_whitespaces(text: str):
        """
        If there are spaces or tab between newlines, it will be removed.
        """
        return re.sub(r"\n[\s\t]+\n", "\n\n", text)

    @staticmethod
    def normalize_newlines(text: str):
        """
        If there are more than 2 newlines continously, it will replace it with 2 newlines.
        """
        return re.sub(r"\n{3,}", "\n\n", text)

    def parse(
        self,
        input: Path,
        metadata: Union[Dict, Path],
        output_path: Path = PECHAS_PATH,
    ) -> Pecha:

        # Clean up class attributes
        self.anns = []
        self.base = ""

        if isinstance(metadata, Path):
            metadata = read_json(metadata)
        if self.source_type == "commentary":
            assert self.source_type is not None
            assert isinstance(metadata, dict)
            metadata["root_path"] = self.root_path

        assert isinstance(metadata, dict)
        self.metadata = metadata

        if self.source_type == "root":
            input_text = input.read_text(encoding="utf-8")
            input_text = self.normalize_text(input_text)
            if input_text.startswith("\ufeff"):
                input_text = input_text[1:]

            self.parse_root(input_text)

        elif self.source_type == "commentary":
            self.parse_commentary(input)

        pecha = self.create_pecha(LayerEnum.meaning_segment, output_path)

        return pecha

    def parse_root(self, input: str):
        """
        Input: Normalized text
        Prcess: Parse and record the root annotations and cleaned base text in self.anns, self.base
        """
        char_count = 0
        base_texts = []
        for segment in input.split(self.root_segment_splitter):
            segment = segment.strip()

            match = re.search(r"^(\d+)\.", segment)
            if match:
                root_idx_num = match.group(1)
                segment = segment.replace(f"{root_idx_num}.", "")
                segment = segment.strip()

                curr_segment_ann = {
                    LayerEnum.meaning_segment.value: {
                        "start": char_count,
                        "end": char_count + len(segment),
                    },
                    "root_idx": int(root_idx_num),
                }

            else:
                curr_segment_ann = {
                    LayerEnum.meaning_segment.value: {
                        "start": char_count,
                        "end": char_count + len(segment),
                    }
                }

            self.anns.append(curr_segment_ann)
            base_texts.append(segment)
            char_count += len(segment)
            char_count += 1  # for newline
        self.base = "\n".join(base_texts)

    def parse_commentary(self, input: Path):
        """
        Input: a docx file
        process: -Parse and record the commentary annotations in self.anns,
                 -Save the cleaned base text in self.base

        """
        doc = Document(input)
        input_text = "\n".join([para.text for para in doc.paragraphs])

        input_text = self.normalize_text(input_text)
        if input_text.startswith("\ufeff"):
            input_text = input_text[1:]

        char_count = 0
        base_texts = []
        for segment in input_text.split(self.commentary_segment_splitter):
            segment = segment.strip()
            if not segment:
                continue

            match = re.match(r"^([\d\-,]+)", segment)
            if match:
                root_idx_mapping = match.group(1)
                segment = segment.replace(root_idx_mapping, "")
                segment = segment.strip()
                curr_segment_ann = {
                    LayerEnum.meaning_segment.value: {
                        "start": char_count,
                        "end": char_count + len(segment),
                    },
                    "root_idx_mapping": root_idx_mapping,
                }
            else:

                curr_segment_ann = {
                    LayerEnum.meaning_segment.value: {
                        "start": char_count,
                        "end": char_count + len(segment),
                    }
                }

            self.anns.append(curr_segment_ann)
            base_texts.append(segment)
            char_count += len(segment)
            char_count += 2  # for two newline

        self.base = "\n\n".join(base_texts)

    def create_pecha(self, layer_type: LayerEnum, output_path: Path):

        pecha = Pecha.create(output_path)
        basename = pecha.set_base(self.base)
        layer, _ = pecha.add_layer(basename, layer_type)
        for ann in self.anns:
            pecha.add_annotation(layer, ann, layer_type)

        pecha.set_metadata(
            PechaMetaData(id=pecha.id, parser=self.name, **self.metadata)
        )

        layer.save()

        return pecha
