import tempfile
from pathlib import Path

from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.pedurma import PedurmaParser
from openpecha.utils import read_json


def test_pedurma():
    data = Path(__file__).parent / "data"
    pedurmafile = data / "pedurma_hfml.txt"
    pedurma_text = pedurmafile.read_text(encoding="utf-8")

    metadata_file = data / "metadata.json"
    metadata = read_json(metadata_file)

    parser = PedurmaParser()

    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        parser.parse(pedurma_text, metadata=metadata, output_path=output_path)

        expected_base = (data / "expected_base.txt").read_text(encoding="utf-8")
        assert parser.base_text == expected_base

        # Checking extracted pedurma annotations
        expected_span_texts = ["༄༅། །", "འཕགས་པ་འཇམ་", "འདུད།", "རྣམ་"]
        for ann, expected_span in zip(parser.pedurma_anns, expected_span_texts):
            start, end = (
                ann[LayerEnum.DURCHEN.value]["start"],
                ann[LayerEnum.DURCHEN.value]["end"],
            )
            assert parser.base_text[start:end] == expected_span

        expected_ann_notes = [
            "(1) <«ཅོ་»«སྡེ་»«སྣར་»«པེ་»༄༅། །ཆོས་ཀྱི་དབྱིངས་སུ་བསྟོད་པ། ༄༅༅། །>",
            "(3) <«སྣར་»«པེ་»འཇམ་>",
            "(4) <«སྣར་»«པེ་»ལོ།>",
            "(5) <«སྣར་»«པེ་»རྣམས་>",
        ]

        for ann, expected_note in zip(parser.pedurma_anns, expected_ann_notes):
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
                ann[LayerEnum.SEGMENTATION.value]["start"],
                ann[LayerEnum.SEGMENTATION.value]["end"],
            )
            assert parser.base_text[start:end] == expected_segment
