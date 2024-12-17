from pathlib import Path

from openpecha.pecha.parsers.google_doc.commentary import GoogleDocCommentaryParser


def test_parser_on_bo_commentary():
    data = Path(__file__).parent / "data"
    input = data / "bo/Tibetan Commentary text test 2.docx"
    metadata = data / "bo/Tibetan Commentary text Metadata 2.xlsx"

    parser = GoogleDocCommentaryParser(
        source_type="commentary", root_path="opf_id/layers/basename/layer_file.json"
    )
    output_path = data / "output"
    output_path.mkdir(parents=True, exist_ok=True)
    parser.parse(input, metadata, output_path)
    expected_sapche_anns = [
        {"Sapche": {"start": 102, "end": 124}, "sapche_number": "1."},
        {"Sapche": {"start": 126, "end": 166}, "sapche_number": "1.1."},
        {"Sapche": {"start": 2122, "end": 2153}, "sapche_number": "1.2."},
        {"Sapche": {"start": 2816, "end": 2856}, "sapche_number": "1.3."},
    ]

    assert parser.sapche_anns == expected_sapche_anns


test_parser_on_bo_commentary()
