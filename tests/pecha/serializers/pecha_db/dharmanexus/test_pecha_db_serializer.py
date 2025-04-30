from pathlib import Path

from openpecha.pecha.serializers.pecha_db.pecha_db import PechaDBSerializer
from openpecha.utils import read_json


def test_pecha_db_serializer():
    serializer = PechaDBSerializer()
    pecha_path = Path("tests/pecha/serializers/pecha_db/dharmanexus/data/I08D84584")
    source_type = "dharmanexus"
    pecha_db_json, mapping_json = serializer.serialize(
        pecha_path=pecha_path,
        source_type=source_type,
    )
    assert pecha_db_json == read_json(
        "tests/pecha/serializers/pecha_db/dharmanexus/data/expected_pecha_db.json"
    )
    assert mapping_json == read_json(
        "tests/pecha/serializers/pecha_db/dharmanexus/data/expected_mapping.json"
    )
