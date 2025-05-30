import tempfile
from pathlib import Path
from unittest import TestCase, mock
from unittest.mock import patch

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AlignmentAnnotation, Span
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
from openpecha.utils import read_json


class TestDocxSimpleCommentaryParser(TestCase):
    def setUp(self):
        self.data_dir = Path(__file__).parent / "data"
        self.input = self.data_dir / "དབུ་མ་_bo_commentary.docx"
        self.metadata = read_json(self.data_dir / "metadata.json")
        self.expected_anns = [
            AlignmentAnnotation(
                span=Span(start=0, end=65, errors=None),
                metadata=None,
                index=1,
                alignment_index="1",
            ),
            AlignmentAnnotation(
                span=Span(start=66, end=330, errors=None),
                metadata=None,
                index=2,
                alignment_index="2",
            ),
            AlignmentAnnotation(
                span=Span(start=331, end=758, errors=None),
                metadata=None,
                index=3,
                alignment_index="2,3",
            ),
            AlignmentAnnotation(
                span=Span(start=759, end=1075, errors=None),
                metadata=None,
                index=4,
                alignment_index="3-5",
            ),
            AlignmentAnnotation(
                span=Span(start=1076, end=1470, errors=None),
                metadata=None,
                index=5,
                alignment_index="2,4-5",
            ),
        ]
        self.expected_base = "དབུ་མ་དགོངས་པ་རབ་གསལ་ལེའུ་དྲུག་པ་བདེན་གཉིས་སོ་སོའི་ངོ་བོ་བཤད་པ།། \nགསུམ་པ་ལ་གཉིས། ཀུན་རྫོབ་ཀྱི་བདེན་པ་བཤད་པ་དང་། དོན་དམ་པའི་བདེན་པ་བཤད་པའོ། །དང་པོ་ལ་གསུམ། ཀུན་རྫོབ་པ་གང་གི་ངོར་བདེན་ལ་གང་གི་ངོར་མི་བདེན་པ་དང་། ཀུན་རྫོབ་ཙམ་དེ་གང་ཟག་གསུམ་ལ་སྣང་བ་དང་མི་སྣང་བའི་ཚུལ་དང་། སོ་སྐྱེ་དང་འཕགས་པ་ལ་ལྟོས་ཏེ་དོན་དམ་པ་དང་ཀུན་རྫོབ་ཏུ་འགྱུར་ཚུལ་ལོ། \nདེས་གང་ལ་སྒྲིབ་ན་ཡང་དག་ཀུན་རྫོབ་འདོད་ཅེས་པས་ཡང་དག་པའི་དོན་ལ་སྒྲིབ་པས་ཀུན་རྫོབ་བམ་སྒྲིབ་བྱེད་དུ་འདོད་ཅེས་པ་སྟེ། ཡང་ལོག་གཉིས་ཀྱི་ནང་ནས་ཡང་དག་ཀུན་རྫོབ་ཏུ་སྟོན་པ་མིན་ནོ། །རྐང་པ་དང་པོས་བསྟན་པའི་ཀུན་རྫོབ་དང་། རྐང་པ་ཕྱི་མ་གཉིས་ཀྱིས་བསྟན་པའི་ཀུན་རྫོབ་གཉིས་གཅིག་ཏུ་མི་བྱ་སྟེ། དང་པོ་ནི། རང་གིས་དངོས་པོ་རྣམས་སྐྱེ་བ་སོགས་སུ་གང་དུ་ཁས་ལེན་པའི་ཀུན་རྫོབ་ཡིན་ལ། ཕྱི་མ་ནི་དངོས་པོ་རྣམས་གང་གི་ངོར་བདེན་པའི་བདེན་འཛིན་གྱི་ཀུན་རྫོབ་ཡིན་པའི་ཕྱིར་རོ། །\nཀུན་རྫོབ་བདེན་འཛིན་དེའི་མཐུས་སྔོན་པོ་ལ་སོགས་པ་གང་ཞིག རང་བཞིན་གྱིས་གྲུབ་པ་མེད་བཞིན་དུ་དེར་སྣང་བར་བཅོས་པའི་བཅོས་མ་སེམས་ཅན་རྣམས་ལ་བདེན་པར་སྣང་བ་དེ་ནི། སྔར་བཤད་པའི་འཇིག་རྟེན་གྱི་ཕྱིན་ཅི་ལོག་གི་ཀུན་རྫོབ་པ་དེའི་ངོར་བདེན་པས་འཇིག་རྟེན་གྱི་ཀུན་རྫོབ་ཀྱི་བདེན་པ་ཞེས་ཐུབ་པ་དེས་གསུངས་ཏེ། གསུངས་ཚུལ་ནི་སྔར་གྱི་མདོ་དེར་གསུངས་པའོ། །\nགང་ཟག་གསུམ་པོ་གང་གི་ངོར་མི་བདེན་པའི་རྟོག་པས་བཅོས་པས་བཅོས་མར་གྱུར་པའི་དངོས་པོ་ནི་དེའི་ཀུན་རྫོབ་པའི་ངོར་མི་བདེན་པས་ཀུན་རྫོབ་ཙམ་ཞེས་བྱའོ། །རྟེན་འབྱུང་གཟུགས་བརྙན་དང་བྲག་ཆ་སོགས་ཅུང་ཟད་ཅིག་ནི་བརྫུན་ཡང་མ་རིག་པ་དང་ལྡན་པ་རྣམས་ལ་སྣང་ལ། སྔོན་པོ་ལ་སོགས་པའི་གཟུགས་དང་སེམས་དང་ཚོར་བ་སོགས་ཅུང་ཟད་ཅིག་ནི་བདེན་པར་སྣང་སྟེ། ཆོས་རྣམས་ཀྱི་ཡིན་ལུགས་ཀྱི་རང་བཞིན་ནི་མ་རིག་པ་དང་ལྡན་པ་རྣམས་ལ་རྣམ་པ་ཐམས་ཅད་དུ་མི་སྣང་ངོ་། །\n"

    def test_extract_commentary_segments(self):
        parser = DocxSimpleCommentaryParser()
        anns, base = parser.extract_anns(self.input, AnnotationType.ALIGNMENT)

        assert (
            anns == self.expected_anns
        ), "NumberedList Commentary Parser failed parsing commentary segments properly."
        assert (
            base == self.expected_base
        ), "NumberedList Commentary failed preparing base text properly."

    def test_create_pecha(self):
        parser = DocxSimpleCommentaryParser()
        with tempfile.TemporaryDirectory() as tempdir, mock.patch(
            "openpecha.pecha.parsers.docx.commentary.simple.DocxSimpleCommentaryParser.extract_anns"
        ) as mock_extract_commentary_segments_anns, patch(
            "openpecha.pecha.get_base_id"
        ) as mock_get_base_id, patch(
            "openpecha.pecha.get_layer_id"
        ) as mock_get_layer_id:
            mock_extract_commentary_segments_anns.return_value = (
                self.expected_anns,
                self.expected_base,
            )
            mock_get_base_id.return_value = "B001"
            mock_get_layer_id.return_value = "L001"

            pecha, layer_name = parser.parse(
                self.input, AnnotationType.SEGMENTATION, self.metadata, Path(tempdir)
            )
            assert isinstance(pecha, Pecha)
            assert layer_name == "B001/segmentation-L001.json"
