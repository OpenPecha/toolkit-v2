from pathlib import Path
from unittest import TestCase, mock

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

        # Create the patcher and set return_value
        self.patcher = mock.patch(
            "openpecha.pecha.serializers.pecha_db.prealigned_root_translation.PreAlignedRootTranslationSerializer.get_pecha_category",
            return_value={
                "bo": [
                    {"name": "སངས་རྒྱས་ཀྱི་བཀའ།", "heDesc": "", "heShortDesc": ""},
                    {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
                    {"name": "འགྲེལ་པ།", "heDesc": "", "heShortDesc": ""},
                    {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
                ],
                "en": [
                    {"name": "The Buddha's Teachings", "enDesc": "", "enShortDesc": ""},
                    {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
                    {"name": "Commentaries", "enDesc": "", "enShortDesc": ""},
                    {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
                ],
            },
        )
        # Start the patch
        self.mock_get_category = self.patcher.start()

    def test_root_translation_pecha(self):
        serializer = PreAlignedRootTranslationSerializer()
        serialized_json = serializer.serialize(
            self.root_display_pecha, self.root_pecha, self.translation_pecha
        )

        expected_json = (
            Path(__file__).parent / "data/expected_prealigned_root_translation.json"
        )
        assert read_json(expected_json) == serialized_json

    def tearDown(self):
        self.patcher.stop()


work = TestPreAlignedRootTranslationSerializer()
work.setUp()
work.test_root_translation_pecha()
