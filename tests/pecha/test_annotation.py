import json

import pytest
from pydantic import ValidationError

from openpecha.pecha.annotations import (
    AnnotationModel,
    BaseAnnotation,
    PechaAlignment,
    PechaId,
    Span,
)
from openpecha.pecha.layer import AnnotationType


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


def test_annotation_model_minimal_alignment():
    align = PechaAlignment(pecha_id="I1234ABCD", alignment_id="align1")
    am = AnnotationModel(
        pecha_id="I1234ABCD",
        type=AnnotationType.ALIGNMENT,
        document_id="doc1",
        path="ann1",
        title="Test",
        aligned_to=align,
    )
    assert am.pecha_id == "I1234ABCD"
    assert am.type == AnnotationType.ALIGNMENT
    assert am.aligned_to == align


def test_annotation_model_minimal_non_alignment():
    am = AnnotationModel(
        pecha_id="I1234ABCD",
        type=AnnotationType.SEGMENTATION,
        document_id="doc1",
        path="ann1",
        title="Test",
    )
    assert am.pecha_id == "I1234ABCD"
    assert am.type == AnnotationType.SEGMENTATION
    assert am.aligned_to is None


def test_annotation_model_with_alignment():
    align = PechaAlignment(pecha_id="I1234ABCD", alignment_id="align1")
    am = AnnotationModel(
        pecha_id="I1234ABCD",
        type=AnnotationType.ALIGNMENT,
        document_id="doc1",
        path="ann1",
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
            type=AnnotationType.ALIGNMENT,
            document_id="doc1",
            path="ann1",
            title="Test",
        )


def test_pecha_relationship_enum():
    from openpecha.pecha.annotations import PechaRelationship

    # Test enum values
    assert PechaRelationship.commentary_of.value == "commentary_of"
    assert PechaRelationship.translation_of.value == "translation_of"

    # Test accessing by value
    assert PechaRelationship("commentary_of") == PechaRelationship.commentary_of
    assert PechaRelationship("translation_of") == PechaRelationship.translation_of

    # Test invalid value raises ValueError
    import pytest

    with pytest.raises(ValueError):
        PechaRelationship("invalid_value")


def test_annotation_model_missing_required():
    with pytest.raises(ValidationError):
        AnnotationModel(
            pecha_id="I1234ABCD",
            type=AnnotationType.ALIGNMENT,
            document_id="doc1",
            # path missing
            title="Test",
        )


class TestValidAnnotationModel:
    """Tests for valid annotation models in different scenarios."""

    def test_valid_annotation_minimal(self):
        """Test minimal valid annotation with default values."""
        input_data = {
            "pecha_id": "I12345678",
            "document_id": "DOC123",
            "title": "Test Annotation",
            "path": "E11/layer.json",
        }

        model = AnnotationModel(**input_data)
        assert str(model.pecha_id) == "I12345678"
        assert model.document_id == "DOC123"
        assert model.title == "Test Annotation"
        assert model.type == AnnotationType.SEGMENTATION
        assert model.aligned_to is None

    def test_valid_annotation_with_type(self):
        """Test valid annotation with explicit type."""
        input_data = {
            "pecha_id": "I12345678",
            "document_id": "DOC123",
            "title": "Test Alignment Annotation",
            "type": "alignment",
            "path": "E11/layer.json",
        }

        model = AnnotationModel(**input_data)
        assert str(model.pecha_id) == "I12345678"
        assert model.document_id == "DOC123"
        assert model.title == "Test Alignment Annotation"
        assert model.type == AnnotationType.ALIGNMENT
        assert model.aligned_to is None

    def test_valid_annotation_with_alignment(self):
        """Test valid annotation with alignment information."""
        input_data = {
            "pecha_id": "I12345678",
            "document_id": "DOC123",
            "title": "Test Annotation with Alignment",
            "type": "alignment",
            "path": "E11/layer.json",
            "aligned_to": {
                "pecha_id": "I87654321",
                "alignment_id": "ALIGN001",
            },
        }

        model = AnnotationModel(**input_data)
        assert str(model.pecha_id) == "I12345678"
        assert model.document_id == "DOC123"
        assert model.title == "Test Annotation with Alignment"
        assert model.type == AnnotationType.ALIGNMENT
        assert model.aligned_to is not None
        assert model.model_dump()["aligned_to"]["pecha_id"] == "I87654321"
        assert model.model_dump()["aligned_to"]["alignment_id"] == "ALIGN001"

    def test_valid_annotation_from_dict(self):
        """Test creating a valid annotation from a dictionary."""
        input_data = {
            "pecha_id": "I12345678",
            "document_id": "DOC123",
            "title": "Test Dict Annotation",
            "path": "E11/layer.json",
        }

        model = AnnotationModel.model_validate(input_data)
        assert str(model.pecha_id) == "I12345678"
        assert model.document_id == "DOC123"
        assert model.title == "Test Dict Annotation"
        assert model.type == AnnotationType.SEGMENTATION


