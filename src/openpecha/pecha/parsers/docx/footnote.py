import re
from pathlib import Path
from typing import Dict, Tuple

from openpecha.pecha import Pecha
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
        matches = re.findall(self.footnote_number, text)
        footnote_spans: Dict[int, Tuple[int, int]] = {}

        for match in matches:
            footnote_number = int(match[0])
            text = re.sub(self.footnote_number, "", text)
            if footnote_number in footnote_contents:
                footnote_spans[footnote_number] = (match.start(), match.end())
        return (text, footnote_spans)

    def parse(self, pecha: Pecha, input: str | Path):
        text = read_docx(input)
        text, footnote_contents = self.get_footnote_contents(text)  # noqa
