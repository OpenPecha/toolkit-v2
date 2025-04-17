from typing import Collection, Dict
from unittest import TestCase

from openpecha.pecha.parsers.docx import DocxParser

extra_fields = {
    "author": {"en": "DPO and Claude-3-5-sonnet-20241022"},
    "document_id": "1vgnfCQH3yaWPDaMDFXT_5GhlG0M9kEra0mxkDX46VLE",
    "language": "en",
    "long_title": {
        "en": "Illuminating the Intent Chapter 6, verses 1 to 64 Literal Translation, Monlam AI, February 2025"
    },
    "title": {
        "bo": "\u0f51\u0f42\u0f7c\u0f44\u0f66\u0f0b\u0f54\u0f0b\u0f62\u0f56\u0f0b\u0f42\u0f66\u0f63\u0f0b\u0f63\u0f66\u0f0b\u0f66\u0f7a\u0f58\u0f66\u0f0b\u0f56\u0f66\u0f90\u0fb1\u0f7a\u0f51\u0f0b\u0f51\u0fb2\u0f74\u0f42\u0f0b\u0f54\u0f0d \u0f64\u0f7c\u0f0b\u0f63\u0f7c\u0f0b\u0f40 \u0f21 \u0f53\u0f66\u0f0b \u0f26\u0f24",
        "en": "Illuminating the Intent Chapter 6",
    },
    "usage_title": {"en": "Illuminating the Intent Chapter 6"},
}

MetadataType = Dict[str, str | Dict[str, str] | Collection[str] | None]


class TestDocxParser(TestCase):
    def setUp(self):
        self.parser = DocxParser()

    def test_root_pecha(self):
        # this is the root pecha

        metadatas: list[MetadataType] = [
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert not self.parser.is_commentary_pecha(metadatas)

    def test_root_translation_pecha(self):
        # translation of root pecha
        metadatas: list[MetadataType] = [
            {
                "translation_of": "P0001",
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert not self.parser.is_commentary_pecha(metadatas)

    def test_commentary_pecha(self):
        metadatas: list[MetadataType] = [
            {
                "translation_of": None,
                "commentary_of": "P0001",
                "version_of": None,
                **extra_fields,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert self.parser.is_commentary_pecha(metadatas)

    def test_commentary_translation_pecha(self):
        # translation of commentary pecha
        metadatas: list[MetadataType] = [
            {
                "translation_of": "P0001",
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
            {
                "translation_of": None,
                "commentary_of": "P0002",
                "version_of": None,
                **extra_fields,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert self.parser.is_commentary_pecha(metadatas)

    def tearDown(self):
        pass
