import tempfile
from pathlib import Path

from openpecha.pecha.serializers.pecha_db import PechaDBSerializer
from openpecha.utils import read_json


def test_peydurma_pecha_db_serializer():
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)

        serializer = PechaDBSerializer(output_path=output_path)

        pecha_path = Path(__file__).parent / "data/I361DF300"
        pecha_json_path = serializer.serialize(
            pecha_path=pecha_path, source_type="pedurma"
        )
        pecha_json = read_json(pecha_json_path)

        expected_pecha_json = read_json(
            Path(__file__).parent / "data/expected_pecha_db.json"
        )
        assert expected_pecha_json == pecha_json


test_peydurma_pecha_db_serializer()
