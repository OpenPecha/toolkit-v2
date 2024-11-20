import tempfile
from pathlib import Path

from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.google_doc import GoogleDocParser
from openpecha.utils import read_json


def test_parser_on_root_text():
    data = Path(__file__).parent / "data"
    input = data / "root/dolma_21.txt"
    metadata = read_json(data / "root/metadata.json")

    parser = GoogleDocParser(source_type="root")
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)

        parser.parse(input, metadata, output_path)

        expected_base = (data / "root/expected_base.txt").read_text(encoding="utf-8")
        assert parser.base == expected_base

        expected_segments = [
            "༄༅། །ཨོཾ་རྗེ་བཙུན་མ་འཕགས་མ་སྒྲོལ་མ་ལ་ཕྱག་འཚལ་ལོ། །",
            "ཕྱག་འཚལ་སྒྲོལ་མ་མྱུར་མ་དཔའ་མོ། །སྤྱན་ནི་སྐད་ཅིག་གློག་དང་འདྲ་མ། །",
            "འཇིག་རྟེན་གསུམ་མགོན་ཆུ་སྐྱེས་ཞལ་གྱི། །གེ་སར་བྱེ་བ་ལས་ནི་བྱུང་མ། །",
            "ཕྱག་འཚལ་སྟོན་ཀའི་ཟླ་བ་ཀུན་ཏུ། །གང་བ་བརྒྱ་ནི་བརྩེགས་པའི་ཞལ་མ། །",
        ]

        for ann, seg in zip(parser.meaning_segment_anns, expected_segments):
            start, end = (
                ann[LayerEnum.meaning_segment.value]["start"],
                ann[LayerEnum.meaning_segment.value]["end"],
            )
            assert parser.base[start:end] == seg


def test_parser_on_commentary_text():
    data = Path(__file__).parent / "data"
    input = data / "commentary/dolma_21.docx"
    metadata = read_json(data / "commentary/metadata.json")

    parser = GoogleDocParser(
        source_type="commentary", root_path="opf_id/layers/basename/layer_file.json"
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)

        parser.parse(input, metadata, output_path)

        expected_base = (data / "commentary/expected_base.txt").read_text(
            encoding="utf-8"
        )
        assert parser.base == expected_base


test_parser_on_commentary_text()


def test_parser_on_commentary_with_sapche():
    data = Path(__file__).parent / "data"
    input = data / "commentary_with_sapche/རྡོ་རྗེ་གཅོད་པ་commentary.docx"
    metadata = read_json(data / "commentary_with_sapche/metadata.json")

    parser = GoogleDocParser(
        source_type="commentary", root_path="opf_id/layers/basename/layer_file.json"
    )
    output_path = Path(__file__).parent / "output"
    output_path.mkdir(parents=True, exist_ok=True)
    parser.parse(input, metadata, output_path)
    expected_sapche_anns = [
        {"Sapche": {"start": 101, "end": 123}},
        {"Sapche": {"start": 124, "end": 166, "sapche_number": "1.1."}},
        {"Sapche": {"start": 253, "end": 270}},
        {"Sapche": {"start": 271, "end": 312, "sapche_number": "2.1."}},
        {"Sapche": {"start": 477, "end": 555}},
    ]

    assert parser.sapche_anns == expected_sapche_anns
