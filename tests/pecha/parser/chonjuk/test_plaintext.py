from pathlib import Path

from openpecha.pecha.parsers.chonjuk.plaintext import ChonjukPlainTextParser


class TestChonjukPlainTextParser:
    def test_chonjuk_plaintext_parser(self):
        data = Path(__file__).parent / "data"
        chonjuk_text = (data / "chonjuk.txt").read_text(encoding="utf-8")
        parser = ChonjukPlainTextParser(chonjuk_text)

        output_path = Path(__file__).parent / "output"
        parser.parse(output_path)


TestChonjukPlainTextParser().test_chonjuk_plaintext_parser()
