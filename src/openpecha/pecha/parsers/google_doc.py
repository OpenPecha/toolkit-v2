import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

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
        self.meaning_segment_anns: List[Dict[str, Any]] = []
        self.sapche_anns: List[Dict[str, Any]] = []
        self.temp_state = {
            "meaning_segment": {"anns": [], "char_diff": 0},
            "sapche": {"anns": [], "char_diff": 0},
        }
        self.base = ""
        self.metadata: Dict[str, Any] = {}

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
        If there are more than 2 newlines continuously, it will replace it with 2 newlines.
        """
        return re.sub(r"\n{3,}", "\n\n", text)

    def parse(
        self,
        input: Path,
        metadata: Union[Dict[str, Any], Path],
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
        Process: Parse and record the root annotations and cleaned base text in self.meaning_segment_anns, self.base
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

        def format_paragraphs(paragraphs: List[Dict[str, Any]]) -> Dict[str, Any]:
            """
            Paragraphs is a text with styles.
            Each line in docx file is a paragraph.
            We have to combine the text and the styles
            """
            formatted_paras = []
            para_texts = []
            for para in paragraphs:
                para_texts.append(para["text"].strip())
                style_texts = []
                styles = []
                for para_style in para["styles"]:
                    para_text = para_style.text
                    style_texts.append(para_text)
                    styles.append(para_style.font)
                if style_texts:
                    style_texts[0] = style_texts[0].lstrip()
                    style_texts[-1] = style_texts[-1].rstrip()
                formatted_paras.append({"texts": style_texts, "styles": styles})
            res = {"text": "\n".join(para_texts), "styles": formatted_paras}
            return res

        # Parse the document
        docs = Document(input)

        formatted_docs = []
        last_doc_data: List[Dict[str, Any]] = []

        for doc in docs.paragraphs:
            if doc.text.strip() == "":
                if last_doc_data:
                    formatted_docs.append(format_paragraphs(last_doc_data))
                    last_doc_data = []
            else:
                last_doc_data.append({"text": doc.text, "styles": doc.runs})

        # Handle remaining paragraphs after the loop
        if last_doc_data:
            formatted_docs.append(format_paragraphs(last_doc_data))

        return formatted_docs

    def add_commentary_meaning_ann(self, doc: Dict[str, Any], char_count: int) -> str:
        segment = doc["text"]
        match = re.match(r"^([\d\-,]+) ", segment)
        updated_segment = segment
        if match:
            root_idx_mapping = match.group(1)
            segment = segment.replace(root_idx_mapping, "")
            updated_segment = segment.strip()
            curr_segment_ann = {
                LayerEnum.meaning_segment.value: {
                    "start": char_count,
                    "end": char_count + len(updated_segment),
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

        # self.meaning_segment_anns.append(curr_segment_ann)
        self.temp_state["meaning_segment"]["anns"].append(curr_segment_ann)  # type: ignore
        return updated_segment

    def add_sapche_ann(self, doc: Dict[str, Any], char_count: int):
        """
        Input: a docx file
        Process: Extract the sapche annotations (in Fuchsia/Pink color)
        """
        inner_char_count = 0
        sapche_anns: List[Dict[str, Any]] = []
        for doc_style in doc["styles"]:
            for idx in range(len(doc_style["texts"])):
                if doc_style["styles"][idx].color.rgb == RGBColor(0xFF, 0x00, 0xFF):
                    match = re.match(r"([\d\.]+)\s", doc_style["texts"][idx])
                    if match:
                        # Extract sapche number and store the char length to update the previous ann spans
                        sapche_number = match.group(1)
                        doc_style["texts"][idx] = doc_style["texts"][idx].replace(
                            sapche_number, ""
                        )
                        self.temp_state["sapche"]["char_diff"] += len(sapche_number)  # type: ignore

                        start = char_count + inner_char_count + len(sapche_number) + 1
                        end = start + len(doc_style["texts"][idx])
                        sapche_anns.append(
                            {
                                LayerEnum.sapche.value: {
                                    "start": start,
                                    "end": end,
                                    "sapche_number": sapche_number,
                                }
                            }
                        )
                    else:
                        start = char_count + inner_char_count
                        end = start + len(doc_style["texts"][idx])
                        sapche_anns.append(
                            {
                                LayerEnum.sapche.value: {
                                    "start": start,
                                    "end": end,
                                }
                            }
                        )
                inner_char_count += len(doc_style["texts"][idx])

        formatted_anns: List[Dict[str, Any]] = []
        last_ann: Optional[Dict[str, Any]] = None
        for sapche_ann in sapche_anns:
            if last_ann is None:
                last_ann = sapche_ann
                continue
            if (
                sapche_ann[LayerEnum.sapche.value]["start"]
                != last_ann[LayerEnum.sapche.value]["end"]
            ):
                formatted_anns.append(last_ann)
                last_ann = sapche_ann
            else:
                last_ann[LayerEnum.sapche.value]["end"] = sapche_ann[
                    LayerEnum.sapche.value
                ]["end"]

        if last_ann:
            formatted_anns.append(last_ann)
        # self.sapche_anns.extend(formatted_anns)
        self.temp_state["sapche"]["anns"].extend(formatted_anns)  # type: ignore
        updated_segment = "\n".join(
            ["".join(doc_style["texts"]) for doc_style in doc["styles"]]
        )
        return updated_segment

    def parse_commentary(self, input: Path):
        """
        Input: a docx file
        Process: - Parse and record the commentary annotations in self.meaning_segment_anns,
                 - Save the cleaned base text in self.base
        """
        formatted_docs = self.prepare_doc(input)

        char_count = 0
        base_texts = []
        for doc in formatted_docs:
            segment = doc["text"]
            if not segment:
                continue

            updated_segment = self.add_commentary_meaning_ann(doc, char_count)
            updated_segment = self.add_sapche_ann(doc, char_count)

            # Updating the ann spans
            if self.temp_state["meaning_segment"]["anns"]:
                meaning_segment_ann = self.temp_state["meaning_segment"]["anns"][0]  # type: ignore
                meaning_segment_ann[LayerEnum.meaning_segment.value][
                    "end"
                ] -= self.temp_state["sapche"]["char_diff"]
                self.meaning_segment_anns.append(meaning_segment_ann)

            self.temp_state = {
                "meaning_segment": {"anns": [], "char_diff": 0},
                "sapche": {"anns": [], "char_diff": 0},
            }

            base_texts.append(updated_segment)
            char_count += len(updated_segment)
            char_count += 2  # for two newlines

        self.base = "\n\n".join(base_texts)

    def create_pecha(self, output_path: Path) -> Pecha:
        pecha = Pecha.create(output_path)
        basename = pecha.set_base(self.base)
        meaning_segment_layer, _ = pecha.add_layer(basename, LayerEnum.meaning_segment)
        for ann in self.meaning_segment_anns:
            pecha.add_annotation(meaning_segment_layer, ann, LayerEnum.meaning_segment)
        meaning_segment_layer.save()

        pecha.set_metadata(
            PechaMetaData(id=pecha.id, parser=self.name, **self.metadata)
        )

        return pecha
