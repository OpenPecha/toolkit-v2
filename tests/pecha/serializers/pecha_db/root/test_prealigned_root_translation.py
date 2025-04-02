from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.prealigned_root_translation import (
    PreAlignedRootTranslationSerializer,
)
from openpecha.utils import read_json


class TestPreAlignedRootTranslationSerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path("tests/alignment/translation_transfer/data")
        self.root_display_pecha = Pecha.from_path(self.DATA_DIR / "P1/I15C4AA72")
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "P2/I73078576")
        self.translation_pecha = Pecha.from_path(self.DATA_DIR / "P3/I4FA57826")

        self.pecha_category = {
            "bo": [
                {"name": "སངས་རྒྱས་ཀྱི་བཀའ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
            ],
            "en": [
                {"name": "The Buddha's Teachings", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
            ],
        }

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


if __name__ == "__main__":
    import unittest

    unittest.main()
