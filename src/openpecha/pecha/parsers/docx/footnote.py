import re
from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import FootnoteAnnotation
from openpecha.pecha.parsers.docx.utils import read_docx


class DocxFootnoteParser:
    def __init__(self):
        self.footnote_number = r"----footnote(\d+)----"
        self.footnote_content = r"footnote(\d+)\)[\t\s]+(.+)"

    def get_footnote_contents(self, text: str) -> Dict[int, str]:
        """
        Extract and remove footnote contents from text.
        """
        matches = re.findall(self.footnote_content, text)

        for match in matches:
            footnote_number = int(match[0])
            footnote_content = match[1]
            text = re.sub(self.footnote_content, "", text)
            footnote_contents[footnote_number] = footnote_content
        return footnote_contents

    def extract_footnote(self, text: str) -> List[FootnoteAnnotation]:
        matches = re.findall(self.footnote_number, text)
        for match in matches:
            # get footnote number
            footnote_number = match.group(1)
            # remove footnote annotation
            text = re.sub(self.footnote_pattern, "", text)
            # Store footnote number
        pass

    def parse(self, pecha: Pecha, input: str | Path):
        text = read_docx(input)
        anns = self.extract_footnote(text)
        pass
