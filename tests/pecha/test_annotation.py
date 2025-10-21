import pytest
from pydantic import ValidationError

from openpecha.pecha.annotations import (
    BaseAnnotation,
    span,
)


def test_span_end_must_not_be_less_than_start():
    with pytest.raises(ValidationError):
        span(start=2, end=1)


def test_annotation_id():
    ann = BaseAnnotation(span=span(start=10, end=20))
    assert ann.span.start == 10
    assert ann.span.end == 20