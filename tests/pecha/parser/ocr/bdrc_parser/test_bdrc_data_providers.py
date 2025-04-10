from pathlib import Path
from unittest import TestCase

from openpecha.bdrc_utils import extract_metadata_for_work, format_metadata_for_op_api
from openpecha.pecha.parsers.ocr import BdrcParser
from openpecha.pecha.parsers.ocr.data_source import (
    BDRCGBSource,
    GoogleVisionSource,
    HOCRIASource,
)


class TestBdrcDataProviders(TestCase):
    def setUp(self):
        self.parser = BdrcParser()

    def test_google_vision_data_provider(self):
        work_path = Path(__file__).parent / "data" / "gv_work" / "W24767"
        metadata = extract_metadata_for_work(work_path)
        metadata = format_metadata_for_op_api(metadata)
        data_source = self.parser.determine_data_source(work_path, metadata)
        assert isinstance(data_source, GoogleVisionSource)

    def test_hocr_data_provider(self):
        work_path = Path(__file__).parent / "data" / "hocr_ia_work" / "W22084"
        metadata = extract_metadata_for_work(work_path)
        metadata = format_metadata_for_op_api(metadata)
        data_source = self.parser.determine_data_source(work_path, metadata)
        assert isinstance(data_source, HOCRIASource)

    def test_bdrc_gb_data_provider(self):
        work_path = Path(__file__).parent / "data" / "bdrc_gb_work" / "W1KG10193"
        metadata = extract_metadata_for_work(work_path)
        metadata = format_metadata_for_op_api(metadata)
        data_source = self.parser.determine_data_source(work_path, metadata)
        assert isinstance(data_source, BDRCGBSource)
