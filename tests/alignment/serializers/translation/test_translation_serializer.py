from pathlib import Path
from unittest import TestCase

from openpecha.alignment.serializers.simple_text_translation import (
    SimpleTextTranslationSerializer,
)
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


class TestSimpleTextTranslationSerializer(TestCase):
    def test_translation_serializer(self):
        root_opf = DATA_DIR / "bo/IFA46BBC2"
        translation_opf = DATA_DIR / "en/I6EA29D09"

        serializer = SimpleTextTranslationSerializer()
        json_output = serializer.serialize(root_opf, translation_opf, OUTPUT_DIR)

        expected_json_path = DATA_DIR / "expected_output.json"
        assert read_json(json_output) == read_json(expected_json_path)
