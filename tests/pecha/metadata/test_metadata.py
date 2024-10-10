import json
from pathlib import Path

from openpecha.pecha.metadata import PechaMetaData
from openpecha.pecha.parsers.chonjuk.plaintext import DummyParser


def test_create_instance():
    """
    Create an instance of PechaMetaData from raw metadata.
    """
    file = Path(__file__).parent / "data" / "input_metadata.json"
    with open(file) as f:
        metadata = json.load(f)
    pecha_metadata = PechaMetaData(parser=DummyParser().name, **metadata)

    assert isinstance(pecha_metadata, PechaMetaData)


def test_load():
    """
    Creata an instance of PechaMetaData from a processed metadata file.
    """
    file = Path(__file__).parent / "data" / "pecha_metadata.json"
    with open(file) as f:
        metadata = json.load(f)

    pecha_metadata = PechaMetaData(**metadata)
    assert isinstance(pecha_metadata, PechaMetaData)


test_load()
