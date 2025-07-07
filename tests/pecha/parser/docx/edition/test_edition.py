from unittest import TestCase
from pathlib import Path

from tests.pecha import SharedPechaSetup
from openpecha.pecha import Pecha
from openpecha.pecha.parsers.docx.edition import DocxEditionParser

class TestDocxEditionParser(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()
        self.DATA = Path(__file__).parent / "data"
        self.docx_file = self.DATA / "edition.docx"

    def test_segmentation_parse(self):
        parser = DocxEditionParser()
        anns = parser.parse_segmentation(self.docx_file)
        print(anns)

    def test_spelling_variant_parse(self):
        parser = DocxEditionParser()
        anns = parser.parse_spelling_variant(self.pecha, self.docx_file)
        print(anns)

    def tearDown(self):
        pass 

