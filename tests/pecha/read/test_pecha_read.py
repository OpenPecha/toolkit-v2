from pathlib import Path

from stam import AnnotationStore

from openpecha.pecha import Pecha


def test_pecha_read():
    DATA = Path(__file__).parent / "data"
    pecha_path = DATA / "I41CFF555"
    pecha = Pecha.from_path(pecha_path)
    assert pecha.id_ == "I41CFF555"

    ann_store = pecha.get_annotation_store("Comment")
    assert isinstance(ann_store, AnnotationStore)


test_pecha_read()
