from pathlib import Path

from openpecha.pecha.serializers.pecha_db import PechaDBSerializer


def test_peydurma_pecha_db_serializer():
    output_path = Path(__file__).parent / "output"

    serializer = PechaDBSerializer(output_path=output_path)

    pecha_path = Path(__file__).parent / "data/I361DF300"
    serializer.serialize(pecha_path=pecha_path, source_type="pedurma")


test_peydurma_pecha_db_serializer()
