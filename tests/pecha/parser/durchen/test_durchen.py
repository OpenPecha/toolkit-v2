from pathlib import Path

from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.durchen import DurchenParser


def test_durchen():
    data = Path(__file__).parent / "data"
    pedurmafile = data / "pedurma_hfml.txt"
    pedurma_text = pedurmafile.read_text(encoding="utf-8")

    parser = DurchenParser()

    output_path = Path(__file__).parent / "output"
    parser.parse(pedurma_text, metadata={}, output_path=output_path)

    expected_base = (data / "expected_base.txt").read_text(encoding="utf-8")
    assert parser.base_text == expected_base

    # Check if parser has extract annotations in proper manner
    expected_span_texts = ["༄༅། །", "འཕགས་པ་འཇམ་", "འདུད།", "རྣམ་"]
    for ann, expected_span in zip(parser.anns, expected_span_texts):
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

    for ann, expected_note in zip(parser.anns, expected_ann_notes):
        assert ann["note"] == expected_note


test_durchen()
