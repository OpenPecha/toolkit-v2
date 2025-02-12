import shutil
from pathlib import Path

import pytest

from openpecha.pecha import Pecha


@pytest.fixture
def temp_data(tmp_path):
    source = Path("tests/pecha/merge/data")
    destination = tmp_path / "data"
    shutil.copytree(source, destination)
    return destination


def test_pecha_merge(temp_data):
    source_pecha_path = Path(temp_data / "P0002")
    target_pecha_path = Path(temp_data / "P0001")
    source_base_name = "0002"
    target_base_name = "0001"

    source_pecha = Pecha.from_path(source_pecha_path)
    target_pecha = Pecha.from_path(target_pecha_path)

    source_base = source_pecha.get_base(source_base_name)
    target_base = target_pecha.get_base(target_base_name)

    assert source_base != target_base
    target_pre_merge_n_layers = len(list(target_pecha.get_layers(target_base_name)))
    source_n_layers = len(list(source_pecha.get_layers(source_base_name)))

    pecha = Pecha.from_path(source_pecha_path)
    target_pecha.merge_pecha(pecha, source_base_name, target_base_name)

    target_post_merge_n_layers = len(list(target_pecha.get_layers(target_base_name)))

    assert target_post_merge_n_layers == target_pre_merge_n_layers + source_n_layers

    """ clean up"""
    target_new_post_layer_path = (
        Path(__file__).parent
        / "data"
        / "P0001"
        / "layers"
        / "0001"
        / "Root_Segment-a222.json"
    )
    if target_new_post_layer_path.exists():
        target_new_post_layer_path.unlink()


test_pecha_merge(Path(__file__).parent / "data")
