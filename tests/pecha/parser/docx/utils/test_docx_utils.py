from pathlib import Path
from unittest import TestCase

from openpecha.pecha.parsers.docx.utils import extract_text_from_docx, remove_footnote


class TestRemoveFootNote(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.one_page_footnote = self.DATA_DIR / "one_page_footnote.docx"
        self.two_page_footnote = self.DATA_DIR / "two_page_footnote.docx"

    def test_remove_footnote_one_page(self):
        text = extract_text_from_docx(self.one_page_footnote)
        expected_before = self.DATA_DIR / "before_one_page.txt"
        assert text == expected_before.read_text(encoding="utf-8").strip()

        text = remove_footnote(text)
        expected_after = self.DATA_DIR / "after_one_page.txt"
        assert text == expected_after.read_text(encoding="utf-8").strip()

    def test_remove_footnote_two_page(self):
        text = extract_text_from_docx(self.two_page_footnote)
        expected_before = self.DATA_DIR / "before_two_page.txt"
        assert text == expected_before.read_text(encoding="utf-8").strip()

        text = remove_footnote(text)
        expected_after = self.DATA_DIR / "after_two_page.txt"
        assert text == expected_after.read_text(encoding="utf-8").strip()
