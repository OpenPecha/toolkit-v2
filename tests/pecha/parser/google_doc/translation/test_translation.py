from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.google_doc.translation import GoogleDocTranslationParser

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


def test_google_doc_translation_parser():
    bo_docx_file = DATA_DIR / "bo" / "Tibetan Root text Translation .docx"
    bo_metadata = DATA_DIR / "bo" / "Tibetan Root text Translation Metadata.xlsx"

    en_docx_file = DATA_DIR / "English aligned Root Text Translation.docx"  # noqa
    zh_docx_file = DATA_DIR / "Chinese aligned Root Text Translation.docx"  # noqa

    parser = GoogleDocTranslationParser()
    pecha = parser.parse(
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