class TestInvalidAnnotationModel:
    """Tests for invalid annotation models that should raise validation errors."""

    def test_invalid_pecha_id_format(self):
        """Test that invalid pecha_id format raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="invalid_id",  # Should start with I and contain 8 hex chars
                document_id="DOC123",
                title="Invalid ID Test",
                path="E11/layer.json",
            )

        # Check the specific validation error message
        errors = exc_info.value.errors()
        assert any(
            err["loc"] == ("pecha_id",)
            and "PechaId must start with 'I' followed by 8 uppercase hex characters"
            in err["msg"]
            for err in errors
        )

    def test_missing_document_id(self):
        """Test that missing document_id raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="I12345678",
                # Missing document_id
                title="Missing Document ID Test",
            )

        errors = exc_info.value.errors()
        assert any("document_id" in str(err) for err in errors)
        assert any("Field required" in str(err) for err in errors)

    def test_missing_title(self):
        """Test that missing title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="I12345678",
                document_id="DOC123",
                # Missing title
            )

        errors = exc_info.value.errors()
        assert any("title" in str(err) for err in errors)
        assert any("Field required" in str(err) for err in errors)

    def test_empty_title(self):
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="I12345678",
                document_id="DOC123",
                title="",  # Empty title
            )

        errors = exc_info.value.errors()
        assert any("title" in str(err) for err in errors)
        assert any("min_length" in str(err) for err in errors)

    def test_invalid_document_id(self):
        """Test that invalid document_id raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="I12345678",
                document_id="",  # Empty document_id
                title="Invalid Document ID Test",
            )

        errors = exc_info.value.errors()
        assert any("document_id" in str(err) for err in errors)
        assert any("pattern" in str(err) for err in errors)

    def test_invalid_type(self):
        """Test that invalid type raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="I12345678",
                document_id="DOC123",
                title="Invalid Type Test",
                type="invalid_type",  # Not in AnnotationType enum
            )

        errors = exc_info.value.errors()
        assert any("type" in str(err) for err in errors)
        assert any("enum" in str(err) for err in errors)

    def test_invalid_aligned_to(self):
        """Test that invalid aligned_to raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="I12345678",
                document_id="DOC123",
                title="Invalid Alignment Test",
                type="Alignment",
                path="E11/layer.json",
                aligned_to={
                    "pecha_id": "invalid_id",  # Invalid pecha_id format
                    "alignment_id": "ALIGN001",
                },
            )

        errors = exc_info.value.errors()
        assert any("aligned_to" in str(err) for err in errors)
        assert any(
            err["loc"] == ("aligned_to", "pecha_id")
            and "PechaId must start with 'I' followed by 8 uppercase hex characters"
            in err["msg"]
            for err in errors
        )

    def test_missing_alignment_id(self):
        """Test that missing alignment_id in aligned_to raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            AnnotationModel(
                pecha_id="I12345678",
                document_id="DOC123",
                title="Missing Alignment ID Test",
                type="Alignment",
                aligned_to={
                    "pecha_id": "I87654321",
                    # Missing alignment_id
                },
            )

        errors = exc_info.value.errors()
        assert any("aligned_to" in str(err) for err in errors)
        assert any("alignment_id" in str(err) for err in errors)


class TestAnnotationModelSerialization:
    """Tests for serialization of annotation models."""

    def test_model_dump(self):
        """Test model_dump() produces the expected dictionary."""
        model = AnnotationModel(
            pecha_id="I12345678",
            document_id="DOC123",
            title="Serialization Test",
            type="alignment",
            path="E11/layer.json",
            aligned_to={
                "pecha_id": "I87654321",
                "alignment_id": "ALIGN001",
            },
        )

        data = model.model_dump()
        assert data["pecha_id"] == "I12345678"  # Should be string not nested object
        assert data["document_id"] == "DOC123"
        assert data["title"] == "Serialization Test"
        assert data["type"] == AnnotationType.ALIGNMENT
        assert data["path"] == "E11/layer.json"
        assert data["aligned_to"]["pecha_id"] == "I87654321"
        assert data["aligned_to"]["alignment_id"] == "ALIGN001"

    def test_model_dump_json(self):
        """Test model_dump_json() produces valid JSON with expected structure."""
        model = AnnotationModel(
            pecha_id="I12345678",
            document_id="DOC123",
            title="JSON Serialization Test",
            path="E11/layer.json",
        )

        json_str = model.model_dump_json()
        data = json.loads(json_str)

        assert data["pecha_id"] == "I12345678"
        assert data["document_id"] == "DOC123"
        assert data["title"] == "JSON Serialization Test"
        assert data["type"] == "segmentation"
        assert data["path"] == "E11/layer.json"
        assert data["aligned_to"] is None

    def test_json_schema(self):
        """Test the JSON schema is correctly generated."""
        schema = AnnotationModel.model_json_schema()

        # Check basic schema structure
        assert "properties" in schema
        assert "pecha_id" in schema["properties"]
        assert "document_id" in schema["properties"]
        assert "title" in schema["properties"]
        assert "type" in schema["properties"]
        assert "aligned_to" in schema["properties"]

        # Check required fields
        assert "required" in schema
        required_fields = schema["required"]
        assert "pecha_id" in required_fields
        assert "document_id" in required_fields
        assert "title" in required_fields


work = TestInvalidAnnotationModel()
work.test_invalid_pecha_id_format()
work.test_invalid_aligned_to()
