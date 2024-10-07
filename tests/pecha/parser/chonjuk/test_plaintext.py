from pathlib import Path

from openpecha.pecha.parsers.chonjuk.plaintext import ChonjukChapterParser


class TestChonjukPlainTextParser:
    def test_chonjuk_plaintext_parser(self):
        data = Path(__file__).parent / "data"
        chonjuk_text = (data / "chonjuk.txt").read_text(encoding="utf-8")
        chapter_parser = ChonjukChapterParser(text=chonjuk_text)

        expected_base_text = (data / "expected_base.txt").read_text(encoding="utf-8")

        expected_chapter_anns = [
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

        chapter_parser.parse()
        assert chapter_parser.cleaned_text == expected_base_text
        assert chapter_parser.annotations == expected_chapter_anns


TestChonjukPlainTextParser().test_chonjuk_plaintext_parser()
