import pytest
from pydantic import ValidationError

from openpecha.pecha.annotations import (
    AnnotationModel,
    BaseAnnotation,
    PechaAlignment,
    PechaId,
    Span,
)
from openpecha.pecha.layer import LayerEnum


def test_span_end_must_not_be_less_than_start():
    with pytest.raises(ValidationError):
        Span(start=2, end=1)


def test_annotation_id():
    ann = BaseAnnotation(span=Span(start=10, end=20))
    assert ann.span.start == 10
    assert ann.span.end == 20
    assert ann.metadata is None


def test_pechaid_valid():
    pid = PechaId.validate("I1234ABCD")
    assert pid == "I1234ABCD"


def test_pechaid_invalid():
    with pytest.raises(ValueError):
        PechaId.validate("X1234ABCD")
    with pytest.raises(ValueError):
        PechaId.validate("I1234ABC")  # too short
    with pytest.raises(ValueError):
        PechaId.validate("I1234ABCDE")  # too long
    with pytest.raises(ValueError):
        PechaId.validate("I1234abcD")  # lowercase


def test_pecha_alignment_fields():
    pa = PechaAlignment(pecha_id="I1234ABCD", alignment_id="align1")
    assert pa.pecha_id == "I1234ABCD"
    assert pa.alignment_id == "align1"


def test_annotation_model_minimal():
    am = AnnotationModel(
        pecha_id="I1234ABCD",
        type=LayerEnum.alignment,
        document_id="doc1",
        id="ann1",
        title="Test",
    )
    assert am.pecha_id == "I1234ABCD"
    assert am.type == LayerEnum.alignment
    assert am.aligned_to is None


def test_annotation_model_with_alignment():
    align = PechaAlignment(pecha_id="I1234ABCD", alignment_id="align1")
    am = AnnotationModel(
        pecha_id="I1234ABCD",
        type=LayerEnum.alignment,
        document_id="doc1",
        id="ann1",
        title="Test",
        aligned_to=align,
    )
    assert am.aligned_to is not None
    assert am.aligned_to.pecha_id == "I1234ABCD"
    assert am.aligned_to.alignment_id == "align1"


def test_annotation_model_invalid_pechaid():
    with pytest.raises(ValidationError):
        AnnotationModel(
            pecha_id="BADID",
            type=LayerEnum.alignment,
            document_id="doc1",
            id="ann1",
            title="Test",
        )


def test_annotation_model_missing_required():
    with pytest.raises(ValidationError):
        AnnotationModel(
            pecha_id="I1234ABCD",
            type=LayerEnum.alignment,
            document_id="doc1",
            # id missing
            title="Test",
        )
