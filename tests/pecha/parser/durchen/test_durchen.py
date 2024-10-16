from pathlib import Path

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

    assert parser.anns == [
        {
            "Durchen": {"start": 0, "end": 5},
            "note": "(1) <«ཅོ་»«སྡེ་»«སྣར་»«པེ་»༄༅། །ཆོས་ཀྱི་དབྱིངས་སུ་བསྟོད་པ། ༄༅༅། །>",
        },
        {"Durchen": {"start": 79, "end": 90}, "note": "(3) <«སྣར་»«པེ་»འཇམ་>"},
        {"Durchen": {"start": 231, "end": 236}, "note": "(4) <«སྣར་»«པེ་»ལོ།>"},
        {"Durchen": {"start": 540, "end": 544}, "note": "(5) <«སྣར་»«པེ་»རྣམས་>"},
    ]


test_durchen()
