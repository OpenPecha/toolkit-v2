import shutil
from pathlib import Path

import pytest

from openpecha.pecha import Pecha


@pytest.fixture
def temp_data(tmp_path):
    source = Path("tests/pecha/data")
    destination = tmp_path / "data"
    shutil.copytree(source, destination)
    return destination


def test_pecha_base_update(temp_data):
    pecha = Pecha(path=temp_data / "P0001")
    base_name = "0001"
    new_base = "00123456789"
    old_layers = list(pecha.get_layers(base_name))

    assert pecha.get_base(base_name) != new_base

    pecha.update_base(base_name, new_base)

    assert pecha.get_base(base_name) == new_base

    new_layers = list(pecha.get_layers(base_name))

    for old_layer, new_layer in zip(old_layers, new_layers):
        for old_ann, new_ann in zip(old_layer.annotations(), new_layer.annotations()):
            old_ann_begin = old_ann.offset().begin().value()
            old_ann_end = old_ann.offset().end().value()
            new_ann_begin = new_ann.offset().begin().value()
            new_ann_end = new_ann.offset().end().value()

            assert new_ann_begin == old_ann_begin + 1
            assert new_ann_end == old_ann_end + 1


def test_pecha_merge(temp_data):
    source_pecha_path = Path(temp_data / "P0002")
    target_pecha_path = Path(temp_data / "P0001")
    source_base_name = "0002"
    target_base_name = "0001"

    source_pecha = Pecha(source_pecha_path)
    target_pecha = Pecha(target_pecha_path)

    source_base = source_pecha.get_base(source_base_name)
    target_base = target_pecha.get_base(target_base_name)

    assert source_base != target_base

    target_pecha.merge_pecha(source_pecha_path, source_base_name, target_base_name)

    source_base = source_pecha.get_base(source_base_name)
    target_base = target_pecha.get_base(target_base_name)

    assert source_base == target_base
