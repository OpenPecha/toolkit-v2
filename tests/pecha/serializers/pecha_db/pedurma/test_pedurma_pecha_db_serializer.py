from pathlib import Path

from openpecha.pecha.serializers.pecha_db.pecha_db import PechaDBSerializer
from openpecha.utils import read_json


def test_peydurma_pecha_db_serializer():
    serializer = PechaDBSerializer()

    pecha_path = Path(__file__).parent / "data/I361DF300"
    pecha_json = serializer.serialize(pecha_path=pecha_path, source_type="pedurma")

    expected_pecha_json = read_json(
        Path(__file__).parent / "data/expected_pecha_db.json"
    )
    assert expected_pecha_json == pecha_json
