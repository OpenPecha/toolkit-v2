from pathlib import Path
from unittest import TestCase, mock

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary import (
    PreAlignedCommentarySerializer,
)
from openpecha.utils import read_json


class TestPreAlignedCommentarySerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path("tests/alignment/commentary_transfer/data")
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "P2/IC7760088")
        self.root_display_pecha = Pecha.from_path(self.DATA_DIR / "P1/IA6E66F92")
        self.commentary_pecha = Pecha.from_path(self.DATA_DIR / "P3/I77BD6EA9")

        self.expected_serialized_commentary = read_json(
            self.DATA_DIR / "expected_serialized_commentary.json"
        )

        # Create the patcher and set return_value
        self.pecha_category = {
            "bo": [
                {"name": "དབུ་མ།", "heDesc": "", "heShortDesc": ""},
                {"name": "དབུ་མ་ལ་འཇུག་པ།", "heDesc": "", "heShortDesc": ""},
            ],
            "en": [
                {"name": "Madhyamaka", "enDesc": "", "enShortDesc": ""},
                {"name": "Entering the Middle Way", "enDesc": "", "enShortDesc": ""},
            ],
        }

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary.CommentaryAlignmentTransfer.get_serialized_commentary",
    )
    def test_prealigned_commentary_pecha(self, mock_get_serialized_commentary):
        mock_get_serialized_commentary.return_value = (
            self.expected_serialized_commentary
        )

        serializer = PreAlignedCommentarySerializer()
        serialized_json = serializer.serialize(
            self.root_display_pecha,
            self.root_pecha,
            self.commentary_pecha,
            self.pecha_category,
        )

        expected_json = Path(__file__).parent / "data/expected_serialized.json"
        assert read_json(expected_json) == serialized_json
