import tempfile
from pathlib import Path
from unittest.mock import patch

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.docx.root import DocxRootParser
from openpecha.pecha.parsers.parser_utils import extract_metadata_from_xlsx

DATA_DIR = Path(__file__).parent / "data"


def test_bo_google_doc_translation_parser():
    bo_docx_file = DATA_DIR / "bo/entering_middle_way.docx"
    bo_metadata = DATA_DIR / "bo/Tibetan Root text Translation Metadata.xlsx"

    parser = DocxRootParser()

    expected_anns = [
        {"Tibetan_Segment": {"start": 0, "end": 42}, "root_idx_mapping": "1"},
        {"Tibetan_Segment": {"start": 42, "end": 201}, "root_idx_mapping": "2"},
        {"Tibetan_Segment": {"start": 201, "end": 354}, "root_idx_mapping": "3"},
        {"Tibetan_Segment": {"start": 354, "end": 501}, "root_idx_mapping": "4"},
        {"Tibetan_Segment": {"start": 501, "end": 668}, "root_idx_mapping": "5"},
    ]
    expected_base = "དབུ་མ་ལུ་འཇུག་པ་ལས། སེམས་བསྐྱེད་པ་དྲུག་པ།\nམངོན་དུ་ཕྱོགས་པར་མཉམ་བཞག་སེམས་གནས་ཏེ། །རྫོགས་པའི་སངས་རྒྱས་ཆོས་ལ་མངོན་ཕྱོགས་ཤིང༌། །འདི་བརྟེན་འབྱུང་བའི་དེ་ཉིད་མཐོང་བ་དེས། །ཤེས་རབ་གནས་པས་འགོག་པ་ཐོབ་པར་འགྱུར། །\nཇི་ལྟར་ལོང་བའི་ཚོགས་ཀུན་བདེ་བླག་ཏུ། །མིག་ལྡན་སྐྱེས་བུ་གཅིག་གིས་འདོད་པ་ཡི། །ཡུལ་དུ་འཁྲིད་པ་དེ་བཞིན་འདིར་ཡང་བློས། །མིག་ཉམས་ཡོན་ཏན་བླངས་ཏེ་རྒྱལ་ཉིད་འགྲོ། །\nཇི་ལྟར་དེ་ཡིས་ཆེས་ཟབ་ཆོས་རྟོགས་པ། །ལུང་དང་གཞན་ཡང་རིགས་པས་ཡིན་པས་ན། །དེ་ལྟར་འཕགས་པ་ཀླུ་སྒྲུབ་གཞུང་ལུགས་ལས། །ཇི་ལྟར་གནས་པའི་ལུགས་བཞིན་བརྗོད་པར་བྱ། །\nསོ་སོ་སྐྱེ་བོའི་དུས་ནའང་སྟོང་པ་ཉིད་ཐོས་ནས། །ནང་དུ་རབ་ཏུ་དགའ་བ་ཡང་དང་ཡང་དུ་འབྱུང༌། །རབ་ཏུ་དགའ་བ་ལས་བྱུང་མཆི་མས་མིག་བརླན་ཞིང༌། །ལུས་ཀྱི་བ་སྤུ་ལྡང་པར་འགྱུར་པ་གང་ཡིན་པ། །\n"
    metadata = extract_metadata_from_xlsx(bo_metadata)
    anns, base = parser.extract_root_segments_anns(bo_docx_file, metadata)

    assert (
        anns == expected_anns
    ), "Translation Parser failed parsing Root anns properly for bo data."
    assert (
        base == expected_base
    ), "Translation Parser failed preparing base text properly for bo data"

    with tempfile.TemporaryDirectory() as tmpdirname, patch(
        "openpecha.pecha.parsers.docx.root.DocxRootParser.extract_root_segments_anns"
    ) as mock_extract_root_idx:
        OUTPUT_DIR = Path(tmpdirname)
        mock_extract_root_idx.return_value = (expected_anns, expected_base)
        pecha = parser.parse(bo_docx_file, metadata, OUTPUT_DIR)

        assert isinstance(pecha, Pecha)


def test_en_google_doc_translation_parser():
    en_docx_file = DATA_DIR / "en" / "entering the middle way english.docx"
    en_metadata = DATA_DIR / "en" / "English Root text Translation Metadata.xlsx"

    parser = DocxRootParser()

    expected_anns = [
        {"English_Segment": {"start": 0, "end": 51}, "root_idx_mapping": "1"},
        {"English_Segment": {"start": 51, "end": 282}, "root_idx_mapping": "2"},
        {"English_Segment": {"start": 282, "end": 501}, "root_idx_mapping": "3"},
        {"English_Segment": {"start": 501, "end": 708}, "root_idx_mapping": "4"},
        {"English_Segment": {"start": 708, "end": 908}, "root_idx_mapping": "5"},
    ]
    expected_base = '"From the Madhyamakavatara, Sixth Mind Generation"\n"When the mind rests in meditative equipoise, directly oriented Towards the qualities of the fully enlightened Buddha, And through this, sees the reality of dependent origination, Through abiding in wisdom, one attains cessation."\n"Just as a single person with eyes Can easily lead an entire group of blind people To their desired destination, likewise here too, intelligence Takes hold of the qualities lacking sight and proceeds to enlightenment."\n"Just as one understands these profound teachings Through scripture and through reasoning as well, Similarly, following the tradition of Noble Nagarjuna\'s writings, I shall explain things just as they are."\n"Even while still an ordinary being, upon hearing about emptiness, Great joy arises again and again within. From this supreme joy, tears moisten one\'s eyes, And the hairs of one\'s body stand on end."\n'

    metadata = extract_metadata_from_xlsx(en_metadata)
    anns, base = parser.extract_root_segments_anns(en_docx_file, metadata)

    assert (
        anns == expected_anns
    ), "Translation Parser failed parsing Root anns properly for en data."
    assert (
        base == expected_base
    ), "Translation Parser failed preparing base text properly for en data"

    with tempfile.TemporaryDirectory() as tmpdirname, patch(
        "openpecha.pecha.parsers.docx.root.DocxRootParser.extract_root_segments_anns"
    ) as mock_extract_root_idx:
        OUTPUT_DIR = Path(tmpdirname)
        mock_extract_root_idx.return_value = (expected_anns, expected_base)
        pecha = parser.parse(en_docx_file, metadata, OUTPUT_DIR)

        assert isinstance(pecha, Pecha)
