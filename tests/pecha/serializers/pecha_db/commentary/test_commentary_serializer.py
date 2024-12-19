from pathlib import Path
from unittest.mock import patch

from openpecha.pecha.serializers.commentary import CommentarySerializer
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"


def test_bo_commentary_serializer():
    pecha_path = DATA_DIR / "bo/I0EB9B939"

    # Patch the `get_category` method in `CategoryExtractor` to return a custom value
    with patch(
        "openpecha.pecha.serializers.commentary.CategoryExtractor.get_category"
    ) as mock_get_category, patch(
        "openpecha.pecha.serializers.commentary.get_en_content_translation"
    ) as mock_get_en_translation:
        mock_get_category.return_value = {
            "bo": [
                {"name": "སངས་རྒྱས་ཀྱི་བཀའ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "འགྲེལ་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
            ],
            "en": [
                {"name": "The Buddha's Teachings", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
                {"name": "Commentaries", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
            ],
        }
        mock_get_en_translation.return_value = {
            "Commentary on the Structure of the Sutra": {
                "data": [],
                "Demonstrating the Unbroken Lineage of the Buddha": {"data": []},
                "Demonstrating the Characteristics of Diligent Application": {
                    "data": []
                },
                "Demonstrating the Basis of the Characteristics of Intense Application": {
                    "data": []
                },
            }
        }

        serializer = CommentarySerializer()
        serialized_json = serializer.serialize(pecha_path, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "bo/commentary_serialized.json")
        assert serialized_json == expected_serialized_json


def test_en_commentary_serializer():
    pecha_path = DATA_DIR / "en/I088F7504"

    # Patch the `get_category` method in `CategoryExtractor` to return a custom value
    with patch(
        "openpecha.pecha.serializers.commentary.CategoryExtractor.get_category"
    ) as mock_get_category, patch(
        "openpecha.pecha.serializers.commentary.get_en_content_translation"
    ) as mock_get_bo_translation:
        mock_get_category.return_value = {
            "bo": [
                {"name": "སངས་རྒྱས་ཀྱི་བཀའ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "འགྲེལ་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
            ],
            "en": [
                {"name": "The Buddha's Teachings", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
                {"name": "Commentaries", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
            ],
        }

        mock_get_bo_translation.return_value = {
            "མདོའི་གཞུང་གི་འགྲེལ་བཤད།": {
                "data": [],
                "སངས་རྒྱས་ཀྱི་མཐར་ཐུག་གི་ཡེ་ཤེས་རྒྱུན་མི་ཆད་པའི་བསྟན་པ།": {"data": []},
            }
        }

        serializer = CommentarySerializer()
        serialized_json = serializer.serialize(pecha_path, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "en/commentary_serialized.json")
        assert serialized_json == expected_serialized_json


def test_zh_commentary_serializer():
    pecha_path = DATA_DIR / "zh/I8BCEC781"

    # Patch the `get_category` method in `CategoryExtractor` to return a custom value
    with patch(
        "openpecha.pecha.serializers.commentary.CategoryExtractor.get_category"
    ) as mock_get_category, patch(
        "openpecha.pecha.serializers.commentary.get_en_content_translation"
    ) as mock_get_bo_translation:
        mock_get_category.return_value = {
            "bo": [
                {"name": "སངས་རྒྱས་ཀྱི་བཀའ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "འགྲེལ་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
            ],
            "en": [
                {"name": "The Buddha's Teachings", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
                {"name": "Commentaries", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
            ],
        }

        mock_get_bo_translation.return_value = {
            "སྔོན་གླེང་།": {"data": []},
            "བཞི། མདོ་འདིའི་སྒྲིག་གཞི།": {
                "data": [],
                "ལྔ་པ། མདོ་འདིའི་ལོ་ཙཱ་བ།": {
                    "data": [],
                    "ལྔ་པ། མདོ་འདིའི་ལོ་ཙཱ་བ།": {"data": []},
                },
            },
            "དྲུག་པ། མདོ་འདིའི་འགྲེལ་བཤད་བྱེད་མཁན།": {"data": []},
        }

        serializer = CommentarySerializer()
        serialized_json = serializer.serialize(pecha_path, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "zh/commentary_serialized.json")
        assert serialized_json == expected_serialized_json
