from pathlib import Path

from openpecha.alignment.serializers.simple_text_translation import (
    SimpleTextTranslationSerializer,
)


def test_simple_text_translation():
    DATA_DIR = Path(__file__).parent / "data"
    root_opf = DATA_DIR / "bo/I72825E94"
    translation_opf = DATA_DIR / "zh/IAE4B5DFE"
    OUTPUT_DIR = DATA_DIR / "output"

    serializer = SimpleTextTranslationSerializer()
    serializer.serialize(root_opf, translation_opf, OUTPUT_DIR)


test_simple_text_translation()
