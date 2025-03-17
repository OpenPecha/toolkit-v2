import pytest

from openpecha.exceptions import MetaDataMissingError, MetaDataValidationError
from openpecha.pecha.parsers.docx import PechaOrgPechaMetaDataValidator


@pytest.fixture
def validator():
    return PechaOrgPechaMetaDataValidator()


def test_validate_metadata_dtype(validator):
    with pytest.raises(TypeError, match="Input metadata should be a dictionary"):
        validator.validate_metadata_dtype("invalid_type")


def test_validate_en_title_missing(validator):
    metadata = {"title": {"bo": "བོད་ཀྱི་མིང་"}, "lang": "bo"}
    with pytest.raises(
        MetaDataMissingError, match="English title is missing in metadata"
    ):
        validator.validate_en_title(metadata)


def test_validate_bo_title_missing(validator):
    metadata = {"title": {"en": "English Title"}, "lang": "bo"}
    with pytest.raises(
        MetaDataMissingError, match="Tibetan title is missing in metadata"
    ):
        validator.validate_bo_title(metadata)


def test_validate_lang_title_missing(validator):
    metadata = {"title": {"en": "English Title", "bo": "བོད་ཀྱི་མིང་"}, "lang": "fr"}
    with pytest.raises(MetaDataMissingError, match="fr title is missing in metadata"):
        validator.validate_lang_title(metadata)


def test_ensure_no_forbidden_symbols(validator):
    with pytest.raises(MetaDataValidationError, match="Title can't have symbol -"):
        validator.ensure_no_forbidden_symbols("Invalid-Title")

    with pytest.raises(MetaDataValidationError, match="Title can't have symbol :"):
        validator.ensure_no_forbidden_symbols("Invalid:Title")

    with pytest.raises(MetaDataValidationError, match="Title can't have symbol _"):
        validator.ensure_no_forbidden_symbols("Invalid_Title")

    with pytest.raises(MetaDataValidationError, match="Title can't have symbol ."):
        validator.ensure_no_forbidden_symbols("Invalid.Title")

    with pytest.raises(MetaDataValidationError, match="Title can't have symbol /"):
        validator.ensure_no_forbidden_symbols("Invalid/Title")


def test_validate_metadata_success(validator):
    metadata = {
        "title": {"en": "Valid Title", "bo": "བོད་ཀྱི་མིང་", "fr": "Titre Français"},
        "lang": "bo",
    }
    try:
        validator.validate_metadata(metadata)
    except Exception as e:
        pytest.fail(f"Validation failed unexpectedly: {e}")
