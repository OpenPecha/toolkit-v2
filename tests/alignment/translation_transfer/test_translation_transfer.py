from pathlib import Path
from unittest import TestCase

from openpecha.alignment.translation_transfer import TranslationAlignmentTransfer
from openpecha.pecha import Pecha
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"


class TestTranslationAlignmentTransfer(TestCase):
    def setUp(self):
        self.root_pecha = Pecha.from_path(DATA_DIR / "P2/I73078576")
        self.root_display_pecha = Pecha.from_path(DATA_DIR / "P1/I15C4AA72")
        self.translation_pecha = Pecha.from_path(DATA_DIR / "P3/I4FA57826")

    def test_get_root_pechas_mapping(self):
        translation_transfer = TranslationAlignmentTransfer()
        mapping = translation_transfer.get_root_pechas_mapping(
            self.root_pecha, self.root_display_pecha
        )
        expected_mapping = {
            1: [1],
            2: [2],
            3: [3],
            4: [4],
            5: [5],
            6: [5],
            7: [6],
            8: [7, 8],
            9: [9],
            10: [10],
        }
        assert mapping == expected_mapping

    def test_get_serialized_translation(self):
        translation_transfer = TranslationAlignmentTransfer()
        serialized_json = translation_transfer.get_serialized_translation(
            self.root_pecha, self.root_display_pecha, self.translation_pecha
        )
        expected_serialized_json = read_json(DATA_DIR / "serialized_translation.json")
        assert serialized_json == expected_serialized_json


work = TestTranslationAlignmentTransfer()
work.setUp()
work.test_get_serialized_translation()
