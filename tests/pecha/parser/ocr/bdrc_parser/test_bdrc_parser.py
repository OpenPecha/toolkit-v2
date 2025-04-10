from pathlib import Path
from unittest import TestCase, mock

from openpecha.bdrc_utils import extract_metadata_for_work, format_metadata_for_op_api
from openpecha.pecha.parsers.ocr import BdrcParser
from openpecha.pecha.parsers.ocr.data_source import (
    BDRCGBSource,
    GoogleVisionSource,
    HOCRIASource,
)


class TestBdrcParser(TestCase):
    def setUp(self):
        self.parser = BdrcParser()

    @mock.patch("openpecha.pecha.parsers.ocr.google_vision.GoogleVisionParser.parse")
    def test_google_vision_parse(self, mock_gv_parser):
        mock_gv_parser.return_value = {}
        zip_file_path = Path(__file__).parent / "data" / "gv_work" / "W24767.zip"
        work_path = Path(__file__).parent / "data" / "gv_work" / "W24767"
        extracted_metadata = extract_metadata_for_work(work_path)
        formatted_metadata = format_metadata_for_op_api(extracted_metadata)
        _ = self.parser.parse(zip_file_path, formatted_metadata)
        mock_gv_parser.assert_called_once()
        # Modified assertion: Check the type instead of the instance
        assert isinstance(mock_gv_parser.call_args[0][0], GoogleVisionSource)
        assert mock_gv_parser.call_args[0][1] is None
        assert mock_gv_parser.call_args[0][2] == {}

    @mock.patch("openpecha.pecha.parsers.ocr.hocr.HOCRParser.parse")
    def test_hocr_parse(self, mock_hocr_parser):
        mock_hocr_parser.return_value = {}
        zip_file_path = Path(__file__).parent / "data" / "hocr_ia_work" / "W22084.zip"
        work_path = Path(__file__).parent / "data" / "hocr_ia_work" / "W22084"
        extracted_metadata = extract_metadata_for_work(work_path)
        formatted_metadata = format_metadata_for_op_api(extracted_metadata)
        _ = self.parser.parse(zip_file_path, formatted_metadata)
        mock_hocr_parser.assert_called_once()
        # Modified assertion: Check the type instead of the instance
        assert isinstance(mock_hocr_parser.call_args[0][0], HOCRIASource)
        assert mock_hocr_parser.call_args[0][1] is None
        assert mock_hocr_parser.call_args[0][2] == {}

    @mock.patch("openpecha.pecha.parsers.ocr.hocr.HOCRParser.parse")
    def test_bdrc_gb_parse(self, mock_bdrc_parser):
        mock_bdrc_parser.return_value = {}
        zip_file_path = (
            Path(__file__).parent / "data" / "bdrc_gb_work" / "W1KG10193.zip"
        )
        work_path = Path(__file__).parent / "data" / "bdrc_gb_work" / "W1KG10193"
        extracted_metadata = extract_metadata_for_work(work_path)
        formatted_metadata = format_metadata_for_op_api(extracted_metadata)
        _ = self.parser.parse(zip_file_path, formatted_metadata)
        mock_bdrc_parser.assert_called_once()
        # Modified assertion: Check the type instead of the instance
        assert isinstance(mock_bdrc_parser.call_args[0][0], BDRCGBSource)
        assert mock_bdrc_parser.call_args[0][1] is None
        assert mock_bdrc_parser.call_args[0][2] == {}

    def tearDown(self):
        pass


if __name__ == "__main__":
    import unittest

    unittest.main()
