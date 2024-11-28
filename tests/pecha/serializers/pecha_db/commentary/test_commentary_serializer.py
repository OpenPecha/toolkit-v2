from pathlib import Path

from openpecha.pecha.serializers.commentary import CommentarySerializer
from openpecha.utils import read_json


def test_commentary_serializer():
    DATA_DIR = Path(__file__).parent / "data"
    pecha_path = DATA_DIR / "IC3797777"

    serializer = CommentarySerializer()
    serialized_json = serializer.serialize(pecha_path, "རྡོ་རྗེ་གཅོད་པ།")

    expected_serialized_json = read_json(DATA_DIR / "commentary_serialized.json")
    assert serialized_json == expected_serialized_json


test_commentary_serializer()
