from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary_translation import (
    PreAlignedCommentaryTranslationSerializer,
)
from openpecha.utils import read_json
from tests.pecha import SharedPechaSetup

null = None


class TestPreAlignedCommentaryTranslationSerializer(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()
        self.pecha_category: List[Dict[Any, Any]] = [
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

    def test_en_prealigned_commentary_translation_pecha(self):
        serializer = PreAlignedCommentaryTranslationSerializer()

        translation_pecha = Pecha.from_path(
            Path(
                "tests/pecha/serializers/pecha_db/commentary/prealigned_translation/data/en/IF5944957"
            )
        )

        root_alignment_id = "B5FE/segmentation-4FD1.json"
        commentary_alignment_id = "B014/alignment-2127.json"
        translation_alignment_id = "0DCE/alignment-8B56.json"

        serialized = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.commentary_pecha,
            commentary_alignment_id,
            translation_pecha,
            translation_alignment_id,
            self.pecha_category,
        )

        expected_serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/prealigned_translation/data/en/expected_serialized.json"
        )
        assert (
            serialized == expected_serialized
        ), "PreAlinged Commentary Translation failed for English.."

    def test_lzh_prealigned_commentary_translation_pecha(self):
        serializer = PreAlignedCommentaryTranslationSerializer()

        translation_pecha = Pecha.from_path(
            Path(
                "tests/pecha/serializers/pecha_db/commentary/prealigned_translation/data/lzh/IAE3E5BE4"
            )
        )

        root_alignment_id = "B5FE/segmentation-4FD1.json"
        commentary_alignment_id = "B014/alignment-2127.json"
        translation_alignment_id = "7A44/alignment-E02B.json"

        serialized = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.commentary_pecha,
            commentary_alignment_id,
            translation_pecha,
            translation_alignment_id,
            self.pecha_category,
        )

        expected_serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/prealigned_translation/data/lzh/expected_serialized.json"
        )
        assert (
            serialized == expected_serialized
        ), "PreAlinged Commentary Translation failed for Literal Chinese.."
