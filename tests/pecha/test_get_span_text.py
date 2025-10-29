from openpecha.pecha import Pecha
from openpecha.pecha.annotations import span
from pathlib import Path

def test_get_span_text():
    pecha = Pecha.from_path(Path("tests/pecha/data/I5003D420"))
    text = pecha.get_span_text(span(start=0, end=12))
    print(text)
    assert text == "In Sanskrit:"

def test_get_span_text_without_span():
    pecha = Pecha.from_path(Path("tests/pecha/data/I5003D420"))
    text = pecha.get_span_text()
    assert text == pecha.get_base_text()

if __name__ == "__main__":
    test_get_span_text()
    test_get_span_text_without_span()