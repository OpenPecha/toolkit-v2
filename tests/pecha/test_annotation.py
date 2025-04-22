import pytest
from pydantic import ValidationError

from openpecha.pecha.annotations import BaseAnnotation, Span


def test_span_end_must_not_be_less_than_start():
    with pytest.raises(ValidationError):
        Span(start=2, end=1)


def test_annotation_id():
    ann = BaseAnnotation(span=Span(start=10, end=20))
    assert ann.span.start == 10
    assert ann.span.end == 20
    assert ann.metadata is None
