from pathlib import Path
from unittest import TestCase


class TestIgnoreFootNote(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.one_page_footnote = self.DATA_DIR / "one_page_footnote.docx"
        self.two_page_footnote = self.DATA_DIR / "two_page_footnote.docx"

    def test_ignore_footnote_one_page(self):
        pass

    def test_ignore_footnote_two_page(self):
        pass
