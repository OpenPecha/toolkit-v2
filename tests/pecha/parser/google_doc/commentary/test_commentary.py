import tempfile
from pathlib import Path

from openpecha.pecha.parsers.google_doc.commentary import GoogleDocCommentaryParser
from openpecha.utils import read_json


def test_parser_on_commentary():
    data = Path(__file__).parent / "data"
    input = data / "commentary/རྡོ་རྗེ་གཅོད་པ་_commentary.docx"
    metadata = read_json(data / "commentary/metadata.json")

    parser = GoogleDocCommentaryParser(
        source_type="commentary", root_path="opf_id/layers/basename/layer_file.json"
    )
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        output_path.mkdir(parents=True, exist_ok=True)
        parser.parse(input, metadata, output_path)
        expected_sapche_anns = [
            {"Sapche": {"start": 102, "end": 124}, "sapche_number": "1."},
            {"Sapche": {"start": 126, "end": 166}, "sapche_number": "1.1."},
            {"Sapche": {"start": 252, "end": 283}, "sapche_number": "1.2."},
            {"Sapche": {"start": 541, "end": 558}, "sapche_number": "2."},
            {"Sapche": {"start": 560, "end": 560}, "sapche_number": "2.1."},
        ]

        assert parser.sapche_anns == expected_sapche_anns
