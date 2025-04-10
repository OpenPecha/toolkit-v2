import tempfile
from pathlib import Path
from unittest import TestCase

from openpecha.pecha.parsers.ocr.data_source import GoogleVisionSource
from openpecha.pecha.parsers.ocr.google_vision import GoogleVisionParser
from openpecha.utils import read_json


class TestGoogleVisionMetaData(TestCase):
    def setUp(self):
        work_id = "W24767"
        pecha_id = "I123456"

        ocr_path = Path(__file__).parent / "data" / work_id
        expected_meta_path = (
            Path(__file__).parent
            / "data"
            / "pecha_expected_data"
            / "expected_google_ocr_meta.json"
        )
        self.expected_metadata = read_json(expected_meta_path) or {}
        buda_data_path = Path(__file__).parent / "data" / work_id / "buda_data.json"
        ocr_import_info_path = (
            Path(__file__).parent / "data" / work_id / "ocr_import_info.json"
        )
        ocr_import_info = read_json(ocr_import_info_path)
        buda_data = read_json(buda_data_path)
        data_source = GoogleVisionSource(
            bdrc_scan_id=work_id,
            buda_data=buda_data,
            ocr_import_info=ocr_import_info,
            ocr_disk_path=ocr_path,
        )

        with tempfile.TemporaryDirectory() as tmpdirname:
            formatter = GoogleVisionParser(output_path=tmpdirname)
            pecha = formatter.parse(data_source, pecha_id, {}, ocr_import_info)
            output_metadata = pecha.load_metadata()
            self.pecha_metadata = output_metadata

    def test_metadata(self):
        # Check licence field (note the spelling)
        assert self.pecha_metadata.parser == self.expected_metadata.get(
            "parser"
        ), "Parser mismatch"
        assert (
            self.pecha_metadata.licence.value == self.expected_metadata["licence"]
        ), "Licence mismatch"

        # Check copyright fields
        assert (
            self.pecha_metadata.copyright.status.value
            == self.expected_metadata["copyright"]["status"]
        ), "Copyright status mismatch"
        assert (
            self.pecha_metadata.copyright.notice
            == self.expected_metadata["copyright"]["notice"]
        ), "Copyright notice mismatch"
        assert (
            self.pecha_metadata.copyright.info_url
            == self.expected_metadata["copyright"]["info_url"]
        ), "Copyright info URL mismatch"

        # Check source metadata fields
        assert self.pecha_metadata.source_metadata.get(
            "access"
        ) == self.expected_metadata["source_metadata"].get(
            "access"
        ), "Source metadata access mismatch"
        assert self.pecha_metadata.source_metadata.get(
            "geo_restriction"
        ) == self.expected_metadata["source_metadata"].get(
            "geo_restriction"
        ), "Source metadata geo restriction mismatch"

    def test_base_metadata(self):
        actual_bases = self.pecha_metadata.bases
        expected_bases = self.expected_metadata.get("bases")

        assert actual_bases == expected_bases, "Bases metadata mismatch"


work = TestGoogleVisionMetaData()
work.setUp()
work.test_base_metadata()
