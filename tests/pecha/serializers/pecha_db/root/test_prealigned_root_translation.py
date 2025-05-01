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
        self.root_pecha = Pecha.from_path(self.DATA_DIR / "root/I15C4AA72")
        self.translation_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/translation/I4FA57826")
        )
        self.translation_pecha_with_display = Pecha.from_path(
            self.DATA_DIR / "translation/I4FA57826"
        )

        self.pecha_category: List[Dict] = [
            {
                "description": {"en": "", "bo": ""},
                "short_description": {"en": "", "bo": ""},
                "name": {"en": "The Buddha's Teachings", "bo": "སངས་རྒྱས་ཀྱི་བཀའ།"},
                "parent": null,
            },
            {
                "description": {"en": "", "bo": ""},
                "short_description": {"en": "", "bo": ""},
                "name": {"en": "Vajra Cutter", "bo": "རྡོ་རྗེ་གཅོད་པ།"},
                "parent": "the-buddha's-teachings",
            },
        ]

    def test_prealigned_root_translation_pecha(self):
        root_alignment_id = "A340/alignment-CCF1.json"
        translation_alignment_id = "AC0A/alignment-9048.json"

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
