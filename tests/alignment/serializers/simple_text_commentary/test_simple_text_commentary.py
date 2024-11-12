from pathlib import Path

from openpecha.alignment.serializers.simple_text_commentary import (
    SimpleTextCommentarySerializer,
)


def test_simple_text_commentary_serializer():
    DATA_DIR = Path(__file__).parent / "data"
    root_opf_path = DATA_DIR / "root" / "IC537C534"
    commentary_opf_path = DATA_DIR / "commentary" / "IBDF9A009"

    serializer = SimpleTextCommentarySerializer()
    output_path = DATA_DIR / "output"
    serializer.serialize(root_opf_path, commentary_opf_path, output_path)


test_simple_text_commentary_serializer()
