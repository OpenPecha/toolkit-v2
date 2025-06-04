from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"
null = None


class TestSimpleCommentarySerializer(TestCase):
    def setUp(self):

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

    def test_bo_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/IDD1DF976")
        annotation_path = "1DFE/alignment-ADAA.json"

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(
            pecha,
            annotation_path,
            self.pecha_category,
            "Entering the Middle Way Chapter 6, verses 1 to 64",
        )
        expected_serialized_json = read_json(DATA_DIR / "bo/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def test_en_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/IDD1DF976")
        translation_pecha = Pecha.from_path(DATA_DIR / "en/ICFCF1CDC")

        annotation_path = "1DFE/alignment-ADAA.json"
        translation_ann_path = "EB60/alignment-6786.json"

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(
            pecha,
            annotation_path,
            self.pecha_category,
            "Entering the Middle Way Chapter 6, verses 1 to 64",
            translation_pecha,
            translation_ann_path,
        )

        expected_serialized_json = read_json(DATA_DIR / "en/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def test_zh_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/IDD1DF976")
        translation_pecha = Pecha.from_path(DATA_DIR / "zh/IC5697AEF")

        annotation_path = "1DFE/alignment-ADAA.json"
        translation_ann_path = "2AC8/alignment-F721.json"

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(
            pecha,
            annotation_path,
            self.pecha_category,
            "Entering the Middle Way Chapter 6, verses 1 to 64",
            translation_pecha,
            translation_ann_path,
        )
        expected_serialized_json = read_json(DATA_DIR / "zh/commentary_serialized.json")
        assert serialized_json == expected_serialized_json
