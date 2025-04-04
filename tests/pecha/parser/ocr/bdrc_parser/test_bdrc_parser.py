from pathlib import Path
from unittest import TestCase

from openpecha.bdrc_utils import extract_metadata_for_work, format_metadata_for_op_api
from openpecha.pecha import Pecha
from openpecha.pecha.parsers.ocr import BdrcParser
from openpecha.pecha.parsers.ocr.google_vision import GoogleVisionParser
from openpecha.pecha.parsers.ocr.hocr import HOCRParser


class TestBdrcParser(TestCase):
    def setUp(self):
        self.parser = BdrcParser()

    def test_google_vision_parse(self):
        zip_file_path = Path(__file__).parent / "data" / "gv_work" / "W24767.zip"
        work_path = Path(__file__).parent / "data" / "gv_work" / "W24767"
        extracted_metadata = extract_metadata_for_work(work_path)
        formatted_metadata = format_metadata_for_op_api(extracted_metadata)
        pecha = self.parser.parse(zip_file_path, formatted_metadata)
        assert isinstance(pecha, Pecha)
        assert pecha.metadata.parser == GoogleVisionParser().name

    def test_hocr_parse(self):
        zip_file_path = Path(__file__).parent / "data" / "hocr_ia_work" / "W22084.zip"
        work_path = Path(__file__).parent / "data" / "hocr_ia_work" / "W22084"
        extracted_metadata = extract_metadata_for_work(work_path)
        formatted_metadata = format_metadata_for_op_api(extracted_metadata)
        pecha = self.parser.parse(zip_file_path, formatted_metadata)
        assert isinstance(pecha, Pecha)
        assert pecha.metadata.parser == HOCRParser().name

    def test_bdrc_gb_parse(self):
        zip_file_path = (
            Path(__file__).parent / "data" / "bdrc_gb_work" / "W1KG10193.zip"
        )
        work_path = Path(__file__).parent / "data" / "bdrc_gb_work" / "W1KG10193"
        extracted_metadata = extract_metadata_for_work(work_path)
        formatted_metadata = format_metadata_for_op_api(extracted_metadata)
        pecha = self.parser.parse(zip_file_path, formatted_metadata)
        assert isinstance(pecha, Pecha)
        assert pecha.metadata.parser == HOCRParser().name

    def tearDown(self):
        pass


if __name__ == "__main__":
    import unittest

    unittest.main()
