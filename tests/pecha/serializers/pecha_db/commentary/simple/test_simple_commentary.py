from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.utils import read_json, write_json

DATA_DIR = Path(__file__).parent / "data"


class TestSimpleCommentarySerializer(TestCase):
    def setUp(self):
        self.pecha_category = {
            "bo": [
                {"name": "དབུ་མ།", "heDesc": "", "heShortDesc": ""},
                {"name": "དབུ་མ་ལ་འཇུག་པ།", "heDesc": "", "heShortDesc": ""},
            ],
            "en": [
                {"name": "Madhyamaka", "enDesc": "", "enShortDesc": ""},
                {"name": "Entering the Middle Way", "enDesc": "", "enShortDesc": ""},
            ],
        }

    def test_bo_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/I6944984E")

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(
            pecha,
            self.pecha_category,
            "Entering the Middle Way Chapter 6, verses 1 to 64",
        )
        write_json("bo_commentary_serialized.json", serialized_json)
        expected_serialized_json = read_json(DATA_DIR / "bo/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def test_en_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/I6944984E")
        translation_pecha = Pecha.from_path(DATA_DIR / "en/I94DBDA91")

        serializer = SimpleCommentarySerializer()
        serialized_json = serializer.serialize(
            pecha,
            self.pecha_category,
            "Entering the Middle Way Chapter 6, verses 1 to 64",
            translation_pecha,
        )
        write_json("en_commentary_serialized.json", serialized_json)

        expected_serialized_json = read_json(DATA_DIR / "en/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def test_zh_commentary_serializer(self):
        pecha = Pecha.from_path(DATA_DIR / "bo/I6944984E")
        translation_pecha = Pecha.from_path(DATA_DIR / "zh/I9A60B88D")

        serializer = SimpleCommentarySerializer()

        serialized_json = serializer.serialize(
            pecha,
            self.pecha_category,
            "Entering the Middle Way Chapter 6, verses 1 to 64",
            translation_pecha,
        )
        write_json("zh_commentary_serialized.json", serialized_json)
        expected_serialized_json = read_json(DATA_DIR / "zh/commentary_serialized.json")
        assert serialized_json == expected_serialized_json


if __name__ == "__main__":
    import unittest

    unittest.main()
