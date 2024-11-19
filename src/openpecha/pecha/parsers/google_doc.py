import re
from pathlib import Path
from typing import Dict, List, Optional, Union

from docx import Document
from docx.shared import RGBColor

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
        self.meaning_segment_anns: List[Dict] = []
        self.sapche_anns: List[Dict] = []
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
        self.meaning_segment_anns = []
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

        pecha = self.create_pecha(output_path)

        return pecha

    def parse_root(self, input: str):
        """
        Input: Normalized text
        Prcess: Parse and record the root annotations and cleaned base text in self.meaning_segment_anns, self.base
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

            self.meaning_segment_anns.append(curr_segment_ann)
            base_texts.append(segment)
            char_count += len(segment)
            char_count += 1  # for newline
        self.base = "\n".join(base_texts)

    def prepare_doc(self, input: Path):
        """
        Input: a docx file
        Process: Prepare the doc for parsing
        """
        # Parse meaning segments
        docs = Document(input)

        formatted_docs = []
        last_doc_data: List[
            Dict
        ] = []  # Store doc data (text and styles) for each paragraph
        for doc in docs.paragraphs:
            if doc.text == "":
                # Add the doc texts separated by two newline
                doc_texts = "\n".join([para["text"] for para in last_doc_data])
                doc_texts = doc_texts.strip()

                # Add the doc styles separated by two newline
                doc_styles = []
                for para in last_doc_data:
                    doc_styles.extend(para["styles"])

                # Strip the text and style
                formatted_doc_styles = []
                for idx, style in enumerate(doc_styles):
                    if idx == 0:
                        formatted_doc_styles.append(
                            {"text": style.text.lstrip(), "style": style.font}
                        )
                        continue
                    formatted_doc_styles.append(
                        {"text": style.text, "style": style.font}
                    )
                if formatted_doc_styles:
                    formatted_doc_styles[-1]["text"] = formatted_doc_styles[-1][
                        "text"
                    ].rstrip()

                formatted_docs.append(
                    {"text": doc_texts, "styles": formatted_doc_styles}
                )
                last_doc_data = []
                continue

            last_doc_data.append({"text": doc.text, "styles": doc.runs})

        if last_doc_data:
            doc_texts = "\n".join([para["text"] for para in last_doc_data])
            doc_texts = doc_texts.strip()
            doc_styles = []
            for para in last_doc_data:
                doc_styles.extend(para["styles"])
            formatted_doc_styles = []
            for idx, style in enumerate(doc_styles):
                if idx == 0:
                    formatted_doc_styles.append(
                        {"text": style.text.lstrip(), "style": style.font}
                    )
                    continue
                formatted_doc_styles.append({"text": style.text, "style": style.font})
            if formatted_doc_styles:
                formatted_doc_styles[-1]["text"] = formatted_doc_styles[-1][
                    "text"
                ].rstrip()
            formatted_docs.append({"text": doc_texts, "styles": formatted_doc_styles})

        return formatted_docs

    def add_commentary_meaning_ann(self, doc, char_count):
        segment = doc["text"]
        match = re.match(r"^([\d\-,]+) ", segment)
        segment_with_no_ann = segment
        if match:
            root_idx_mapping = match.group(1)
            segment = segment.replace(root_idx_mapping, "")
            segment_with_no_ann = segment.strip()
            curr_segment_ann = {
                LayerEnum.meaning_segment.value: {
                    "start": char_count,
                    "end": char_count + len(segment_with_no_ann),
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

        self.meaning_segment_anns.append(curr_segment_ann)
        return segment_with_no_ann

    def add_sapche_ann(self, doc, char_count):

        """
        Input: a docx file
        Process: Extract the sapche annotations (in Fusia/Pink color)
        """

        inner_char_count = 0
        for style in doc["styles"]:
            if style["style"].color.rgb == RGBColor(0xFF, 0x00, 0xFF):
                self.sapche_anns.append(
                    {
                        LayerEnum.sapche.value: {
                            "start": char_count + inner_char_count,
                            "end": char_count + inner_char_count + len(style["text"]),
                        }
                    }
                )
            inner_char_count += len(style["text"])

    def parse_commentary(self, input: Path):
        """
        Input: a docx file
        process: -Parse and record the commentary annotations in self.meaning_segment_anns,
                 -Save the cleaned base text in self.base

        """
        formatted_docs = self.prepare_doc(input)

        char_count = 0
        base_texts = []
        for doc in formatted_docs:
            segment = doc["text"]
            if not segment:
                continue

            self.add_sapche_ann(doc, char_count)
            segment_with_no_ann = self.add_commentary_meaning_ann(doc, char_count)

            base_texts.append(segment_with_no_ann)
            char_count += len(segment_with_no_ann)
            char_count += 2  # for two newline

        self.base = "\n\n".join(base_texts)

    def create_pecha(self, output_path: Path):

        pecha = Pecha.create(output_path)
        basename = pecha.set_base(self.base)
        meaning_segment_layer, _ = pecha.add_layer(basename, LayerEnum.meaning_segment)
        for ann in self.meaning_segment_anns:
            if ann["Meaning_Segment"]["end"] > len(self.base):
                ann["Meaning_Segment"]["end"] = len(self.base)
            pecha.add_annotation(meaning_segment_layer, ann, LayerEnum.meaning_segment)
        meaning_segment_layer.save()

        pecha.set_metadata(
            PechaMetaData(id=pecha.id, parser=self.name, **self.metadata)
        )

        return pecha
