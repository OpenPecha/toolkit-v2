import tempfile
from pathlib import Path

from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.google_doc.commentary import GoogleDocCommentaryParser
from openpecha.utils import read_json


def test_parser_on_root_text():
    data = Path(__file__).parent / "data"
    input = data / "root/dolma_21.txt"
    metadata = read_json(data / "root/metadata.json")

    parser = GoogleDocCommentaryParser(source_type="root")
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
