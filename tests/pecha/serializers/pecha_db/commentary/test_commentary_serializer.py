from pathlib import Path

from openpecha.pecha.serializers.commentary import CommentarySerializer


def test_commentary_serializer():
    DATA_DIR = Path(__file__).parent / "data"
    pecha_path = DATA_DIR / "I1E88FE81"

    serializer = CommentarySerializer()
    serializer.serialize(pecha_path, source_type="commentary")
