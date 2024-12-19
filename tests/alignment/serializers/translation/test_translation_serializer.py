from pathlib import Path
from unittest import TestCase

from openpecha.alignment.serializers.simple_text_translation import (
    SimpleTextTranslationSerializer,
)

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


class TestTranslationSerializer(TestCase):
    def setUp(self):
        pass

    def serialize(self):
        root_opf = DATA_DIR / "bo/IFA46BBC2"
        translation_opf = DATA_DIR / "en/I6EA29D09"

        serializer = SimpleTextTranslationSerializer()
        serializer.serialize(root_opf, translation_opf, OUTPUT_DIR)

    def tearDown(self):
        pass


TestTranslationSerializer().serialize()
