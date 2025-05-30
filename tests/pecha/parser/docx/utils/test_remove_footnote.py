from pathlib import Path
from unittest import TestCase

from openpecha.pecha.parsers.docx.utils import read_docx, remove_footnote


class TestRemoveFootNote(TestCase):
    def setUp(self):
        self.FOOTNOTE_DIR = Path(__file__).parent / "data" / "footnote"
        self.ONE_PAGE_DIR = self.FOOTNOTE_DIR / "one_page"
        self.TWO_PAGE_DIR = self.FOOTNOTE_DIR / "two_page"
        self.one_page_footnote = self.ONE_PAGE_DIR / "one_page_footnote.docx"
        self.two_page_footnote = self.TWO_PAGE_DIR / "two_page_footnote.docx"

    def test_remove_footnote_one_page(self):
        text = read_docx(self.one_page_footnote, False)
        expected_before = self.ONE_PAGE_DIR / "before_one_page.txt"
        assert text == expected_before.read_text(encoding="utf-8").strip()

        text = remove_footnote(text)
        expected_after = self.ONE_PAGE_DIR / "after_one_page.txt"
        assert text == expected_after.read_text(encoding="utf-8").strip()

    def test_remove_footnote_two_page(self):
        text = read_docx(self.two_page_footnote, False)
        expected_before = self.TWO_PAGE_DIR / "before_two_page.txt"
        assert text == expected_before.read_text(encoding="utf-8").strip()

        text = remove_footnote(text)
        expected_after = self.TWO_PAGE_DIR / "after_two_page.txt"
        assert text == expected_after.read_text(encoding="utf-8").strip()
