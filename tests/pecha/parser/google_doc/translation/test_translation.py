import tempfile
from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.google_doc.translation import GoogleDocTranslationParser

DATA_DIR = Path(__file__).parent / "data"


def test_bo_google_doc_translation_parser():
    bo_docx_file = DATA_DIR / "bo" / "Tibetan Root text Translation .docx"
    bo_metadata = DATA_DIR / "bo" / "Tibetan Root text Translation Metadata.xlsx"

    parser = GoogleDocTranslationParser()
    with tempfile.TemporaryDirectory() as tmpdirname:
        OUTPUT_DIR = Path(tmpdirname)
        pecha, _ = parser.parse(
            input=bo_docx_file,
            metadata=bo_metadata,
            output_path=OUTPUT_DIR,
        )

        assert isinstance(pecha, Pecha)

        assert (
            parser.base
            == "རྒྱ་གར་སྐད་དུ། ཨརྱཱ་བཛྲ་ཙྪེད་ཀ་པྲཛྙཱ་པ་ར་མི་ཏཱ་ནཱ་མ་མ་ཧཱ་ཡ་ན་སཱུ་ཏྲ། བོད་སྐད་དུ། འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ།\nསངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །\nའདི་སྐད་བདག་གིས་ཐོས་པ་དུས་གཅིག་ན།  བཅོམ་ལྡན་འདས་མཉན་ཡོད་ན་རྒྱལ་བུ་རྒྱལ་བྱེད་ཀྱི་ཚལ་མགོན་མེད་ཟས་སྦྱིན་གྱི་ཀུན་དགའ་ར་བ་ན། དགེ་སློང་སྟོང་ཉིས་བརྒྱ་ལྔ་བཅུའི་དགེ་སློང་གི་དགེ་འདུན་ཆེན་པོ་དང༌། བྱང་ཆུབ་སེམས་དཔའ་སེམས་དཔའ་ཆེན་པོ་རབ་ཏུ་མང་པོ་དག་དང་ཐབས་གཅིག་ཏུ་བཞུགས་སོ། །"
        )
        expected_anns = [
            {"Tibetan_Segment": {"start": 0, "end": 158}, "root_idx_mapping": "1"},
            {"Tibetan_Segment": {"start": 159, "end": 210}, "root_idx_mapping": "2"},
            {"Tibetan_Segment": {"start": 211, "end": 470}, "root_idx_mapping": "3"},
        ]
        assert parser.anns == expected_anns


def test_en_google_doc_translation_parser():
    en_docx_file = DATA_DIR / "en" / "English aligned Root Text Translation.docx"
    en_metadata = DATA_DIR / "en" / "English Root text Translation Metadata.xlsx"

    parser = GoogleDocTranslationParser()
    with tempfile.TemporaryDirectory() as tmpdirname:
        OUTPUT_DIR = Path(tmpdirname)

        pecha, _ = parser.parse(
            input=en_docx_file,
            metadata=en_metadata,
            output_path=OUTPUT_DIR,
        )

        assert isinstance(pecha, Pecha)

        assert (
            parser.base
            == 'In Sanskrit: Āryavajracchedikā-prajñāpāramitā-nāma-mahāyāna-sūtra In Tibetan: The Noble Mahāyāna Sūtra "The Perfection of Wisdom that Cuts Like a Diamond"\nHomage to all Buddhas and Bodhisattvas.\nThus have I heard at one time: The Blessed One was dwelling in Śrāvastī, in the Jeta Grove, in Anāthapiṇḍada\'s park, together with a great assembly of 1,250 monks and a great number of bodhisattva mahāsattvas.'
        )
        expected_anns = [
            {"English_Segment": {"start": 0, "end": 154}, "root_idx_mapping": "1"},
            {"English_Segment": {"start": 155, "end": 194}, "root_idx_mapping": "2"},
            {"English_Segment": {"start": 195, "end": 404}, "root_idx_mapping": "3"},
        ]
        assert parser.anns == expected_anns


def test_zh_google_doc_translation_parser():
    en_docx_file = DATA_DIR / "zh" / "Chinese aligned Root Text Translation.docx"
    en_metadata = DATA_DIR / "zh" / "Chinese Root text Translation Metadata.xlsx"

    parser = GoogleDocTranslationParser()
    with tempfile.TemporaryDirectory() as tmpdirname:
        OUTPUT_DIR = Path(tmpdirname)

        pecha, _ = parser.parse(
            input=en_docx_file,
            metadata=en_metadata,
            output_path=OUTPUT_DIR,
        )

        assert isinstance(pecha, Pecha)

        assert (
            parser.base
            == "梵文：Āryavajracchedikā-prajñāpāramitā-nāma-mahāyāna-sūtra 藏文：圣般若波罗蜜多金刚经大乘经\n礼敬一切佛菩萨。\n如是我闻，一时：佛在舍卫国祇树给孤独园，与大比丘众千二百五十人俱，并诸菩萨摩诃萨众多。"
        )
        expected_anns = [
            {"Chinese_Segment": {"start": 0, "end": 72}, "root_idx_mapping": "1"},
            {"Chinese_Segment": {"start": 73, "end": 81}, "root_idx_mapping": "2"},
            {"Chinese_Segment": {"start": 82, "end": 125}, "root_idx_mapping": "3"},
        ]
        assert parser.anns == expected_anns
