from pathlib import Path

from openpecha.pecha.parsers.google_doc.translation import GoogleDocTranslationParser

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


def test_translation():
    bo_docx_file = DATA_DIR / "bo" / "Tibetan Root text Translation .docx"
    bo_metadata = DATA_DIR / "bo" / "Tibetan Root text Translation Metadata.xlsx"

    en_docx_file = DATA_DIR / "English aligned Root Text Translation.docx"  # noqa
    zh_docx_file = DATA_DIR / "Chinese aligned Root Text Translation.docx"  # noqa

    parser = GoogleDocTranslationParser()
    parser.parse(
        input=bo_docx_file,
        metadata=bo_metadata,
        output_path=OUTPUT_DIR,
    )
    pass


test_translation()
