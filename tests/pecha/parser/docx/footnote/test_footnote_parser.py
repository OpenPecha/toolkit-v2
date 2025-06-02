from pathlib import Path
from unittest import TestCase

from openpecha.pecha.parsers.docx.footnote import DocxFootnoteParser
from openpecha.pecha.parsers.docx.utils import read_docx


class TestFootnoteParser(TestCase):
    def setUp(self):
        self.FOOTNOTE_DIR = Path("tests/pecha/parser/docx/utils/data/footnote")
        self.ONE_PAGE_DIR = self.FOOTNOTE_DIR / "one_page"
        self.TWO_PAGE_DIR = self.FOOTNOTE_DIR / "two_page"
        self.one_page_footnote = self.ONE_PAGE_DIR / "one_page_footnote.docx"
        self.two_page_footnote = self.TWO_PAGE_DIR / "two_page_footnote.docx"

    def test_parse_one_page_footnote(self):
        parser = DocxFootnoteParser()
        text = read_docx(self.one_page_footnote)
        anns = parser.extract_footnote(text)

        pass  # TODO: add test case for one page footnote
