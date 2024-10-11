import json
import tempfile
from pathlib import Path

from openpecha.pecha.parsers.chonjuk.plaintext import ChonjukChapterParser


class TestChonjukPlainTextParser:
    def test_chonjuk_plaintext_parser(self):
        data = Path(__file__).parent / "data"
        chonjuk_text = (data / "chonjuk.txt").read_text(encoding="utf-8")
        with open(data / "chonjuk_metadata.json") as f:
            chonjuk_metadata = json.load(f)

        parser = ChonjukChapterParser()

        expected_base_text = (data / "expected_base.txt").read_text(encoding="utf-8")

        expected_chapter_anns = [
            {
                "chapter_number": "1",
                "chapter_title": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
                "Chapter": {"start": 145, "end": 446},
            },
            {
                "chapter_number": "2",
                "chapter_title": "སྡིག་པ་བཤགས་པ།",
                "Chapter": {"start": 449, "end": 896},
            },
        ]

        output_path = Path(__file__).parent / "output"
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_path = Path(tmpdirname)
            parser.parse(
                chonjuk_text, output_path=output_path, metadata=chonjuk_metadata
            )
            assert parser.cleaned_text == expected_base_text
            assert parser.annotations == expected_chapter_anns


TestChonjukPlainTextParser().test_chonjuk_plaintext_parser()
