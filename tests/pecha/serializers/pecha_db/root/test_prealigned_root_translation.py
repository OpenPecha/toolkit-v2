from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.prealigned_root_translation import (
    PreAlignedRootTranslationSerializer,
)
from openpecha.utils import read_json
null = None

class TestPreAlignedRootTranslationSerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path("tests/alignment/translation_transfer/data")
        self.root_display_pecha = Pecha.from_path(self.DATA_DIR / "P1/I15C4AA72")
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "P2/I73078576")
        self.translation_pecha = Pecha.from_path(self.DATA_DIR / "P3/I4FA57826")
        self.pecha_category = [
            {
                "description": {
                    "en": "",
                    "bo": ""
                },
                "short_description": {
                    "en": "",
                    "bo": ""
                },
                "name": {
                    "en": "The Buddha's Teachings",
                    "bo": "སངས་རྒྱས་ཀྱི་བཀའ།"
                },
                "parent": null
            },
            {
                "description": {
                    "en": "",
                    "bo": ""
                },
                "short_description": {
                    "en": "",
                    "bo": ""
                },
                "name": {
                    "en": "Vajra Cutter",
                    "bo": "རྡོ་རྗེ་གཅོད་པ།"
                },
                "parent": "the-buddha's-teachings"
            }
        ]

    def test_root_translation_pecha(self):
        serializer = PreAlignedRootTranslationSerializer()
        serialized_json = serializer.serialize(
            self.root_display_pecha,
            self.root_pecha,
            self.translation_pecha,
            self.pecha_category,
        )
        expected_json = (
            Path(__file__).parent / "data/expected_prealigned_root_translation.json"
        )
        assert read_json(expected_json) == serialized_json


