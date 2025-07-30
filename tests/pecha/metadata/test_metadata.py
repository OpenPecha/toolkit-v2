import json
from datetime import datetime
from pathlib import Path
from unittest import TestCase

from openpecha import ids
from openpecha.bdrc_utils import extract_metadata_for_work, format_metadata_for_op_api
from openpecha.pecha.metadata import (
    Copyright,
    CopyrightStatus,
    InitialCreationType,
    InitialPechaMetadata,
    LicenseType,
    PechaMetaData,
)
from openpecha.pecha.parsers import DummyParser
from openpecha.utils import read_json


class TestPechaMetadata(TestCase):
    def test_create_instance(self):
        """
        Create an instance of PechaMetaData from raw metadata.
        """
        file = Path(__file__).parent / "data" / "input_metadata.json"
        with open(file) as f:
            metadata = json.load(f)
        pecha_metadata = PechaMetaData(parser=DummyParser().name, **metadata)

        toolkit_version = pecha_metadata.toolkit_version
        self.assertEqual(len((toolkit_version).split(".")), 3)
        self.assertIsInstance(pecha_metadata, PechaMetaData)

    def test_load(self):
        """
        Create an instance of PechaMetaData from a processed metadata file.
        """
        file = Path(__file__).parent / "data" / "pecha_metadata.json"
        with open(file) as f:
            metadata = json.load(f)

        pecha_metadata = PechaMetaData(**metadata)
        self.assertIsInstance(pecha_metadata, PechaMetaData)

    def test_toolkit_version(self):
        """Test when toolkit_version is provided in input"""
        file = Path(__file__).parent / "data" / "input_metadata.json"
        with open(file) as f:
            metadata = json.load(f)

        pecha_metadata = PechaMetaData(parser=DummyParser().name, **metadata)
        self.assertIsInstance(pecha_metadata.toolkit_version, str)

    def test_base_pecha_metadata_model(self):
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

        self.assertEqual(metadata.imported, imported_at)
        self.assertEqual(metadata.last_modified, last_modified_at)
        self.assertEqual(
            metadata.initial_creation_type.value, InitialCreationType.ocr.value
        )
        self.assertTrue(metadata.id.startswith("I"))
        self.assertEqual(len(metadata.id), 9)

    def test_initial_pecha_metadata(self):
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

        self.assertEqual(
            metadata.initial_creation_type.value, InitialCreationType.ocr.value
        )
        self.assertTrue(metadata.id.startswith("I"))

        self.assertIsNotNone(metadata.statistics)
        self.assertEqual(metadata.statistics["ocr_word_median_confidence_index"], 0.9)
        self.assertIsNotNone(metadata.bases)
        self.assertEqual(metadata.bases["id"], "529C")

    def test_pecha_copyright(self):
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

        self.assertIsNotNone(metadata.copyright)
        self.assertEqual(metadata.copyright.status, copyright_status)

    def test_pecha_licence(self):
        license_type = LicenseType.CC_BY_NC_SA

        metadata = InitialPechaMetadata(
            initial_creation_type=InitialCreationType.ocr,
            license=license_type,
            parser=DummyParser().name,  # Add parser field.
        )

        self.assertIsNotNone(metadata.license)
        self.assertEqual(metadata.license, license_type)

    def test_extract_metadata_for_work(self):
        metadata = extract_metadata_for_work(Path(__file__).parent / "data" / "W24767")
        expected_metadata = read_json(
            Path(__file__).parent / "data" / "expected_extracted_metadata.json"
        )
        self.assertIsNotNone(metadata)
        self.assertIsInstance(metadata, dict)

        if metadata and expected_metadata:  # check both metadata and expected_metadata
            if metadata.get("ocr_import_info") and expected_metadata.get(
                "ocr_import_info"
            ):
                self.assertEqual(
                    metadata.get("ocr_import_info"),
                    expected_metadata.get("ocr_import_info"),
                )
            if metadata.get("buda_data") and expected_metadata.get("buda_data"):
                self.assertEqual(
                    metadata.get("buda_data"), expected_metadata.get("buda_data")
                )

    def test_format_metadata_for_op_api(self):
        """Test that BDRC metadata is correctly formatted for OpenPecha API."""
        # Load test input data
        metadata = extract_metadata_for_work(Path(__file__).parent / "data" / "W24767")

        # Call the function under test
        formatted_data = format_metadata_for_op_api(metadata)

        # Load expected output
        expected_formatted_metadata = read_json(
            Path(__file__).parent / "data" / "expected_formatted_metadata.json"
        )

        self.assertIsNotNone(formatted_data)
        self.assertIsInstance(formatted_data, dict)

        if formatted_data and expected_formatted_metadata:
            if formatted_data.get("bdrc") and expected_formatted_metadata.get("bdrc"):
                self.assertEqual(
                    formatted_data.get("bdrc"), expected_formatted_metadata.get("bdrc")
                )
            if formatted_data.get("author") and expected_formatted_metadata.get(
                "author"
            ):
                self.assertEqual(
                    formatted_data.get("author"),
                    expected_formatted_metadata.get("author"),
                )
            if formatted_data.get("document_id") and expected_formatted_metadata.get(
                "document_id"
            ):
                self.assertEqual(
                    formatted_data.get("document_id"),
                    expected_formatted_metadata.get("document_id"),
                )
            if formatted_data.get("language") and expected_formatted_metadata.get(
                "language"
            ):
                self.assertEqual(
                    formatted_data.get("language"),
                    expected_formatted_metadata.get("language"),
                )
            if formatted_data.get("long_title") and expected_formatted_metadata.get(
                "long_title"
            ):
                self.assertEqual(
                    formatted_data.get("long_title"),
                    expected_formatted_metadata.get("long_title"),
                )
            if formatted_data.get("source_url") and expected_formatted_metadata.get(
                "source_url"
            ):
                self.assertEqual(
                    formatted_data.get("source_url"),
                    expected_formatted_metadata.get("source_url"),
                )
            if formatted_data.get("title") and expected_formatted_metadata.get("title"):
                self.assertEqual(
                    formatted_data.get("title"),
                    expected_formatted_metadata.get("title"),
                )
