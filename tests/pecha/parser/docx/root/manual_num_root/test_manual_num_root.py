import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.docx.root.manual_num_root import DocxManualNumRootParser
from openpecha.pecha.parsers.parser_utils import extract_metadata_from_xlsx


class TestDocxManualNumRootParser(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"

    def test_bo_google_doc_translation_parser(self):
        bo_docx_file = self.DATA_DIR / "bo" / "Tibetan Root text Translation .docx"
        bo_metadata = (
            self.DATA_DIR / "bo" / "Tibetan Root text Translation Metadata.xlsx"
        )

        parser = DocxManualNumRootParser()

        expected_anns = [
            {"Tibetan_Segment": {"start": 0, "end": 158}, "root_idx_mapping": "1"},
            {"Tibetan_Segment": {"start": 159, "end": 210}, "root_idx_mapping": "2"},
            {"Tibetan_Segment": {"start": 211, "end": 470}, "root_idx_mapping": "3"},
        ]
        expected_base = "རྒྱ་གར་སྐད་དུ། ཨརྱཱ་བཛྲ་ཙྪེད་ཀ་པྲཛྙཱ་པ་ར་མི་ཏཱ་ནཱ་མ་མ་ཧཱ་ཡ་ན་སཱུ་ཏྲ། བོད་སྐད་དུ། འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ།\nསངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །\nའདི་སྐད་བདག་གིས་ཐོས་པ་དུས་གཅིག་ན།  བཅོམ་ལྡན་འདས་མཉན་ཡོད་ན་རྒྱལ་བུ་རྒྱལ་བྱེད་ཀྱི་ཚལ་མགོན་མེད་ཟས་སྦྱིན་གྱི་ཀུན་དགའ་ར་བ་ན། དགེ་སློང་སྟོང་ཉིས་བརྒྱ་ལྔ་བཅུའི་དགེ་སློང་གི་དགེ་འདུན་ཆེན་པོ་དང༌། བྱང་ཆུབ་སེམས་དཔའ་སེམས་དཔའ་ཆེན་པོ་རབ་ཏུ་མང་པོ་དག་དང་ཐབས་གཅིག་ཏུ་བཞུགས་སོ། །"
        metadata = extract_metadata_from_xlsx(bo_metadata)
        anns, base = parser.extract_root_idx(bo_docx_file, metadata)

        assert (
            anns == expected_anns
        ), "Translation Parser failed parsing Root anns properly for bo data."
        assert (
            base == expected_base
        ), "Translation Parser failed preparing base text properly for bo data"

        with tempfile.TemporaryDirectory() as tmpdirname, patch(
            "openpecha.pecha.parsers.docx.root.manual_num_root.DocxManualNumRootParser.extract_root_idx"
        ) as mock_extract_root_idx:
            OUTPUT_DIR = Path(tmpdirname)
            mock_extract_root_idx.return_value = (expected_anns, expected_base)
            pecha = parser.parse(bo_docx_file, metadata, OUTPUT_DIR)

            assert isinstance(pecha, Pecha)

    def test_en_google_doc_translation_parser(self):
        en_docx_file = (
            self.DATA_DIR / "en" / "English aligned Root Text Translation.docx"
        )
        en_metadata = (
            self.DATA_DIR / "en" / "English Root text Translation Metadata.xlsx"
        )

        parser = DocxManualNumRootParser()

        expected_anns = [
            {"English_Segment": {"start": 0, "end": 154}, "root_idx_mapping": "1"},
            {"English_Segment": {"start": 155, "end": 194}, "root_idx_mapping": "2"},
            {"English_Segment": {"start": 195, "end": 404}, "root_idx_mapping": "3"},
        ]
        expected_base = 'In Sanskrit: Āryavajracchedikā-prajñāpāramitā-nāma-mahāyāna-sūtra In Tibetan: The Noble Mahāyāna Sūtra "The Perfection of Wisdom that Cuts Like a Diamond"\nHomage to all Buddhas and Bodhisattvas.\nThus have I heard at one time: The Blessed One was dwelling in Śrāvastī, in the Jeta Grove, in Anāthapiṇḍada\'s park, together with a great assembly of 1,250 monks and a great number of bodhisattva mahāsattvas.'

        metadata = extract_metadata_from_xlsx(en_metadata)
        anns, base = parser.extract_root_idx(en_docx_file, metadata)

        assert (
            anns == expected_anns
        ), "Translation Parser failed parsing Root anns properly for en data."
        assert (
            base == expected_base
        ), "Translation Parser failed preparing base text properly for en data"

        with tempfile.TemporaryDirectory() as tmpdirname, patch(
            "openpecha.pecha.parsers.docx.root.manual_num_root.DocxManualNumRootParser.extract_root_idx"
        ) as mock_extract_root_idx:
            OUTPUT_DIR = Path(tmpdirname)
            mock_extract_root_idx.return_value = (expected_anns, expected_base)
            pecha = parser.parse(en_docx_file, metadata, OUTPUT_DIR)

            assert isinstance(pecha, Pecha)

    def test_zh_google_doc_translation_parser(self):
        zh_docx_file = (
            self.DATA_DIR / "zh" / "Chinese aligned Root Text Translation.docx"
        )
        zh_metadata = (
            self.DATA_DIR / "zh" / "Chinese Root text Translation Metadata.xlsx"
        )

        parser = DocxManualNumRootParser()
        expected_anns = [
            {"Chinese_Segment": {"start": 0, "end": 72}, "root_idx_mapping": "1"},
            {"Chinese_Segment": {"start": 73, "end": 81}, "root_idx_mapping": "2"},
            {"Chinese_Segment": {"start": 82, "end": 125}, "root_idx_mapping": "3"},
        ]
        expected_base = "梵文：Āryavajracchedikā-prajñāpāramitā-nāma-mahāyāna-sūtra 藏文：圣般若波罗蜜多金刚经大乘经\n礼敬一切佛菩萨。\n如是我闻，一时：佛在舍卫国祇树给孤独园，与大比丘众千二百五十人俱，并诸菩萨摩诃萨众多。"

        metadata = extract_metadata_from_xlsx(zh_metadata)
        anns, base = parser.extract_root_idx(zh_docx_file, metadata)

        assert (
            anns == expected_anns
        ), "Translation Parser failed parsing Root anns properly for zh data."
        assert (
            base == expected_base
        ), "Translation Parser failed preparing base text properly for zh data"

        with tempfile.TemporaryDirectory() as tmpdirname, patch(
            "openpecha.pecha.parsers.docx.root.manual_num_root.DocxManualNumRootParser.extract_root_idx"
        ) as mock_extract_root_idx:
            OUTPUT_DIR = Path(tmpdirname)
            mock_extract_root_idx.return_value = (expected_anns, expected_base)
            pecha = parser.parse(zh_docx_file, metadata, OUTPUT_DIR)

            assert isinstance(pecha, Pecha)


work = TestDocxManualNumRootParser()
work.setUp()
work.test_bo_google_doc_translation_parser()
