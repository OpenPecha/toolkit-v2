from pathlib import Path

from openpecha.pecha.parsers.chonjuk.plaintext import ChonjukChapterParser


class TestChonjukPlainTextParser:
    def test_chonjuk_plaintext_parser(self):
        data = Path(__file__).parent / "data"
        chonjuk_text = (data / "chonjuk.txt").read_text(encoding="utf-8")
        chapter_parser = ChonjukChapterParser(text=chonjuk_text)

        expected_base_text = (data / "expected_base.txt").read_text(encoding="utf-8")
        assert chapter_parser.get_updated_text() == expected_base_text

        chapter_anns = chapter_parser.get_annotations()
        assert chapter_anns == [
            {
                "chapter_number": (145, 146),
                "chapter_title": (147, 177),
                "Chapter": (177, 478),
            },
            {
                "chapter_number": (481, 482),
                "chapter_title": (483, 497),
                "Chapter": (497, 944),
            },
        ]


TestChonjukPlainTextParser().test_chonjuk_plaintext_parser()
