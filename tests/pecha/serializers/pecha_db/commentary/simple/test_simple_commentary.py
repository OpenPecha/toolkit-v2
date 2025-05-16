from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.utils import FormatPechaCategory
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
        pecha = Pecha.from_path(DATA_DIR / "bo/I6944984E")
        annotation_path = "E949/alignment-2F29.json"

        serializer = SimpleCommentarySerializer()

        root_title = "Entering the Middle Way Chapter 6, verses 1 to 64"
        formatted_category = FormatPechaCategory().format_commentary_category(
            pecha, self.pecha_category, root_title
        )
        serialized_json = serializer.serialize(
            pecha, annotation_path, formatted_category
        )
        expected_serialized_json = read_json(DATA_DIR / "bo/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def test_en_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/I6944984E")
        translation_pecha = Pecha.from_path(DATA_DIR / "en/I94DBDA91")

        annotation_path = "E949/alignment-2F29.json"
        translation_ann_path = "FD22/alignment-599A.json"

        serializer = SimpleCommentarySerializer()

        root_title = "Entering the Middle Way Chapter 6, verses 1 to 64"
        formatted_category = FormatPechaCategory().format_commentary_category(
            pecha, self.pecha_category, root_title
        )
        serialized_json = serializer.serialize(
            pecha,
            annotation_path,
            formatted_category,
            translation_pecha,
            translation_ann_path,
        )

        expected_serialized_json = read_json(DATA_DIR / "en/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def test_zh_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/I6944984E")
        translation_pecha = Pecha.from_path(DATA_DIR / "zh/I9A60B88D")

        annotation_path = "E949/alignment-2F29.json"
        translation_ann_path = "B97E/alignment-22A8.json"

        serializer = SimpleCommentarySerializer()

        root_title = "Entering the Middle Way Chapter 6, verses 1 to 64"
        formatted_category = FormatPechaCategory().format_commentary_category(
            pecha, self.pecha_category, root_title
        )
        serialized_json = serializer.serialize(
            pecha,
            annotation_path,
            formatted_category,
            translation_pecha,
            translation_ann_path,
        )
        expected_serialized_json = read_json(DATA_DIR / "zh/commentary_serialized.json")
        assert serialized_json == expected_serialized_json
