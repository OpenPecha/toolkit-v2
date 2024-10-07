from pathlib import Path
from shutil import rmtree

from openpecha.pecha.parsers.chonjuk.plaintext import ChonjukChapterParser


class TestChonjukPlainTextParser:
    def test_chonjuk_plaintext_parser(self):
        data = Path(__file__).parent / "data"
        chonjuk_text = (data / "chonjuk.txt").read_text(encoding="utf-8")
        parser = ChonjukChapterParser()

        expected_base_text = (data / "expected_base.txt").read_text(encoding="utf-8")

        expected_chapter_anns = [
            {
                "chapter_number": "1",
                "chapter_title": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
                "Chapter": (149, 450),
            },
            {
                "chapter_number": "2",
                "chapter_title": "སྡིག་པ་བཤགས་པ།",
                "Chapter": (457, 904),
            },
        ]

        output_path = data / "output"
        parser.parse(chonjuk_text, output_path=output_path)
        assert parser.cleaned_text == expected_base_text
        assert parser.annotations == expected_chapter_anns

        rmtree(output_path)


TestChonjukPlainTextParser().test_chonjuk_plaintext_parser()
