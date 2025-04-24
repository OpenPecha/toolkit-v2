from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.updated_opf_serializer import (
    update_serialize_json,
)
from openpecha.utils import read_json

MetadataType = Dict[str, str | Dict[str, str] | List[str] | None]

extra_fields: Dict[str, str | Dict[str, str] | List[str] | None] = {
    "author": {"en": "DPO and Claude-3-5-sonnet-20241022"},
    "document_id": "1vgnfCQH3yaWPDaMDFXT_5GhlG0M9kEra0mxkDX46VLE",
    "language": "en",
    "long_title": {
        "en": "Illuminating the Intent Chapter 6, verses 1 to 64 Literal Translation, Monlam AI, February 2025"
    },
    "title": {
        "bo": "མངོན་དུ་ཕྱོགས་པར་མཉམ་བཞག་སེམས་གནས་ཏེ།",
        "en": "Illuminating the Intent Chapter 6",
    },
    "usage_title": {"en": "Illuminating the Intent Chapter 6"},
}


def test_updated_commentary_translation_serializer():
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
    metadatas: list[MetadataType] = [
        {
            "translation_of": "P0001",
            "commentary_of": None,
            "version_of": None,
            **extra_fields,
        },
        {
            "translation_of": None,
            "commentary_of": "P0002",
            "version_of": None,
            **extra_fields,
        },
        {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **extra_fields,
        },
    ]
    pecha = Pecha.from_path(pecha_path)
    updated_commentary_json = update_serialize_json(
        pecha=pecha, metadatas=metadatas, json=old_commentary_json
    )

    assert expected_commentary_json == updated_commentary_json


def test_updated_root_translation_serializer():
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
    metadatas: list[MetadataType] = [
        {
            "translation_of": "P0001",
            "commentary_of": None,
            "version_of": None,
            **extra_fields,
        },
        {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **extra_fields,
        },
    ]
    pecha = Pecha.from_path(pecha_path)

    updated_root_json = update_serialize_json(
        pecha=pecha, metadatas=metadatas, json=old_root_json
    )

    assert expected_root_json == updated_root_json
