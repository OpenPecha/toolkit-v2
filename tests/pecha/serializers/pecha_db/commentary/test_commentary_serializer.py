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
    ) as mock_get_category:
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

        serializer = CommentarySerializer()
        serialized_json = serializer.serialize(pecha_path, "རྡོ་རྗེ་གཅོད་པ།")

        expected_serialized_json = read_json(DATA_DIR / "commentary_serialized.json")
        assert serialized_json == expected_serialized_json
