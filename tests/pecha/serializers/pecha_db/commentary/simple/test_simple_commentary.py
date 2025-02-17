from pathlib import Path
from unittest import TestCase, mock

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"


class TestSimpleCommentarySerializer(TestCase):
    def setUp(self):
        # Create the patcher and set return_value
        self.patcher = mock.patch(
            "openpecha.pecha.serializers.commentary.simple_commentary.CategoryExtractor.get_category",
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

    def test_bo_commentary_serializer(self):
        pecha_path = DATA_DIR / "bo/I6944984E"

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(pecha_path, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "bo/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    @mock.patch(
        "openpecha.pecha.serializers.commentary.simple_commentary.get_pecha_with_id"
    )
    def test_en_commentary_serializer(self, mock_get_pecha_with_id):
        mock_get_pecha_with_id.return_value = Pecha.from_path(DATA_DIR / "bo/I6944984E")
        pecha_path = DATA_DIR / "en/I94DBDA91"

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(pecha_path, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "en/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    @mock.patch(
        "openpecha.pecha.serializers.commentary.simple_commentary.get_pecha_with_id"
    )
    def test_zh_commentary_serializer(self, mock_get_pecha_with_id):
        mock_get_pecha_with_id.return_value = Pecha.from_path(DATA_DIR / "bo/I6944984E")
        pecha_path = DATA_DIR / "zh/I9A60B88D"

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(pecha_path, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "zh/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def tearDown(self):
        # Stop the patch
        self.patcher.stop()


work = TestSimpleCommentarySerializer()
work.setUp()
# work.test_bo_commentary_serializer()
work.test_en_commentary_serializer()
# work.test_zh_commentary_serializer()
