import tempfile
from pathlib import Path
from unittest import TestCase

from test_hocr_data_provider import BDRCGBTestFileProvider

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
            Path(__file__).parent / "data" / "file_per_page" / "buda_data.json"
        )
        ocr_import_info_path = (
            Path(__file__).parent / "data" / "file_per_page" / "ocr_import_info.json"
        )
        ocr_import_info = read_json(ocr_import_info_path)
        buda_data = read_json(buda_data_path)
        bdrc_image_list_path = Path(__file__).parent / "data" / "file_per_page"
        data_provider = BDRCGBTestFileProvider(
            work_id, bdrc_image_list_path, buda_data, ocr_import_info, ocr_path
        )

        self.expected_metadata = read_json(expected_meta_path)
        with tempfile.TemporaryDirectory() as tmpdirname:
            formatter = HOCRParser(output_path=tmpdirname)
            pecha = formatter.parse(
                data_provider,
                pecha_id,
                {"remove_duplicate_symbols": True},
                ocr_import_info,
            )
            self.pecha_metadata = pecha.load_metadata()

    def test_metadata(self):
        # Check licence field (note the spelling)
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
        assert self.pecha_metadata.source_metadata == self.expected_metadata.get(
            "source_metadata"
        ), "Source metadata mismatch"
        assert self.pecha_metadata.bases == self.expected_metadata.get(
            "bases"
        ), "Bases metadata mismatch"
