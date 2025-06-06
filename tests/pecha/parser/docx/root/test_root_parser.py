import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import SegmentationAnnotation, Span
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers.docx.root import DocxRootParser
from openpecha.utils import read_json


class TestDocxRootParser(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.parser = DocxRootParser()

    def test_bo_google_doc_translation_parser(self):
        bo_docx_file = self.DATA_DIR / "bo/entering_middle_way.docx"
        metadata = read_json(self.DATA_DIR / "bo/metadata.json")

        expected_anns = [
            SegmentationAnnotation(
                span=Span(start=0, end=41, errors=None), metadata=None, index=1
            ),
            SegmentationAnnotation(
                span=Span(start=42, end=200, errors=None), metadata=None, index=2
            ),
            SegmentationAnnotation(
                span=Span(start=201, end=353, errors=None), metadata=None, index=3
            ),
            SegmentationAnnotation(
                span=Span(start=354, end=500, errors=None), metadata=None, index=4
            ),
            SegmentationAnnotation(
                span=Span(start=501, end=667, errors=None), metadata=None, index=5
            ),
        ]
        expected_base = "དབུ་མ་ལུ་འཇུག་པ་ལས། སེམས་བསྐྱེད་པ་དྲུག་པ།\nམངོན་དུ་ཕྱོགས་པར་མཉམ་བཞག་སེམས་གནས་ཏེ། །རྫོགས་པའི་སངས་རྒྱས་ཆོས་ལ་མངོན་ཕྱོགས་ཤིང༌། །འདི་བརྟེན་འབྱུང་བའི་དེ་ཉིད་མཐོང་བ་དེས། །ཤེས་རབ་གནས་པས་འགོག་པ་ཐོབ་པར་འགྱུར། །\nཇི་ལྟར་ལོང་བའི་ཚོགས་ཀུན་བདེ་བླག་ཏུ། །མིག་ལྡན་སྐྱེས་བུ་གཅིག་གིས་འདོད་པ་ཡི། །ཡུལ་དུ་འཁྲིད་པ་དེ་བཞིན་འདིར་ཡང་བློས། །མིག་ཉམས་ཡོན་ཏན་བླངས་ཏེ་རྒྱལ་ཉིད་འགྲོ། །\nཇི་ལྟར་དེ་ཡིས་ཆེས་ཟབ་ཆོས་རྟོགས་པ། །ལུང་དང་གཞན་ཡང་རིགས་པས་ཡིན་པས་ན། །དེ་ལྟར་འཕགས་པ་ཀླུ་སྒྲུབ་གཞུང་ལུགས་ལས། །ཇི་ལྟར་གནས་པའི་ལུགས་བཞིན་བརྗོད་པར་བྱ། །\nསོ་སོ་སྐྱེ་བོའི་དུས་ནའང་སྟོང་པ་ཉིད་ཐོས་ནས། །ནང་དུ་རབ་ཏུ་དགའ་བ་ཡང་དང་ཡང་དུ་འབྱུང༌། །རབ་ཏུ་དགའ་བ་ལས་བྱུང་མཆི་མས་མིག་བརླན་ཞིང༌། །ལུས་ཀྱི་བ་སྤུ་ལྡང་པར་འགྱུར་པ་གང་ཡིན་པ། །\n"

        anns, base = self.parser.extract_anns(bo_docx_file, AnnotationType.SEGMENTATION)

        assert (
            anns == expected_anns
        ), "TestDocxRootParser failed extract segmentation coordinates for bo data."
        assert (
            base == expected_base
        ), "TestDocxRootParser failed preparing base text properly for bo data"

        with tempfile.TemporaryDirectory() as tmpdirname, patch(
            "openpecha.pecha.parsers.docx.root.DocxRootParser.extract_segmentation_anns"
        ) as mock_extract_root_idx, patch(
            "openpecha.pecha.get_base_id"
        ) as mock_get_base_id, patch(
            "openpecha.pecha.get_layer_id"
        ) as mock_get_layer_id:
            OUTPUT_DIR = Path(tmpdirname)
            mock_extract_root_idx.return_value = (
                expected_anns,
                expected_base,
            )
            mock_get_base_id.return_value = "B001"
            mock_get_layer_id.return_value = "L001"
            pecha, layer_name = self.parser.parse(
                bo_docx_file, AnnotationType.SEGMENTATION, metadata, OUTPUT_DIR
            )

            assert isinstance(pecha, Pecha)
            assert layer_name == "B001/segmentation-L001.json"

    def test_en_google_doc_translation_parser(self):
        en_docx_file = self.DATA_DIR / "en" / "entering the middle way english.docx"
        metadata = read_json(self.DATA_DIR / "en" / "metadata.json")

        expected_anns = [
            SegmentationAnnotation(
                span=Span(start=0, end=50, errors=None), metadata=None, index=1
            ),
            SegmentationAnnotation(
                span=Span(start=51, end=281, errors=None), metadata=None, index=2
            ),
            SegmentationAnnotation(
                span=Span(start=282, end=500, errors=None), metadata=None, index=3
            ),
            SegmentationAnnotation(
                span=Span(start=501, end=707, errors=None), metadata=None, index=4
            ),
            SegmentationAnnotation(
                span=Span(start=708, end=907, errors=None), metadata=None, index=5
            ),
        ]
        expected_base = '"From the Madhyamakavatara, Sixth Mind Generation"\n"When the mind rests in meditative equipoise, directly oriented Towards the qualities of the fully enlightened Buddha, And through this, sees the reality of dependent origination, Through abiding in wisdom, one attains cessation."\n"Just as a single person with eyes Can easily lead an entire group of blind people To their desired destination, likewise here too, intelligence Takes hold of the qualities lacking sight and proceeds to enlightenment."\n"Just as one understands these profound teachings Through scripture and through reasoning as well, Similarly, following the tradition of Noble Nagarjuna\'s writings, I shall explain things just as they are."\n"Even while still an ordinary being, upon hearing about emptiness, Great joy arises again and again within. From this supreme joy, tears moisten one\'s eyes, And the hairs of one\'s body stand on end."\n'

        anns, base = self.parser.extract_anns(en_docx_file, AnnotationType.SEGMENTATION)

        assert (
            anns == expected_anns
        ), "TestDocxRootParser failed extract segmentation coordinates for en data."
        assert (
            base == expected_base
        ), "TestDocxRootParser failed preparing base text properly for en data"

        with tempfile.TemporaryDirectory() as tmpdirname, patch(
            "openpecha.pecha.parsers.docx.root.DocxRootParser.extract_segmentation_anns"
        ) as mock_extract_root_idx, patch(
            "openpecha.pecha.get_base_id"
        ) as mock_get_base_id, patch(
            "openpecha.pecha.get_layer_id"
        ) as mock_get_layer_id:
            OUTPUT_DIR = Path(tmpdirname)
            mock_extract_root_idx.return_value = (
                expected_anns,
                expected_base,
            )
            mock_get_base_id.return_value = "B002"
            mock_get_layer_id.return_value = "L002"

            pecha, layer_name = self.parser.parse(
                en_docx_file, AnnotationType.SEGMENTATION, metadata, OUTPUT_DIR
            )

            assert isinstance(pecha, Pecha)
            assert layer_name == "B002/segmentation-L002.json"
