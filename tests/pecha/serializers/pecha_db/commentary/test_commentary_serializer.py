from pathlib import Path

from openpecha.pecha.serializers.commentary import CommentarySerializer


def test_commentary_serializer():
    DATA_DIR = Path(__file__).parent / "data"
    pecha_path = DATA_DIR / "IC3797777"

    serializer = CommentarySerializer()
    serializer.serialize(pecha_path, title="test")


test_commentary_serializer()
