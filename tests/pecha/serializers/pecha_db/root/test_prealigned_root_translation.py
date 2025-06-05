from pathlib import Path
from typing import Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.prealigned_root_translation import (
    PreAlignedRootTranslationSerializer,
)
from openpecha.utils import read_json

null = None


class TestPreAlignedRootTranslationSerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path("tests/alignment/translation_transfer/data")
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "root/I2B2E5268")
        self.translation_pecha = Pecha.from_path(
            self.DATA_DIR / "translation/I9248F287"
        )

        self.pecha_category: List[Dict] = [
            {
                "description": null,
                "short_description": null,
                "name": {
                    "en": "The Buddha's Teachings",
                    "bo": "སངས་རྒྱས་ཀྱི་བཀའ།",
                    "lzh": "佛陀教法",
                },
                "parent": null,
            },
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Vajra Cutter", "bo": "རྡོ་རྗེ་གཅོད་པ།", "lzh": "金刚经"},
                "parent": "the-buddha's-teachings",
            },
        ]

    def test_prealigned_root_translation_pecha(self):
        root_alignment_id = "44AC/alignment-148C.json"
        translation_alignment_id = "BE59/alignment-044E.json"

        serializer = PreAlignedRootTranslationSerializer()
        serialized_json = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.translation_pecha,
            translation_alignment_id,
            self.pecha_category,
        )
        expected_json = (
            Path(__file__).parent / "data/expected_prealigned_root_translation.json"
        )
        assert read_json(expected_json) == serialized_json

    def test_prealigned_root_translation_pecha_with_display(self):
        root_alignment_id = "44AC/alignment-148C.json"
        translation_alignment_id = "BE59/alignment-044E.json"
        translation_display_id = "BE59/segmentation-60A8.json"

        serializer = PreAlignedRootTranslationSerializer()
        serialized_json = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.translation_pecha,
            translation_alignment_id,
            self.pecha_category,
            translation_display_id,
        )
        expected_json = (
            Path(__file__).parent
            / "data/expected_prealigned_root_translation_with_display.json"
        )
        assert read_json(expected_json) == serialized_json
