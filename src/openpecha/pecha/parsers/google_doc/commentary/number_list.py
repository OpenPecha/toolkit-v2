import re
from pathlib import Path
from typing import Any, Dict, Optional

from docx2python import docx2python

from openpecha.config import PECHAS_PATH
from openpecha.pecha.parsers import BaseParser


class DocxNumberListCommentaryParser(BaseParser):
    def __init__(self, root_path: Optional[str] = None):
        self.root_path = root_path
        self.number_list_regex = r"^(\d+)\)\t(.*)"

    def normalize_text(self, text: str):
        text = self.normalize_whitespaces(text)
        text = self.normalize_newlines(text)
        text = text.strip()
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

    def get_number_list(self, text: str) -> Dict:
        """
        Extract number list from the extracted text from docx.
        """
        res: Dict[str, str] = {}
        for para_text in text.split("\n\n"):
            match = re.match(self.number_list_regex, para_text)
            if match:
                number = match.group(1)
                text = match.group(2)
                res[number] = text

        return res

    def parse(
        self,
        input: Path,
        metadata: Dict[str, Any],
        output_path: Path = PECHAS_PATH,
    ):
        text = docx2python(input).text
        text = self.normalize_text(text)
        res = self.get_number_list(text)
        return res
