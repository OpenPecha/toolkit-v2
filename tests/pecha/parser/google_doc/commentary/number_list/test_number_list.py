from pathlib import Path
from unittest import TestCase

from openpecha.pecha.parsers.google_doc.commentary.number_list import (
    DocxNumberListCommentaryParser,
)
from openpecha.pecha.parsers.parser_utils import extract_metadata_from_xlsx


class TestNumberListCommentaryParser(TestCase):
    def setUp(self):
        self.data_dir = Path(__file__).parent / "data"
        self.input = self.data_dir / "དབུ་མ་_bo_commentary.docx"
        self.metadata = extract_metadata_from_xlsx(
            self.data_dir / "དབུ་མ་_bo_commentary_metadata.xlsx"
        )
        self.output_dir = self.data_dir / "output"

    def test_parse_numberlist_commentary_parser(self):
        parser = DocxNumberListCommentaryParser(
            root_path="opf_id/layers/basename/layer_file.json"
        )
        parser.parse(self.input, self.metadata, self.output_dir)

    def tearDown(self):
        pass


parser = TestNumberListCommentaryParser()
parser.setUp()
parser.test_parse_numberlist_commentary_parser()
parser.tearDown()
