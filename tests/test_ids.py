import re

from openpecha.ids import (
    get_alignment_id,
    get_annotation_id,
    get_base_id,
    get_collection_id,
    get_diplomatic_id,
    get_id,
    get_initial_pecha_id,
    get_layer_id,
    get_open_pecha_id,
    get_uuid,
    get_work_id,
)


def test_get_uuid():
    uuid = get_uuid()
    assert re.match(
        r"^[0-9a-fA-F]{32}$", uuid
    ), f"UUID {uuid} is not in the correct format"


def test_get_id():
    prefix = "T"
    length = 4
    generated_id = get_id(prefix, length)
    assert re.match(
        r"^T[0-9A-F]{4}$", generated_id
    ), f"ID {generated_id} is not in the correct format"


def test_get_base_id():
    base_id = get_base_id()
    assert re.match(
        r"^[0-9A-F]{4}$", base_id
    ), f"Base ID {base_id} is not in the correct format"


def test_get_layer_id():
    layer_id = get_layer_id()
    assert re.match(
        r"^[0-9A-F]{4}$", layer_id
    ), f"Layer ID {layer_id} is not in the correct format"


def test_get_initial_pecha_id():
    initial_pecha_id = get_initial_pecha_id()
    assert re.match(
        r"^I[0-9A-F]{8}$", initial_pecha_id
    ), f"Initial Pecha ID {initial_pecha_id} is not in the correct format"


def test_get_open_pecha_id():
    open_pecha_id = get_open_pecha_id()
    assert re.match(
        r"^O[0-9A-F]{8}$", open_pecha_id
    ), f"Open Pecha ID {open_pecha_id} is not in the correct format"


def test_get_diplomatic_id():
    diplomatic_id = get_diplomatic_id()
    assert re.match(
        r"^D[0-9A-F]{8}$", diplomatic_id
    ), f"Diplomatic ID {diplomatic_id} is not in the correct format"


def test_get_work_id():
    work_id = get_work_id()
    assert re.match(
        r"^W[0-9A-F]{8}$", work_id
    ), f"Work ID {work_id} is not in the correct format"


def test_get_alignment_id():
    alignment_id = get_alignment_id()
    assert re.match(
        r"^A[0-9A-F]{8}$", alignment_id
    ), f"Alignment ID {alignment_id} is not in the correct format"


def test_get_collection_id():
    collection_id = get_collection_id()
    assert re.match(
        r"^C[0-9A-F]{8}$", collection_id
    ), f"Collection ID {collection_id} is not in the correct format"


def test_get_annotation_id():
    ann_id = get_annotation_id()
    assert len(ann_id) == 8
