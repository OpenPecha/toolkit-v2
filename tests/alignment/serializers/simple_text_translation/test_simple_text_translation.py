import tempfile
from pathlib import Path

from openpecha.alignment.serializers.simple_text_translation import (
    SimpleTextTranslationSerializer,
)
from openpecha.utils import read_json


def test_simple_text_translation():
    DATA_DIR = Path(__file__).parent / "data"
    root_opf = DATA_DIR / "bo/I72825E94"
    translation_opf = DATA_DIR / "zh/IAE4B5DFE"
    with tempfile.TemporaryDirectory() as tmpdirname:
        OUTPUT_DIR = Path(tmpdirname)

        serializer = SimpleTextTranslationSerializer()
        serialized_json_file = serializer.serialize(
            root_opf, translation_opf, OUTPUT_DIR
        )

        expected_json_output_file = DATA_DIR / "expected_serialized.json"
        assert read_json(serialized_json_file) == read_json(expected_json_output_file)


test_simple_text_translation()
