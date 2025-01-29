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
        self.root_alignment_index_regex = r"^([\d\-,]+)\s(.*)"

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

    def extract_numbered_list(self, text: str) -> Dict[str, str]:
        """
        Extract number list from the extracted text from docx.

        Example Output:>
            {
                '1': 'དབུ་མ་དགོངས་པ་རབ་གསལ་ལེའུ་དྲུག་པ་བདེན་གཉིས་སོ་སོའི་ངོ་བོ་བཤད་པ།། ',
                '2': '2 གསུམ་པ་ལ་གཉིས། ཀུན་རྫོབ་ཀྱི་བདེན་པ་བཤད་པ་དང་། ',
                '3': '2,3 དེས་གང་ལ་སྒྲིབ་ན་ཡང་དག་ཀུན་རྫོབ་འདོད་ཅེས་པས་ཡང་དག་པའི་དོན་ལ་སྒྲིབ་པས་ཀུན་རྫོབ་བམ་སྒྲིབ་བྱེད་དུ་འདོད་ཅེས་པ་སྟེ། །',
                ...
            }
        """
        res: Dict[str, str] = {}
        for para_text in text.split("\n\n"):
            match = re.match(self.number_list_regex, para_text)
            if match:
                number = match.group(1)
                text = match.group(2)
                res[number] = text

        return res

    def extract_root_aligned_indices(self, docx_file: Path) -> Dict:

        text = docx2python(docx_file).text
        text = self.normalize_text(text)
        numbered_text: Dict[str, str] = self.extract_numbered_list(text)
        root_aligned_indices = {}
        for number, text in numbered_text.items():
            match = re.match(self.root_alignment_index_regex, text)
            if match:
                root_aligned_indices[match.group(1)] = match.group(2)
            else:
                root_aligned_indices[number] = text
        return root_aligned_indices

    def parse(
        self,
        input: Path,
        metadata: Dict[str, Any],
        output_path: Path = PECHAS_PATH,
    ):
        res = self.extract_root_aligned_indices(input)
        return res
