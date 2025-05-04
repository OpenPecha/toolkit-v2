import json
from datetime import datetime
from pathlib import Path

from openpecha import ids
from openpecha.bdrc_utils import extract_metadata_for_work, format_metadata_for_op_api
from openpecha.pecha.metadata import (
    Copyright,
    CopyrightStatus,
    DiplomaticPechaMetadata,
    InitialCreationType,
    InitialPechaMetadata,
    LicenseType,
    OpenPechaMetadata,
    PechaMetaData,
)
from openpecha.pecha.parsers import DummyParser
from openpecha.utils import read_json


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
    assert isinstance(pecha_metadata.toolkit_version, str)


def test_base_pecha_metadata_model():
    imported_at = datetime.fromisoformat("2020-01-01T00:00:00")
    last_modified_at = datetime.fromisoformat("2020-01-01T00:00:00")

    metadata = PechaMetaData(
        id=ids.get_initial_pecha_id(),
        source="https://library.bdrc.io",
        source_file="https://library.bdrc.io/text.json",
        initial_creation_type=InitialCreationType.ocr,
        imported=imported_at,
        last_modified=last_modified_at,
        parser=DummyParser().name,
        source_metadata={
            "id": "bdr:W1PD90121",
            "title": "མའོ་རྫོང་གི་ས་ཆའི་མིང་བཏུས།",
            "author": "author name",
        },
        base={
            "f3c9": {
                "id": "I1PD90137",
                "title": "Volume 1 of mao wen qiang zu zi zhi xian di ming lu",
                "total_pages": 220,
                "order": 1,
                "base_file": "f3c9.tx",
            }
        },
    )

    assert metadata.imported == imported_at
    assert metadata.last_modified == last_modified_at
    assert metadata.initial_creation_type.value == InitialCreationType.ocr.value
    assert metadata.id.startswith("I")
    assert len(metadata.id) == 9


def test_initial_pecha_metadata():
    metadata = InitialPechaMetadata(
        initial_creation_type=InitialCreationType.ocr,
        statistics={"ocr_word_median_confidence_index": 0.9},
        bases={
            "id": "529C",
            "source_metadata": {
                "image_group_id": "I3CN8548",
                "title": "",
                "total_pages": 62,
            },
            "order": 1,
            "base_file": "529C.txt",
            "statistics": {
                "ocr_word_median_confidence_index": 0.9,
            },
        },
        parser=DummyParser().name,  # Add parser field.
    )

    assert metadata.initial_creation_type.value == InitialCreationType.ocr.value
    assert metadata.id.startswith("I")

    assert metadata.statistics is not None
    assert metadata.statistics["ocr_word_median_confidence_index"] == 0.9
    assert metadata.bases is not None
    assert metadata.bases["id"] == "529C"


def test_diplomatic_pecha_metadata():
    metadata = DiplomaticPechaMetadata(
        initial_creation_type=InitialCreationType.ocr,
        parser=DummyParser().name,  # Add parser field.
    )

    assert metadata.initial_creation_type.value == InitialCreationType.ocr.value
    assert metadata.id.startswith("D")


def test_open_pecha_metadata():
    metadata = OpenPechaMetadata(
        initial_creation_type=InitialCreationType.ocr,
        parser=DummyParser().name,  # Add parser field.
    )

    assert metadata.initial_creation_type.value == InitialCreationType.ocr.value
    assert metadata.id.startswith("O")


def test_pecha_copyright():
    copyright_status = CopyrightStatus.COPYRIGHTED

    copyright = Copyright(
        status=copyright_status,
        notice="Copyright 2022 OpenPecha",
        info_url="https://dev.openpecha.org",
    )

    metadata = InitialPechaMetadata(
        initial_creation_type=InitialCreationType.ocr,
        copyright=copyright,
        parser=DummyParser().name,  # Add parser field.
    )

    assert metadata.copyright is not None
    assert metadata.copyright.status == copyright_status


def test_pecha_licence():
    license_type = LicenseType.CC_BY_NC_SA

    metadata = InitialPechaMetadata(
        initial_creation_type=InitialCreationType.ocr,
        license=license_type,
        parser=DummyParser().name,  # Add parser field.
    )

    assert metadata.license is not None
    assert metadata.license == license_type


def test_extract_metadata_for_work():
    metadata = extract_metadata_for_work(Path(__file__).parent / "data" / "W24767")
    expected_metadata = read_json(
        Path(__file__).parent / "data" / "expected_extracted_metadata.json"
    )
    assert metadata is not None
    assert isinstance(metadata, dict)

    if metadata and expected_metadata:  # check both metadata and expected_metadata
        if metadata.get("ocr_import_info") and expected_metadata.get("ocr_import_info"):
            assert metadata.get("ocr_import_info") == expected_metadata.get(
                "ocr_import_info"
            )
        if metadata.get("buda_data") and expected_metadata.get("buda_data"):
            assert metadata.get("buda_data") == expected_metadata.get("buda_data")


def test_format_metadata_for_op_api():
    """Test that BDRC metadata is correctly formatted for OpenPecha API."""
    # Load test input data
    metadata = extract_metadata_for_work(Path(__file__).parent / "data" / "W24767")

    # Call the function under test
    formatted_data = format_metadata_for_op_api(metadata)

    # Load expected output
    expected_formatted_metadata = read_json(
        Path(__file__).parent / "data" / "expected_formatted_metadata.json"
    )

    assert formatted_data is not None
    assert isinstance(formatted_data, dict)

    if formatted_data and expected_formatted_metadata:
        if formatted_data.get("bdrc") and expected_formatted_metadata.get("bdrc"):
            assert formatted_data.get("bdrc") == expected_formatted_metadata.get("bdrc")
        if formatted_data.get("author") and expected_formatted_metadata.get("author"):
            assert formatted_data.get("author") == expected_formatted_metadata.get(
                "author"
            )
        if formatted_data.get("document_id") and expected_formatted_metadata.get(
            "document_id"
        ):
            assert formatted_data.get("document_id") == expected_formatted_metadata.get(
                "document_id"
            )
        if formatted_data.get("language") and expected_formatted_metadata.get(
            "language"
        ):
            assert formatted_data.get("language") == expected_formatted_metadata.get(
                "language"
            )
        if formatted_data.get("long_title") and expected_formatted_metadata.get(
            "long_title"
        ):
            assert formatted_data.get("long_title") == expected_formatted_metadata.get(
                "long_title"
            )
        if formatted_data.get("source_url") and expected_formatted_metadata.get(
            "source_url"
        ):
            assert formatted_data.get("source_url") == expected_formatted_metadata.get(
                "source_url"
            )
        if formatted_data.get("title") and expected_formatted_metadata.get("title"):
            assert formatted_data.get("title") == expected_formatted_metadata.get(
                "title"
            )
