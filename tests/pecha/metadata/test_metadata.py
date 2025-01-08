import json
from pathlib import Path

from openpecha.pecha.metadata import PechaMetaData
from openpecha.pecha.parsers import DummyParser


def test_create_instance():
    """
    Create an instance of PechaMetaData from raw metadata.
    """
    file = Path(__file__).parent / "data" / "input_metadata.json"
    with open(file) as f:
        metadata = json.load(f)
    pecha_metadata = PechaMetaData(parser=DummyParser().name, **metadata)

    toolkit_version = pecha_metadata.toolkit_version
    assert len((toolkit_version).split(".")) == 3
    assert isinstance(pecha_metadata, PechaMetaData)


def test_load():
    """
    Create an instance of PechaMetaData from a processed metadata file.
    """
    file = Path(__file__).parent / "data" / "pecha_metadata.json"
    with open(file) as f:
        metadata = json.load(f)

    pecha_metadata = PechaMetaData(**metadata)
    assert isinstance(pecha_metadata, PechaMetaData)

def test_toolkit_version():
    """Test when toolkit_version is provided in input"""
    file = Path(__file__).parent / "data" / "input_metadata.json"
    with open(file) as f:
        metadata = json.load(f)

    pecha_metadata = PechaMetaData(parser=DummyParser().name, **metadata)
    assert pecha_metadata.toolkit_version == "0.0.1"
