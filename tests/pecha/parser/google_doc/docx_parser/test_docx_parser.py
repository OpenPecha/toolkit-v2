from typing import Union
from unittest import TestCase

from openpecha.pecha.parsers.google_doc import DocxParser


class TestDocxParser(TestCase):
    def setUp(self):
        self.parser = DocxParser()

    def test_root_pecha(self):
        # this is the root pecha
        metadatas: list[dict[str, Union[str, None]]] = [
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
            },
        ]
        assert not self.parser.is_commentary_pecha(metadatas)

    def test_root_translation_pecha(self):
        # translation of root pecha
        metadatas: list[dict[str, Union[str, None]]] = [
            {
                "translation_of": "P0001",
                "commentary_of": None,
                "version_of": None,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
            },
        ]
        assert not self.parser.is_commentary_pecha(metadatas)

    def test_commentary_pecha(self):
        metadatas: list[dict[str, Union[str, None]]] = [
            {
                "translation_of": None,
                "commentary_of": "P0001",
                "version_of": None,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
            },
        ]
        assert self.parser.is_commentary_pecha(metadatas)

    def test_commentary_translation_pecha(self):
        # translation of commentary pecha
        metadatas: list[dict[str, Union[str, None]]] = [
            {
                "translation_of": "P0001",
                "commentary_of": None,
                "version_of": None,
            },
            {
                "translation_of": None,
                "commentary_of": "P0002",
                "version_of": None,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
            },
        ]
        assert self.parser.is_commentary_pecha(metadatas)

    def tearDown(self):
        pass
