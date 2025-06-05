from pathlib import Path
from unittest import TestCase

from openpecha.alignment.translation_transfer import TranslationAlignmentTransfer
from openpecha.pecha import Pecha
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"


class TestTranslationAlignmentTransfer(TestCase):
    def setUp(self):
        self.root_pecha = Pecha.from_path(DATA_DIR / "root/I2B2E5268")
        self.translation_pecha = Pecha.from_path(DATA_DIR / "translation/I5B9200FF")

    def test_get_root_pechas_mapping(self):

        root_alignment_id = "44AC/alignment-148C.json"
        translation_transfer = TranslationAlignmentTransfer()
        mapping = translation_transfer.get_root_pechas_mapping(
            self.root_pecha, root_alignment_id
        )
        expected_mapping = {
            1: [1],
            2: [2],
            3: [3],
            4: [4],
            5: [5],
            6: [5],
            7: [6],
            8: [7],
            9: [8],
            10: [9],
            11: [10],
        }
        assert mapping == expected_mapping

    def test_get_translation_pechas_mapping(self):
        translation_alignment_id = "AC0A/alignment-9048.json"
        translation_segmentation_id = "AC0A/segmentation-E0A6.json"

        translation_transfer = TranslationAlignmentTransfer()
        mapping = translation_transfer.get_translation_pechas_mapping(
            self.translation_pecha,
            translation_alignment_id,
            translation_segmentation_id,
        )
        expected_mapping = {
            1: [1, 2],
            2: [3],
            3: [4, 5],
            4: [6],
            5: [7],
            6: [8],
            7: [9],
            8: [10],
        }
        assert mapping == expected_mapping

    def test_get_serialized_translation_alignment(self):
        root_alignment_id = "A340/alignment-CCF1.json"
        translation_alignment_id = "AC0A/alignment-9048.json"

        translation_transfer = TranslationAlignmentTransfer()
        serialized_json = translation_transfer.get_serialized_translation_alignment(
            self.root_pecha,
            root_alignment_id,
            self.translation_pecha,
            translation_alignment_id,
        )
        expected_serialized_json = read_json(DATA_DIR / "serialized_translation.json")
        assert serialized_json == expected_serialized_json

    def test_get_serialized_translation_segmentation(self):
        root_alignment_id = "A340/alignment-CCF1.json"
        translation_alignment_id = "AC0A/alignment-9048.json"
        translation_segmentation_id = "AC0A/segmentation-E0A6.json"

        translation_transfer = TranslationAlignmentTransfer()
        serialized_json = translation_transfer.get_serialized_translation_segmentation(
            self.root_pecha,
            root_alignment_id,
            self.translation_pecha,
            translation_alignment_id,
            translation_segmentation_id,
        )
        expected_serialized_json = read_json(
            DATA_DIR / "expected_serialized_translation_with_display.json"
        )
        assert serialized_json == expected_serialized_json
