import shutil
from pathlib import Path

import pytest

from openpecha.pecha import Pecha


@pytest.fixture
def setup_temp_pecha(tmp_path):
    source = Path("tests/pecha/data/P0001")
    destination = tmp_path / "P0001"
    shutil.copytree(source, destination)
    return destination


def test_pecha_base_update(setup_temp_pecha):
    pecha = Pecha(path=setup_temp_pecha)
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
