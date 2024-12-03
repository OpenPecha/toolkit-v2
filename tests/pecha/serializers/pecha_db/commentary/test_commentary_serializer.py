from pathlib import Path
from unittest.mock import patch

from openpecha.pecha.serializers.commentary import CommentarySerializer
from openpecha.utils import read_json


def test_commentary_serializer():
    DATA_DIR = Path(__file__).parent / "data"
    pecha_path = DATA_DIR / "IC3797777"

    # Patch the `get_category` method in `CategoryExtractor` to return a custom value
    with patch(
        "pecha_org_tools.extract.CategoryExtractor.get_category"
    ) as mock_get_category, patch(
        "openpecha.pecha.serializers.commentary.CommentarySerializer.get_en_content_translation"
    ) as mock_get_en_content:
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
        mock_get_en_content.return_value = {
            "Commentary on the Structure of the Sutra": {
                "data": [],
                "The Unbroken Lineage of Buddha's Teachings": {"data": []},
            },
            "Explanation of the Meaning of Words": {
                "data": [],
                "The Unbroken Lineage of Buddha's Teachings": {"data": []},
            },
        }

        serializer = CommentarySerializer()
        serialized_json = serializer.serialize(
            pecha_path, "རྡོ་རྗེ་གཅོད་པ།", "རྡོ་རྗེ་གཅོད་པ།", "Diamond Cutter Sutra"
        )

        expected_serialized_json = read_json(DATA_DIR / "commentary_serialized.json")
        assert serialized_json == expected_serialized_json
