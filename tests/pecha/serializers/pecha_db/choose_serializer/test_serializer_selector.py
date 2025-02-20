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
        "bo": "མངོན་དུ་ཕྱོགས་པར་མཉམ་བཞག་སེམས་གནས་ཏེ།",
        "en": "Illuminating the Intent Chapter 6",
    },
    "usage_title": {"en": "Illuminating the Intent Chapter 6"},
}

MetadataType = Dict[str, Union[str, Dict[str, str], List[str], None]]


class TestPechaSerializer(TestCase):
    def setUp(self):
        self.serializer = PechaSerializer()

    def test_simple_commentary_serializer(self):
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

    def test_translation_serializer(self):
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

    def test_commentary_translation_pecha(self):
        metadatas: List[MetadataType] = [
            {
                "commentary_of": "P0001",
                "translation_of": None,
                **extra_fields,
            },
            {
                "commentary_of": None,
                "translation_of": "P0002",
                **extra_fields,
            },
            {
                "commentary_of": None,
                "translation_of": None,
                **extra_fields,
            },
        ]
        self.assertTrue(self.serializer.is_commentary_pecha(metadatas))

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
