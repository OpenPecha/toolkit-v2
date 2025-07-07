from unittest import TestCase
from pathlib import Path

from tests.pecha import SharedPechaSetup

class TestDocxEditionParser(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()
        self.DATA = Path(__file__).parent / "data"
        self.docx_file = self.DATA / "edition.docx"

    def test_segmentation_parse(self):
        pass

    def test_spelling_variant_parse(self):
        pass 

    def tearDown(self):
        pass 