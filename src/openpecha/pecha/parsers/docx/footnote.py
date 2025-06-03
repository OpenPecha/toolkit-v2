import re
from pathlib import Path
from typing import Dict, List, Tuple

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import BaseAnnotation, FootnoteAnnotation, Span
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers.docx.utils import read_docx


class DocxFootnoteParser:
    def __init__(self):
        self.footnote_number = r"----footnote(\d+)----"
        self.footnote_content = r"footnote(\d+)\)[\t\s]+(.+)"

    def get_footnote_contents(self, text: str) -> Tuple[str, Dict[int, str]]:
        """
        Extract and remove footnote contents from text.
        """
        matches = re.findall(self.footnote_content, text)
        footnote_contents: Dict[int, str] = {}

        for match in matches:
            footnote_number = int(match[0])
            footnote_content = match[1]
            footnote_contents[footnote_number] = footnote_content

        text = re.sub(self.footnote_content, "", text)
        return (text, footnote_contents)

    def get_footnote_spans(
        self, text: str, footnote_contents: Dict[int, str]
    ) -> Tuple[str, Dict[int, Tuple[int, int]]]:
        matches = re.finditer(self.footnote_number, text)
        footnote_spans: Dict[int, Tuple[int, int]] = {}

        diff = 0

        for match in matches:
            footnote_number = int(match.group(1))
            if footnote_number in footnote_contents:
                footnote_spans[footnote_number] = (
                    match.start() - diff,
                    match.start() - diff,
                )

            diff += match.end() - match.start()

        text = re.sub(self.footnote_number, "", text)
        return (text, footnote_spans)

    def add_footnote_layer(
        self, pecha: Pecha, anns: List[BaseAnnotation], ann_type: AnnotationType
    ):

        basename = list(pecha.bases.keys())[0]
        layer, layer_path = pecha.add_layer(basename, ann_type)
        for ann in anns:
            pecha.add_annotation(layer, ann, ann_type)
        layer.save()

        return str(layer_path.relative_to(pecha.layer_path))

    def parse(self, pecha: Pecha, input: str | Path) -> str:
        text = read_docx(input)
        text, footnote_contents = self.get_footnote_contents(text)
        text, footnote_spans = self.get_footnote_spans(text, footnote_contents)

        anns = []
        for footnote_number, span in footnote_spans.items():
            anns.append(
                FootnoteAnnotation(
                    span=Span(start=span[0], end=span[1]),
                    note=footnote_contents[footnote_number],
                )
            )

        annotation_path: str = self.add_footnote_layer(
            pecha, anns, AnnotationType.FOOTNOTE
        )
        return annotation_path
