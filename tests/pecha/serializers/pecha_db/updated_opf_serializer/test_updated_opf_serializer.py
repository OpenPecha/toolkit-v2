from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.updated_opf_serializer import (
    UpdatedCommentarySerializer,
    UpdatedRootSerializer,
)
from openpecha.utils import read_json


def test_updated_commentary_serializer():
    pecha_id = "IB0D3B88B"
    expected_commentary_json = read_json(
        Path(
            f"tests/pecha/serializers/pecha_db/updated_opf_serializer/data/expected_{pecha_id}.json"
        )
    )
    old_commentary_json = read_json(
        Path(
            f"tests/pecha/serializers/pecha_db/updated_opf_serializer/data/old_{pecha_id}.json"
        )
    )
    pecha_path = Path(
        f"tests/pecha/serializers/pecha_db/updated_opf_serializer/data/{pecha_id}"
    )
    pecha = Pecha.from_path(pecha_path)
    updated_commentary_json = UpdatedCommentarySerializer().update_json(
        pecha=pecha, commentary_json=old_commentary_json
    )

    assert expected_commentary_json == updated_commentary_json


def test_updated_root_serializer():
    pecha_id = "I99491BA1"
    expected_root_json = read_json(
        Path(
            f"tests/pecha/serializers/pecha_db/updated_opf_serializer/data/expected_{pecha_id}.json"
        )
    )
    old_root_json = read_json(
        Path(
            f"tests/pecha/serializers/pecha_db/updated_opf_serializer/data/old_{pecha_id}.json"
        )
    )
    pecha_path = Path(
        f"tests/pecha/serializers/pecha_db/updated_opf_serializer/data/{pecha_id}"
    )
    pecha = Pecha.from_path(pecha_path)

    updated_root_json = UpdatedRootSerializer().update_json(
        pecha=pecha, root_json=old_root_json
    )

    assert expected_root_json == updated_root_json
