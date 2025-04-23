from pathlib import Path
from unittest import TestCase

from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.pecha import Pecha
from openpecha.utils import read_json


class TestCommentaryAlignmentTransfer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        # self.root_pecha = Pecha.from_path(self.DATA_DIR / "P2/IC7760088")
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "P1/IA6E66F92")
        self.commentary_pecha = Pecha.from_path(self.DATA_DIR / "P3/I77BD6EA9")

    def test_get_root_pechas_mapping(self):
        root_alignment_id = "B8B3/Alignment-F81A.json"
        serializer = CommentaryAlignmentTransfer()
        mapping = serializer.get_root_pechas_mapping(self.root_pecha, root_alignment_id)
        expected_mapping = {
            1: [1],
            2: [2],
            3: [3],
            4: [4, 5],
            5: [5],
            6: [6, 7],
            7: [7],
            8: [8],
            9: [8],
            10: [9],
        }
        assert mapping == expected_mapping

    def test_get_serialized_commentary(self):
        serializer = CommentaryAlignmentTransfer()
        serialized_json = serializer.get_serialized_commentary(
            self.root_display_pecha, self.root_pecha, self.commentary_pecha
        )

        expected_json = self.DATA_DIR / "expected_serialized_commentary.json"
        assert read_json(expected_json) == serialized_json

    def tearDown(self):
        pass
