import tempfile
from pathlib import Path

from openpecha.pecha.parsers.docx.commentary.manual_number import (
    GoogleDocCommentaryParser,
)


def test_parser_on_bo_commentary():
    data = Path(__file__).parent / "data"
    input = data / "bo/Tibetan Commentary text test 2.docx"
    metadata = data / "bo/Tibetan Commentary text Metadata 2.xlsx"

    parser = GoogleDocCommentaryParser(
        root_path="opf_id/layers/basename/layer_file.json"
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        output_path.mkdir(parents=True, exist_ok=True)
        parser.parse(input, metadata, output_path)
        expected_sapche_anns = [
            {"Sapche": {"start": 102, "end": 124}, "sapche_number": "1."},
            {"Sapche": {"start": 126, "end": 166}, "sapche_number": "1.1."},
            {"Sapche": {"start": 2122, "end": 2153}, "sapche_number": "1.2."},
            {"Sapche": {"start": 2816, "end": 2856}, "sapche_number": "1.3."},
        ]

        assert parser.sapche_anns == expected_sapche_anns


def test_parser_on_en_commentary():
    data = Path(__file__).parent / "data"
    input = data / "en/English aligned Commentary Text 2.docx"
    metadata = data / "en/English Commentary text Metadata 2.xlsx"

    parser = GoogleDocCommentaryParser(
        root_path="opf_id/layers/basename/layer_file.json"
    )
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        output_path.mkdir(parents=True, exist_ok=True)
        parser.parse(input, metadata, output_path)
        expected_sapche_anns = [
            {"Sapche": {"start": 124, "end": 164}, "sapche_number": "1."},
            {"Sapche": {"start": 166, "end": 238}, "sapche_number": "1.1."},
        ]

        assert parser.sapche_anns == expected_sapche_anns


def test_parser_on_zh_commentary():
    data = Path(__file__).parent / "data"
    input = data / "zh/Chinese aligned Commentary Text 1.docx"
    metadata = data / "zh/Chinese Commentary text Metadata 1.xlsx"

    parser = GoogleDocCommentaryParser(
        root_path="opf_id/layers/basename/layer_file.json"
    )
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        output_path.mkdir(parents=True, exist_ok=True)
        parser.parse(input, metadata, output_path)
        expected_sapche_anns = [
            {"Sapche": {"start": 251, "end": 253}, "sapche_number": "1."},
            {"Sapche": {"start": 316, "end": 322}, "sapche_number": "2."},
            {"Sapche": {"start": 324, "end": 330}, "sapche_number": "2.1"},
            {"Sapche": {"start": 397, "end": 403}, "sapche_number": "2.1.1"},
            {"Sapche": {"start": 731, "end": 737}, "sapche_number": "3."},
        ]

        assert parser.sapche_anns == expected_sapche_anns
