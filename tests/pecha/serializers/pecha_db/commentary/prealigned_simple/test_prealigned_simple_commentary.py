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
        self.patcher = mock.patch(
            "openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary.PreAlignedCommentarySerializer.get_category",
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

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary.CommentaryAlignmentTransfer.get_serialized_commentary",
    )
    def test_serialize(self, mock_get_serialized_commentary):
        mock_get_serialized_commentary.return_value = (
            self.expected_serialized_commentary
        )

        serializer = PreAlignedCommentarySerializer()
        serialized_json = serializer.serialize(
            self.root_display_pecha, self.root_pecha, self.commentary_pecha
        )

        expected_json = Path(__file__).parent / "data/expected_serialized.json"
        assert read_json(expected_json) == serialized_json

    def tearDown(self):
        self.patcher.stop()
