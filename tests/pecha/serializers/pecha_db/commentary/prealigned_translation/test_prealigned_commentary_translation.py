from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary_translation import (
    PreAlignedCommentaryTranslationSerializer,
)
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
                "tests/pecha/serializers/pecha_db/commentary/prealigned_translation/data/en/I8A645565"
            )
        )

        root_alignment_id = "B8B3/alignment-F81A.json"
        commentary_alignment_id = "BEC3/alignment-90C0.json"
        translation_alignment_id = "757D/alignment-C2B5.json"

        serialized = serializer.serialize(
            self.root_pecha,
            root_alignment_id,
            self.commentary_pecha,
            commentary_alignment_id,
            translation_pecha,
            translation_alignment_id,
            self.pecha_category,
        )

        from openpecha.utils import write_json

        write_json("temp.json", serialized)
        pass
