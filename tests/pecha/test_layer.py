import pytest
from pydantic import ValidationError

from openpecha.pecha.annotations import Citation, Layer, Span
from openpecha.pecha.layer import AnnotationType


def test_layer_model():
    layer = Layer(
        annotation_type=AnnotationType.BOOK_TITLE, revision="00001", annotations={}
    )
    assert layer.annotation_type.value == "book_title"
    assert layer.revision == "00001"
    layer.bump_revision()
    assert layer.revision == "00002"


def test_not_supported_layer():
    with pytest.raises(ValidationError):
        Layer(annotation_type="NotSupportedLayer", revision="00001", annotations={})


def test_revision_should_be_int_parsible():
    with pytest.raises(ValidationError):
        Layer(
            annotation_type=AnnotationType.BOOK_TITLE, revision="1aaa", annotations={}
        )


def test_layer_reset():
    layer = Layer(
        annotation_type=AnnotationType.BOOK_TITLE,
        revision="00003",
        annotations={"1": "ann"},
    )
    assert layer.revision == "00003"
    assert layer.annotations
    layer.reset()
    assert layer.revision == "00001"
    assert layer.annotations == {}


def test_add_annotation():
    layer = Layer(annotation_type=AnnotationType.CITATION)
    ann = Citation(span=Span(start=10, end=20))

    ann_id = layer.set_annotation(ann)
    assert ann_id in layer.annotations
    assert layer.get_annotation(ann_id) == ann


def test_get_annotation():
    layer = Layer(annotation_type=AnnotationType.CITATION)
    ann = Citation(span=Span(start=10, end=20))

    ann_id = layer.set_annotation(ann)
    assert ann_id in layer.annotations
    assert layer.get_annotation(ann_id) == ann


def test_remove_annotation():
    layer = Layer(annotation_type=AnnotationType.CITATION)
    ann = Citation(span=Span(start=10, end=20))

    ann_id = layer.set_annotation(ann)

    assert ann_id in layer.annotations

    layer.remove_annotation(ann_id)

    assert ann_id not in layer.annotations
