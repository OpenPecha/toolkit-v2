from pathlib import Path
from typing import Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.prealigned_root_translation import (
    PreAlignedRootTranslationSerializer,
)
from openpecha.pecha.serializers.pecha_db.utils import FormatPechaCategory
from openpecha.utils import read_json

null = None


class TestPreAlignedRootTranslationSerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path("tests/alignment/translation_transfer/data")
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "root/I15C4AA72")
        self.translation_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/translation/I4FA57826")
        )
        self.translation_pecha_with_display = Pecha.from_path(
            self.DATA_DIR / "translation/I4FA57826"
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
        root_alignment_id = "A340/alignment-CCF1.json"
        translation_alignment_id = "AC0A/alignment-9048.json"

        formatted_category = FormatPechaCategory().format_root_category(
            self.root_pecha, self.pecha_category
        )
        serializer = PreAlignedRootTranslationSerializer()
        serialized_json = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.translation_pecha,
            translation_alignment_id,
            formatted_category,
        )
        expected_json = (
            Path(__file__).parent / "data/expected_prealigned_root_translation.json"
        )
        assert read_json(expected_json) == serialized_json

    def test_prealigned_root_translation_pecha_with_display(self):
        root_alignment_id = "A340/alignment-CCF1.json"
        translation_alignment_id = "AC0A/alignment-9048.json"
        translation_display_id = "AC0A/segmentation-E0A6.json"

        formatted_category = FormatPechaCategory().format_root_category(
            self.root_pecha, self.pecha_category
        )

        serializer = PreAlignedRootTranslationSerializer()
        serialized_json = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.translation_pecha_with_display,
            translation_alignment_id,
            formatted_category,
            translation_display_id,
        )
        expected_json = (
            Path(__file__).parent
            / "data/expected_prealigned_root_translation_with_display.json"
        )
        assert read_json(expected_json) == serialized_json
