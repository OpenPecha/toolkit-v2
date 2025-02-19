from typing import Dict, List, Union
from unittest import TestCase

from openpecha.pecha.serializers import PechaSerializer

extra_fields: Dict[str, Union[str, Dict[str, str], List[str], None]] = {
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

MetadataType = Dict[str, Union[str, Dict[str, str], List[str], None]]


class TestPechaSerializer(TestCase):
    def setUp(self):
        self.serializer = PechaSerializer()

    def test_choose_simple_commentary_serializer(self):
        metadatas: List[MetadataType] = [
            {
                "commentary_of": "P0001",
                "translation_of": None,
                **extra_fields,
            },
            {
                "commentary_of": None,
                "translation_of": None,
                **extra_fields,
            },
        ]
        self.assertTrue(self.serializer.is_commentary_pecha(metadatas))

    def test_choose_translation_serializer(self):
        metadatas: List[MetadataType] = [
            {
                "commentary_of": None,
                "translation_of": "P0001",
                **extra_fields,
            },
            {
                "commentary_of": None,
                "translation_of": None,
                **extra_fields,
            },
        ]
        self.assertFalse(self.serializer.is_commentary_pecha(metadatas))

    def test_is_root(self):
        metadatas: List[MetadataType] = [
            {
                "commentary_of": None,
                "translation_of": None,
                **extra_fields,
            }
        ]
        self.assertFalse(self.serializer.is_commentary_pecha(metadatas))

    def tearDown(self):
        pass
