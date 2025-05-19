from pathlib import Path
from unittest import TestCase, mock

from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary import (
    PreAlignedCommentarySerializer,
)
from openpecha.utils import read_json
from tests.pecha import SharedPechaSetup

null = None


class TestPreAlignedCommentarySerializer(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()

        self.DATA_DIR = Path("tests/alignment/commentary_transfer/data")
        self.expected_serialized_commentary = read_json(
            self.DATA_DIR / "expected_serialized_commentary.json"
        )

        # Create the patcher and set return_value
        self.pecha_category = [
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Madhyamaka", "bo": "དབུ་མ།", "lzh": "中观"},
                "parent": null,
            },
            {
                "description": null,
                "short_description": null,
                "name": {
                    "en": "Entering the Middle Way",
                    "bo": "དབུ་མ་ལ་འཇུག་པ།",
                    "lzh": "入中论",
                },
                "parent": "madhyamaka",
            },
        ]

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary.CommentaryAlignmentTransfer.get_serialized_commentary",
    )
    def test_prealigned_commentary_pecha(self, mock_get_serialized_commentary):
        mock_get_serialized_commentary.return_value = (
            self.expected_serialized_commentary
        )

        root_alignment_id = "B8B3/Alignment-F81A.json"
        commentary_alignment_id = "BEC3/Alignment-90C0.json"

        serializer = PreAlignedCommentarySerializer()
        serialized_json = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.commentary_pecha,
            commentary_alignment_id,
            self.pecha_category,
        )

        expected_json = Path(__file__).parent / "data/expected_serialized.json"
        assert read_json(expected_json) == serialized_json
