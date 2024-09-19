import shutil
from pathlib import Path

import pytest

from openpecha.pecha import StamPecha


@pytest.fixture
def temp_data(tmp_path):
    source = Path("tests/pecha/data")
    destination = tmp_path / "data"
    shutil.copytree(source, destination)
    return destination


def test_pecha_base_update(temp_data):
    pecha = StamPecha(path=temp_data / "P0001")
    base_name = "0001"
    new_base = "00123456789"
    old_layers = list(pecha.get_layers(base_name))

    assert pecha.get_base(base_name) != new_base

    pecha.update_base(base_name, new_base)

    assert pecha.get_base(base_name) == new_base

    new_layers = list(pecha.get_layers(base_name))

    for (_, old_layer), (_, new_layer) in zip(old_layers, new_layers):
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

    source_pecha = StamPecha(source_pecha_path)
    target_pecha = StamPecha(target_pecha_path)

    source_base = source_pecha.get_base(source_base_name)
    target_base = target_pecha.get_base(target_base_name)

    assert source_base != target_base
    target_pre_merge_n_layers = len(list(target_pecha.get_layers(target_base_name)))
    source_n_layers = len(list(source_pecha.get_layers(source_base_name)))

    pecha = StamPecha(source_pecha_path)
    target_pecha.merge_pecha(pecha, source_base_name, target_base_name)

    target_post_merge_n_layers = len(list(target_pecha.get_layers(target_base_name)))

    assert target_post_merge_n_layers == target_pre_merge_n_layers + source_n_layers

    """ clean up"""
    target_new_post_layer_path = (
        Path(__file__).parent / "data" / "P0001" / "layers" / "0001" / "pos-a222.json"
    )
    if target_new_post_layer_path.exists():
        target_new_post_layer_path.unlink()


test_pecha_merge(Path(__file__).parent / "data")
