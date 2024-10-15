import tempfile
from pathlib import Path

from openpecha.pecha.serializers.pecha_db import PechaDBSerializer
from openpecha.utils import read_json


def test_pecha_db_serializer():
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        serializer = PechaDBSerializer(output_path=output_path)
        pecha_path = Path("tests/pecha/serializers/pecha_db/data/IB1A4B480")
        pecha_db_json_path, mapping_json_path = serializer.serialize(
            pecha_path=pecha_path
        )
        assert read_json(pecha_db_json_path) == read_json(
            "tests/pecha/serializers/pecha_db/data/expected_pecha_db.json"
        )
        assert read_json(mapping_json_path) == read_json(
            "tests/pecha/serializers/pecha_db/data/expected_mapping.json"
        )
