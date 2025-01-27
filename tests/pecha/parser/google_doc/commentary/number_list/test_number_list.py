from pathlib import Path
from unittest import TestCase


class TestNumberListCommentaryParser(TestCase):
    def setUp(self):
        self.data_dir = Path(__file__).parent / "data"
        self.bo_docx_file = self.data_dir / "དབུ་མ་_bo_commentary.docx"
        self.bo_metadata_file = self.data_dir / "དབུ་མ་_bo_commentary_metadata.xlsx"

    def test_parse_numberlist_commentary_parser(self):
        pass

    def tearDown(self):
        pass
