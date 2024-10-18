import tempfile
from pathlib import Path

from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.google_doc import GoogleDocParser
from openpecha.utils import read_json


def test_root_google_doc_parser():
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

        for ann, seg in zip(parser.anns, expected_segments):
            start, end = (
                ann[LayerEnum.meaning_segment.value]["start"],
                ann[LayerEnum.meaning_segment.value]["end"],
            )
            assert parser.base[start:end] == seg


def test_commentary_google_doc_parser():
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

        expected_anns = [
            {"Meaning_Segment": {"start": 0, "end": 68}},
            {"Meaning_Segment": {"start": 70, "end": 232}},
            {"Meaning_Segment": {"start": 234, "end": 297}, "root_idx_mapping": "1"},
            {"Meaning_Segment": {"start": 299, "end": 557}, "root_idx_mapping": "2-3"},
            {"Meaning_Segment": {"start": 559, "end": 945}, "root_idx_mapping": "2"},
            {"Meaning_Segment": {"start": 947, "end": 1105}, "root_idx_mapping": "5,7"},
            {
                "Meaning_Segment": {"start": 1107, "end": 1265},
                "root_idx_mapping": "1-5,9",
            },
        ]

        assert parser.anns == expected_anns

        expected_segments = [
            "སྒྲོལ་མ་ཉེར་གཅིག་པའི་བསྟོད་འགྲེལ་འཕྲིན་ལས་ཆར་དུ་སྙིལ་བའི་སྤྲིན་ཕུང་།",
            "དང་པོ་ནི། རྒྱ་གར་སྐད་དུ། ན་མཿ ཏཱརཱ་ཨེ་ཀ་བིཾ་ཤ་ཏི་སྟོ་ཏྲ་གུ་ཎ་ཧི་ཏ་སཱ་ཀ །བོད་སྐད་དུ། སྒྲོལ་མ་ལ་ཕྱག་འཚལ་ཉི་ཤུ་རྩ་གཅིག་གིས་བསྟོད་པ་ཕན་ཡོན་དང་བཅས་པ། ཞེས་པའི་དོན་ཏོ། །",
            "གཉིས་པ་ནི། རྗེ་བཙུན་མ་འཕགས་མ་སྒྲོལ་མ་ལ་ཕྱག་འཚལ་ལོ། ། ཞེས་གསུངས།",
            "གསུམ་པ་ལ་ཕྱག་འཚལ་ཉེར་གཅིག་ཡོད་པ་ལས། ཕྱག་འཚལ་དང་པོ་རྗེ་བཙུན་མ་འཕགས་མ་སྒྲོལ་མ་ལ་ཕྱག་འཚལ་བ་ནི།\nརྒྱུད་ལས།།\nཕྱག་འཚལ་སྒྲོལ་མ་མྱུར་མ་དཔའ་མོ། །\nསྤྱན་ནི་སྐད་གཅིག་གློག་དང་འདྲ་མ། །\nའཇིག་རྟེན་གསུམ་མགོན་ཆུ་སྐྱེས་ཞལ་གྱི། །\nགེ་སར་བྱེ་བ་ལས་ནི་བྱུང་མ། །\nཞེས་གསུངས་པའི་དོན་ནི།",
            "ཕྱག་འཚལ་ལོ་རྗེ་བཙུན་མ་འཕགས་མ་སྒྲོལ་མ་ལའོ། །རྒྱུ་གང་གི་སྒོ་ནས་ཕྱག་འཚལ་ཞེ་ན། སྒྲོལ་མྱུར་དཔའ་གསུམ་གྱི་ཆེ་བའི་སྒོ་ནས་ཏེ། དང་པོ་སྒྲོལ་མ་ཞེས་པའི་མཚན་གྱི་ཆེ་བ་ནི། ལྷ་མོ་འདིས་སེམས་ཅན་དཔག་ཏུ་མེད་པ་གནས་སྐབས་འཇིགས་པ་བརྒྱད་སོགས་དང་། མཐར་ཉོན་མོངས་པ་དང་ཤེས་བྱའི་སྒྲིབ་པ་ལས་བསྒྲལ་ཏེ་བླ་མེད་རྫོགས་པའི་སངས་རྒྱས་ཀྱི་སར་བཀོད་པས་ན། བསྐལ་པ་དཔག་ཏུ་མེད་པའི་སྔོན་རོལ་ནས་སྒྲོལ་མ་ཞེས་པའི་མཚན་གྱིས་བསྔགས་པ་ཡིན་ཏེ།",
            "སྐབས་འདིའི་འོད་ཟེར་ནི། འགྲེལ་པ་འགའ་ཞིག་ལས། ཕྱག་གཡས་པའི་མཐིལ་གྱི་འཁོར་ལོའི་འོད་ཟེར་ཡིན་པར་གསུངས་པ་དང་། གཞན་དག་སྐུའི་འོད་ཟེར་ཡིན་པར་གསུངས་པ་ས་བཞེད་པ་མི་འདྲ་ཡང་།",
            "སྐབས་འདིའི་འོད་ཟེར་ནི། འགྲེལ་པ་འགའ་ཞིག་ལས། ཕྱག་གཡས་པའི་མཐིལ་གྱི་འཁོར་ལོའི་འོད་ཟེར་ཡིན་པར་གསུངས་པ་དང་། གཞན་དག་སྐུའི་འོད་ཟེར་ཡིན་པར་གསུངས་པ་ས་བཞེད་པ་མི་འདྲ་ཡང་།",
        ]

        for ann, expected_segment in zip(parser.anns, expected_segments):
            start, end = (
                ann[LayerEnum.meaning_segment.value]["start"],
                ann[LayerEnum.meaning_segment.value]["end"],
            )
            assert parser.base[start:end] == expected_segment
