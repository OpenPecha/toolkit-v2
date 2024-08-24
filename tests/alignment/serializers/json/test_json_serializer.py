from pathlib import Path

from openpecha.alignment.alignment import Alignment
from openpecha.alignment.serializers.json import JSONSerializer
from openpecha.pecha import Pecha


def test_json_serializer():
    DATA = Path(__file__).parent / "data"

    alignment_path = DATA / "A84686EBF"

    alignment = Alignment.from_path(alignment_path)
    serializer = JSONSerializer(alignment)

    source_pecha = Pecha.from_path(DATA / "I79F4F48B")
    target_pecha = Pecha.from_path(DATA / "IF1FF2A77")

    serializer.load_pechas(source_pecha, target_pecha)


test_json_serializer()
