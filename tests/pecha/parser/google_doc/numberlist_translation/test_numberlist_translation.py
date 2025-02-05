import tempfile
from pathlib import Path
from unittest.mock import patch

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.google_doc.numberlist_translation import DocxNumberListTranslationParser
from openpecha.pecha.parsers.parser_utils import extract_metadata_from_xlsx

DATA_DIR = Path(__file__).parent / "data"


def test_bo_google_doc_translation_parser():
    bo_docx_file = DATA_DIR / "entering_middle_way.docx"
    bo_metadata = DATA_DIR / "Tibetan Root text Translation Metadata.xlsx"

    parser = DocxNumberListTranslationParser()

    expected_anns = [
        {'Tibetan_Segment': {'start': 0, 'end': 42}, 'root_idx_mapping': '1'},
        {'Tibetan_Segment': {'start': 42, 'end': 201}, 'root_idx_mapping': '2'},
        {'Tibetan_Segment': {'start': 201, 'end': 354}, 'root_idx_mapping': '3'},
        {'Tibetan_Segment': {'start': 354, 'end': 501}, 'root_idx_mapping': '4'},
        {'Tibetan_Segment': {'start': 501, 'end': 668}, 'root_idx_mapping': '5'}
    ]
    expected_base = 'དབུ་མ་ལུ་འཇུག་པ་ལས། སེམས་བསྐྱེད་པ་དྲུག་པ།\nམངོན་དུ་ཕྱོགས་པར་མཉམ་བཞག་སེམས་གནས་ཏེ། །རྫོགས་པའི་སངས་རྒྱས་ཆོས་ལ་མངོན་ཕྱོགས་ཤིང༌། །འདི་བརྟེན་འབྱུང་བའི་དེ་ཉིད་མཐོང་བ་དེས། །ཤེས་རབ་གནས་པས་འགོག་པ་ཐོབ་པར་འགྱུར། །\nཇི་ལྟར་ལོང་བའི་ཚོགས་ཀུན་བདེ་བླག་ཏུ། །མིག་ལྡན་སྐྱེས་བུ་གཅིག་གིས་འདོད་པ་ཡི། །ཡུལ་དུ་འཁྲིད་པ་དེ་བཞིན་འདིར་ཡང་བློས། །མིག་ཉམས་ཡོན་ཏན་བླངས་ཏེ་རྒྱལ་ཉིད་འགྲོ། །\nཇི་ལྟར་དེ་ཡིས་ཆེས་ཟབ་ཆོས་རྟོགས་པ། །ལུང་དང་གཞན་ཡང་རིགས་པས་ཡིན་པས་ན། །དེ་ལྟར་འཕགས་པ་ཀླུ་སྒྲུབ་གཞུང་ལུགས་ལས། །ཇི་ལྟར་གནས་པའི་ལུགས་བཞིན་བརྗོད་པར་བྱ། །\nསོ་སོ་སྐྱེ་བོའི་དུས་ནའང་སྟོང་པ་ཉིད་ཐོས་ནས། །ནང་དུ་རབ་ཏུ་དགའ་བ་ཡང་དང་ཡང་དུ་འབྱུང༌། །རབ་ཏུ་དགའ་བ་ལས་བྱུང་མཆི་མས་མིག་བརླན་ཞིང༌། །ལུས་ཀྱི་བ་སྤུ་ལྡང་པར་འགྱུར་པ་གང་ཡིན་པ། །\n'
    metadata = extract_metadata_from_xlsx(bo_metadata)
    anns, base = parser.extract_root_segments_anns(bo_docx_file, metadata)

    assert (
        anns == expected_anns
    ), "Translation Parser failed parsing Root anns properly for bo data."
    assert (
        base == expected_base
    ), "Translation Parser failed preparing base text properly for bo data"

    with tempfile.TemporaryDirectory() as tmpdirname, patch(
        "openpecha.pecha.parsers.google_doc.numberlist_translation.DocxNumberListTranslationParser.extract_root_segments_anns"
    ) as mock_extract_root_idx:
        OUTPUT_DIR = Path(tmpdirname)
        mock_extract_root_idx.return_value = (expected_anns, expected_base)
        pecha = parser.parse(bo_docx_file, metadata, OUTPUT_DIR)

        assert isinstance(pecha, Pecha)

