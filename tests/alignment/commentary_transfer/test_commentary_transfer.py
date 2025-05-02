from pathlib import Path
from unittest import TestCase

from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.pecha import Pecha
from openpecha.utils import read_json


class TestCommentaryAlignmentTransfer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "root/IA6E66F92")
        self.commentary_pecha = Pecha.from_path(self.DATA_DIR / "commentary/I77BD6EA9")

    def test_get_root_pechas_mapping(self):
        root_alignment_id = "B8B3/alignment-F81A.json"
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

    def test_get_commentary_pechas_mapping(self):
        commentary_alignment_id = "BEC3/alignment-90C0.json"
        commentary_segmentation_id = "BEC3/segmentation-0C09.json"

        serializer = CommentaryAlignmentTransfer()
        mapping = serializer.get_commentary_pechas_mapping(
            self.commentary_pecha, commentary_alignment_id, commentary_segmentation_id
        )
        expected_mapping = {
            1: [2],
            2: [2],
            3: [2],
            4: [4],
            5: [5],
            6: [5],
            7: [6],
            8: [6],
            9: [7],
            10: [8],
            11: [8],
            12: [9],
        }
        assert mapping == expected_mapping

    def test_get_serialized_commentary(self):
        root_alignment_id = "B8B3/alignment-F81A.json"
        commentary_alignment_id = "BEC3/alignment-90C0.json"

        serializer = CommentaryAlignmentTransfer()
        serialized_json = serializer.get_serialized_commentary(
            self.root_pecha,
            root_alignment_id,
            self.commentary_pecha,
            commentary_alignment_id,
        )

        expected_json = read_json(self.DATA_DIR / "expected_serialized_commentary.json")
        assert serialized_json == expected_json

    def tearDown(self):
        pass


work = TestCommentaryAlignmentTransfer()
work.setUp()

work.test_get_commentary_pechas_mapping()
