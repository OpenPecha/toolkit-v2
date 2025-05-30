import tempfile
from pathlib import Path
from unittest import TestCase

from openpecha.pecha.annotations import SapcheAnnotation, Span
from openpecha.pecha.parsers.docx.commentary.complex import DocxComplexCommentaryParser
from openpecha.pecha.parsers.parser_utils import extract_metadata_from_xlsx


class TestDocxComplexCommentaryParser(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"

    def test_parser_on_bo_commentary(self):
        input = self.DATA_DIR / "bo/Tibetan Commentary text test 2.docx"

        metadata_file_path = (
            self.DATA_DIR / "bo/Tibetan Commentary text Metadata 2.xlsx"
        )
        metadata = extract_metadata_from_xlsx(metadata_file_path)

        parser = DocxComplexCommentaryParser(
            root_path="opf_id/layers/basename/layer_file.json"
        )

        with tempfile.TemporaryDirectory() as tmpdirname:
            output_path = Path(tmpdirname)
            output_path.mkdir(parents=True, exist_ok=True)
            parser.parse(input, metadata, output_path)
            expected_sapche_anns = [
                SapcheAnnotation(span=Span(start=102, end=124), sapche_number="1."),
                SapcheAnnotation(span=Span(start=126, end=166), sapche_number="1.1."),
                SapcheAnnotation(span=Span(start=2122, end=2153), sapche_number="1.2."),
                SapcheAnnotation(span=Span(start=2816, end=2856), sapche_number="1.3."),
            ]

            assert parser.sapche_anns == expected_sapche_anns

    def test_parser_on_en_commentary(self):
        input = self.DATA_DIR / "en/English aligned Commentary Text 2.docx"

        metadata_file_path = (
            self.DATA_DIR / "en/English Commentary text Metadata 2.xlsx"
        )
        metadata = extract_metadata_from_xlsx(metadata_file_path)

        parser = DocxComplexCommentaryParser(
            root_path="opf_id/layers/basename/layer_file.json"
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_path = Path(tmpdirname)
            output_path.mkdir(parents=True, exist_ok=True)
            parser.parse(input, metadata, output_path)
            expected_sapche_anns = [
                SapcheAnnotation(span=Span(start=124, end=164), sapche_number="1."),
                SapcheAnnotation(span=Span(start=166, end=238), sapche_number="1.1."),
            ]

            assert parser.sapche_anns == expected_sapche_anns

    def test_parser_on_zh_commentary(self):
        input = self.DATA_DIR / "zh/Chinese aligned Commentary Text 1.docx"

        metadata_file_path = (
            self.DATA_DIR / "zh/Chinese Commentary text Metadata 1.xlsx"
        )
        metadata = extract_metadata_from_xlsx(metadata_file_path)

        parser = DocxComplexCommentaryParser(
            root_path="opf_id/layers/basename/layer_file.json"
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_path = Path(tmpdirname)
            output_path.mkdir(parents=True, exist_ok=True)
            parser.parse(input, metadata, output_path)

            expected_sapche_anns = [
                SapcheAnnotation(span=Span(start=251, end=253), sapche_number="1."),
                SapcheAnnotation(span=Span(start=316, end=322), sapche_number="2."),
                SapcheAnnotation(span=Span(start=324, end=330), sapche_number="2.1"),
                SapcheAnnotation(span=Span(start=397, end=403), sapche_number="2.1.1"),
                SapcheAnnotation(span=Span(start=731, end=737), sapche_number="3."),
            ]

            assert parser.sapche_anns == expected_sapche_anns
