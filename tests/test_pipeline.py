from unittest import TestCase, mock

from openpecha.pipeline import translation_pipeline


class TestTranslationPipeline(TestCase):
    @mock.patch("openpecha.pipeline.GoogleDocAndSheetsDownloader")
    def setUp(self):
        self.bo_links = {
            "docx": "https://docs.google.com/document/d/1Gt0mFYzMbB7fnwKDzPvlweB9Fkj2oCBM/edit?usp=sharing&ouid=109531200462368596070&rtpof=true&sd=true",
            "sheet": "https://docs.google.com/spreadsheets/d/1ZBrqRqGibgJx0s3qRGDtSE75nXDt7g3b/edit?gid=1782814887#gid=1782814887",
        }
        self.en_links = {
            "docx": "https://docs.google.com/document/d/1Gt0mFYzMbB7fnwKDzPvlweB9Fkj2oCBM/edit?usp=sharing&ouid=109531200462368596070&rtpof=true&sd=true",
            "sheet": "https://docs.google.com/spreadsheets/d/1OQRbOM7wkUjmo8ulmpduOAF0Ed0kX0Sv/edit?gid=188752190#gid=188752190",
        }

    def test_translation_pipeline(self):
        translation_pipeline(self.bo_links, self.en_links)
