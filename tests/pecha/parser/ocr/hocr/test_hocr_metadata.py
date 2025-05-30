import tempfile
from pathlib import Path
from typing import Any, Dict, cast
from unittest import TestCase

from openpecha.pecha.parsers.ocr.data_source import BDRCGBSource
from openpecha.pecha.parsers.ocr.hocr import HOCRParser
from openpecha.utils import read_json


class TestHORCRMetaData(TestCase):
    def setUp(self):
        work_id = "W1KG10193"
        pecha_id = "I123456"

        ocr_path = Path(__file__).parent / "data" / "file_per_page" / work_id
        expected_meta_path = (
            Path(__file__).parent
            / "data"
            / "file_per_page"
            / "pecha_expected_data"
            / "expected_hocr_meta.json"
        )
        buda_data_path = (
            Path(__file__).parent
            / "data"
            / "file_per_page"
            / work_id
            / "buda_data.json"
        )
        ocr_import_info_path = (
            Path(__file__).parent
            / "data"
            / "file_per_page"
            / work_id
            / "ocr_import_info.json"
        )
        ocr_import_info = read_json(ocr_import_info_path)
        buda_data = read_json(buda_data_path)
        data_source = BDRCGBSource(work_id, buda_data, ocr_import_info, ocr_path)

        self.expected_metadata: Dict[str, Any] = cast(
            Dict[str, Any], read_json(expected_meta_path)
        )
        if not self.expected_metadata:
            raise ValueError(
                f"Failed to read expected metadata from {expected_meta_path}"
            )

        with tempfile.TemporaryDirectory() as tmpdirname:
            formatter = HOCRParser(output_path=tmpdirname)
            pecha = formatter.parse(
                data_source,
                pecha_id,
                {"remove_duplicate_symbols": True},
                ocr_import_info,
            )
            self.pecha_metadata = pecha.load_metadata()

    def test_metadata(self):
        # Check licence field (note the spelling)
        assert self.pecha_metadata.parser == self.expected_metadata.get(
            "parser"
        ), "Parser mismatch"
        assert self.pecha_metadata.licence.value == self.expected_metadata.get(
            "licence"
        ), "Licence mismatch"

        # Check copyright fields
        assert self.pecha_metadata.copyright.status.value == self.expected_metadata.get(
            "copyright", {}
        ).get("status"), "Copyright status mismatch"
        assert self.pecha_metadata.copyright.notice == self.expected_metadata.get(
            "copyright", {}
        ).get("notice"), "Copyright notice mismatch"
        assert self.pecha_metadata.copyright.info_url == self.expected_metadata.get(
            "copyright", {}
        ).get("info_url"), "Copyright info URL mismatch"

        # Check source metadata fields
        assert self.pecha_metadata.source_metadata.get(
            "access"
        ) == self.expected_metadata.get("source_metadata", {}).get(
            "access"
        ), "Source metadata access mismatch"
        assert self.pecha_metadata.source_metadata.get(
            "geo_restriction"
        ) == self.expected_metadata.get("source_metadata", {}).get(
            "geo_restriction"
        ), "Source metadata geo restriction mismatch"

    def test_base_metadata(self):
        actual_bases = self.pecha_metadata.bases
        expected_bases = self.expected_metadata.get("bases")

        assert actual_bases == expected_bases, "Bases metadata mismatch"
