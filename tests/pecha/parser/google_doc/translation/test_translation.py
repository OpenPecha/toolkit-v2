from pathlib import Path

from openpecha.pecha.parsers.google_doc.translation import GoogleDocTranslationParser

DATA_DIR = Path(__file__).parent / "data"


def test_translation():
    bo_docx_file = DATA_DIR / "Tibetan Root text Translation .docx"
    en_docx_file = DATA_DIR / "English aligned Root Text Translation.docx"  # noqa
    zh_docx_file = DATA_DIR / "Chinese aligned Root Text Translation.docx"  # noqa

    parser = GoogleDocTranslationParser()
    parser.parse(
        input=bo_docx_file,
        metadata={"title": "Dummy Title"},
        output_path=(DATA_DIR / "output"),
    )
    pass


test_translation()
