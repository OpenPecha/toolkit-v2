import json
from pathlib import Path

from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.durchen import DurchenParser


def test_durchen():
    data = Path(__file__).parent / "data"
    pedurmafile = data / "pedurma_hfml.txt"
    pedurma_text = pedurmafile.read_text(encoding="utf-8")

    metadata_file = data / "metadata.json"
    with open(metadata_file) as f:
        metadata = json.load(f)

    parser = DurchenParser()

    output_path = Path(__file__).parent / "output"
    parser.parse(pedurma_text, metadata=metadata, output_path=output_path)

    expected_base = (data / "expected_base.txt").read_text(encoding="utf-8")
    assert parser.base_text == expected_base

    # Checking extracted durchen annotations
    expected_span_texts = ["༄༅། །", "འཕགས་པ་འཇམ་", "འདུད།", "རྣམ་"]
    for ann, expected_span in zip(parser.durchen_anns, expected_span_texts):
        start, end = (
            ann[LayerEnum.durchen.value]["start"],
            ann[LayerEnum.durchen.value]["end"],
        )
        assert parser.base_text[start:end] == expected_span

    expected_ann_notes = [
        "(1) <«ཅོ་»«སྡེ་»«སྣར་»«པེ་»༄༅། །ཆོས་ཀྱི་དབྱིངས་སུ་བསྟོད་པ། ༄༅༅། །>",
        "(3) <«སྣར་»«པེ་»འཇམ་>",
        "(4) <«སྣར་»«པེ་»ལོ།>",
        "(5) <«སྣར་»«པེ་»རྣམས་>",
    ]

    for ann, expected_note in zip(parser.durchen_anns, expected_ann_notes):
        assert ann["note"] == expected_note

    # Checking extracted meaning segment annotations
    expected_meaning_segments = [
        "༄༅། །",
        "རྒྱ་གར་སྐད་དུ། དྷརྨ་དྷཱ་ཏུ་སྟ་བཾ། བོད་སྐད་དུ། ཆོས་ཀྱི་དབྱིངས་སུ་བསྟོད་པ། འཕགས་པ་འཇམ་དཔལ་གཞོན་ནུར་གྱུར་པ་ལ་ཕྱག་འཚལ་ལོ། །གང་ཞིག་ཀུན་དུ་མ་ཤེས་ན། །",
        "སྲིད་པ་གསུམ་དུ་རྣམ་འཁོར་བ། །སེམས་ཅན་ཀུན་ལ་ངེས་གནས་པའི། །ཆོས་ཀྱི་དབྱིངས་ལ་ཕྱག་འཚལ་འདུད། །",
        "གང་ཞིག་འཁོར་བའི་རྒྱུར་གྱུར་པ། །དེ་ཉིད་སྦྱང་བ་བྱས་པང་པོ་མི་་ལས། །དག་པ་དེ་ཉིད་མྱ་ངན་འདས། །",
        "ཆོས་ཀྱི་སྐུ་ཡང་དེ་ཉིད་དོ། །ཇི་ལྟར་འོ་མ་དང་འདྲེས་པས། །མར་གྱི་སྙིསྣང་བ། །",
        "དེ་བཞིན་ཉོན་མོངས་དང་འདྲེས་པས། །ཆོས་ཀྱི་དབྱིངས་ཀྱང་མི་མཐོང་ངོ་། །ཇི་ལྟར་འོ་མ་རྣམ་སྦྱངས་པས། །",
        "མར་གྱི་སྙིང་པོ་དྲི་མེད་འགྱུར། །དེ་བཞིན་ཉོན་མོངས་རྣམ་སྦྱངས་པས། །ཆོས་དབྱིངས་ཤིན་ཏུ་དྲི་མེད་འགྱུར། །",
    ]
    for ann, expected_segment in zip(
        parser.meaning_segment_anns, expected_meaning_segments
    ):
        start, end = (
            ann[LayerEnum.meaning_segment.value]["start"],
            ann[LayerEnum.meaning_segment.value]["end"],
        )
        assert parser.base_text[start:end] == expected_segment
