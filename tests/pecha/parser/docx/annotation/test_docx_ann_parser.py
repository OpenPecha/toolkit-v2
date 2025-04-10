from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser
from openpecha.pecha.pecha_types import PechaType


class TestDocxAnnotationParser(TestCase):
    def setUp(self):
        self.parser = DocxAnnotationParser()
        self.root_display_pecha = Pecha.from_path(
            Path("tests/alignment/commentary_transfer/data/P1/IA6E66F92")
        )
        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_display_pecha.metadata.to_dict(),
        }

    def test_is_root_related_pecha(self):
        # Test root pecha types
        assert self.parser.is_root_related_pecha(PechaType.root_pecha)
        assert self.parser.is_root_related_pecha(
            PechaType.prealigned_root_translation_pecha
        )

        # Test non-root pecha types
        assert not self.parser.is_root_related_pecha(PechaType.commentary_pecha)
        assert not self.parser.is_root_related_pecha(
            PechaType.prealigned_commentary_pecha
        )

    def test_is_commentary_related_pecha(self):
        # Test commentary pecha types
        assert self.parser.is_commentary_related_pecha(PechaType.commentary_pecha)
        assert self.parser.is_commentary_related_pecha(
            PechaType.prealigned_commentary_pecha
        )

        # Test non-commentary pecha types
        assert not self.parser.is_commentary_related_pecha(PechaType.root_pecha)
        assert not self.parser.is_commentary_related_pecha(
            PechaType.prealigned_root_translation_pecha
        )

    def test_root_pecha(self):
        ann_type = LayerEnum.root_segment
        ann_title = "དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1"
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/root_display_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1.docx"
        )
        metadatas = [self.root_display_pecha_metadata]

        layer_path = self.parser.add_annotation(
            self.root_display_pecha, ann_type, ann_title, docx_file, metadatas
        )

        new_anns = get_anns(AnnotationStore(file=str(layer_path)))
        layer_path.unlink()
        expected_new_anns = [
            {
                "root_idx_mapping": "1",
                "Translation_Segment": "English_Segment",
                "text": "བུ་མ་འཇུག་པ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ མངོན་དུ་ཕྱོགས་པར་མཉམ་བཞག་སེམས་གནས་ཏ",
            },
            {
                "root_idx_mapping": "2",
                "Translation_Segment": "English_Segment",
                "text": "། །རྫོགས་པའི་སངས་རྒྱས་ཆོས་ལ་མངོན་ཕྱོགས་",
            },
            {
                "root_idx_mapping": "3",
                "Translation_Segment": "English_Segment",
                "text": "ིང༌། །འདི་བརྟེན་འབྱུང་བའི་དེ་ཉིད་མཐ",
            },
            {
                "root_idx_mapping": "4",
                "Translation_Segment": "English_Segment",
                "text": "ང་བ་དེས། །ཤེས་རབ་གནས་པས་འགོག་པ་",
            },
            {
                "root_idx_mapping": "5",
                "Translation_Segment": "English_Segment",
                "text": "ོབ་པར་འགྱུར། །\nཇི་ལྟར་ལོང་བའི་ཚོགས་ཀུན་བདེ་བླག་ཏུ། །མིག་ལྡན་སྐྱེས་བུ་གཅིག་གིས་འདོད་པ་ཡི། །ཡུལ་དུ་འཁྲིད་པ་དེ་བཞིན་འདིར་ཡང་བློས། །མིག་ཉམས་ཡོན་ཏན་བླངས་",
            },
            {
                "root_idx_mapping": "6",
                "Translation_Segment": "English_Segment",
                "text": "ེ་རྒྱལ་ཉིད་འགྲོ། །\nཇི་ལྟར་དེ་ཡིས་ཆེས་ཟབ་ཆོས་རྟོགས་པ། །ལུང་དང་གཞན་ཡང་རིགས་པས་ཡིན་པས་ན། །དེ་ལྟར་འཕགས་པ་ཀླུ་སྒྲུབ་གཞུང་ལུགས་ལས། །ཇི་ལྟར་གནས་པའི་ལ",
            },
            {
                "root_idx_mapping": "7",
                "Translation_Segment": "English_Segment",
                "text": "གས་བཞིན་བརྗོད་པར་བྱ། །\nསོ་སོ་སྐྱེ་བོའི་དུས་ནའང་སྟོང་པ་ཉིད་ཐོས་ནས། །ནང་དུ་རབ་ཏུ་དགའ་བ་ཡང་དང་ཡང་དུ་འབྱུང༌། །རབ་ཏུ་དགའ་བ་ལས་བྱུང་མཆི་མས་མིག་བརླན་ཞིང༌། །ལུས་ཀྱི་བ་སྤུ",
            },
            {
                "root_idx_mapping": "8",
                "Translation_Segment": "English_Segment",
                "text": "ལྡང་པར་འགྱུར་པ་གང་ཡིན་པ། །\nདེ་ལ་རྫོགས་པའི་སངས་རྒྱས་བློ་ཡི་ས་བོན་ཡོད། །དེ་ཉིད་ཉེ་བར་བསྟན་པའི་སྣོད་ནི་དེ་ཡིན་ཏེ། །དེ་ལ་དམ་པའི་དོན་གྱི་བདེན་པ་བསྟན་པར་བྱ། །དེ་ལ་དེ་ཡི་རྗ",
            },
            {
                "root_idx_mapping": "9",
                "Translation_Segment": "English_Segment",
                "text": "ས་སུ་འགྲོ་བའི་ཡོན་ཏན་འབྱུང༌། །\nརྟག་ཏུ་ཚུལ་ཁྲིམས་ཡང་དག་བླངས་ནས་གནས་པར་འགྱུར། །སྦྱིན་པ་གཏོང་བར་འགྱུར་ཞིང་སྙིང་རྗེ་བསྟེན་པར་བྱེད། །བཟོད་པ་སྒོམ་བྱེད་དེ་ཡི་དགེ་བའང་བྱང་ཆུབ་ཏུ། །འགྲོ་བ་དགྲོལ་བ",
            },
            {
                "root_idx_mapping": "10",
                "Translation_Segment": "English_Segment",
                "text": "་བྱ་ཕྱིར་ཡོངས་སུ་བསྔོ་བྱེད་ཅིང༌། །\nརྫོགས་པའི་བྱང་ཆུབ་སེམས་དཔའ་རྣམས་ལ་གུས་པར་བྱེད། །ཟབ་ཅིང་རྒྱ་ཆེའི་ཚུལ་ལ་མཁས་པའི་སྐྱེ་བོས་ནི། །རིམ་གྱིས་རབ་ཏུ་དགའ་བའི་ས་ནི་འཐོབ་འགྱུར་བས། །དེ",
            },
            {
                "root_idx_mapping": "11",
                "Translation_Segment": "English_Segment",
                "text": "ནི་དོན་དུ་གཉེར་བས་ལམ་འདི་མཉན་པར་གྱིས། །\nདེ་ཉིད་དེ་ལས་འབྱུང་མིན་གཞན་དག་ལས་ལྟ་ག་ལ་ཞིག །གཉིས་ཀ་ལས་ཀྱང་མ་ཡིན་རྒྱུ་མེད་པར་ནི་ག་ལ་ཡོད། །དེ་ནི་དེ་ལས་འབྱུང་ན་ཡོན་ཏན་འགའ་ཡང་ཡོད་མ་ཡིན། །སྐྱེས་པ",
            },
            {
                "root_idx_mapping": "12",
                "Translation_Segment": "English_Segment",
                "text": "་གྱུར་པ་སླར་ཡང་སྐྱེ་བར་རིགས་པའང་མ་ཡིན་ཉིད། །\nསྐྱེས་ཟིན་སླར་ཡང་སྐྱེ་བར་ཡོངས་སུ་རྟོག་པར་འགྱུར་ན་ནི། །མྱུ་གུ་ལ་སོགས་རྣམས་ཀྱི་སྐྱེ་བ་འདིར་རྙེད་མི་འགྱུར་ཞིང༌། །ས་བོན་སྲིད་མཐར་ཐུག་པར་རབ་ཏུ་སྐྱེ་བ་ཉིད་དུ་འགྱུར། །ཇི་",
            },
        ]
        assert new_anns == expected_new_anns
