from pathlib import Path
from typing import Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.pecha_types import (
    PechaType,
    get_pecha_type,
    is_commentary_related_pecha,
    is_root_related_pecha,
)

extra_fields: Dict[str, str | Dict[str, str] | List[str] | None] = {
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

MetadataType = Dict[str, str | Dict[str, str] | List[str] | None]


class TestPechaType(TestCase):
    def setUp(self):
        self.root_display_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P1/IA6E66F92"
        )
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P2/IC7760088"
        )
        self.commentary_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P3/I77BD6EA9"
        )

        self.root_display_pecha = Pecha.from_path(self.root_display_pecha_path)
        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.commentary_pecha = Pecha.from_path(self.commentary_pecha_path)

        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_display_pecha.metadata.to_dict(),
        }
        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": self.root_display_pecha.id,
            **self.root_pecha.metadata.to_dict(),
        }
        self.commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": self.root_pecha.id,
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
        }

    def test_is_root_related_pecha(self):
        # Test root pecha types
        assert is_root_related_pecha(PechaType.root_pecha)
        assert is_root_related_pecha(PechaType.prealigned_root_translation_pecha)

        # Test non-root pecha types
        assert not is_root_related_pecha(PechaType.commentary_pecha)
        assert not is_root_related_pecha(PechaType.prealigned_commentary_pecha)

    def test_is_commentary_related_pecha(self):
        # Test commentary pecha types
        assert is_commentary_related_pecha(PechaType.commentary_pecha)
        assert is_commentary_related_pecha(PechaType.prealigned_commentary_pecha)

        # Test non-commentary pecha types
        assert not is_commentary_related_pecha(PechaType.root_pecha)
        assert not is_commentary_related_pecha(
            PechaType.prealigned_root_translation_pecha
        )

    def test_root_pecha(self):
        metadatas: list[MetadataType] = [
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert get_pecha_type(metadatas) == PechaType.root_pecha

    def test_root_translation_pecha(self):
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
        assert get_pecha_type(metadatas) == PechaType.root_translation_pecha

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
        assert get_pecha_type(metadatas) == PechaType.commentary_pecha

    def test_commentary_translation_pecha(self):
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
        assert get_pecha_type(metadatas) == PechaType.commentary_translation_pecha

    def test_prealigned_root_translation_pecha(self):
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
                "version_of": "P0002",
                **extra_fields,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert get_pecha_type(metadatas) == PechaType.prealigned_root_translation_pecha

    def test_prealigned_commentary_pecha(self):
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
                "version_of": "P0002",
                **extra_fields,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert get_pecha_type(metadatas) == PechaType.prealigned_commentary_pecha

    def test_prealigned_commentary_translation_pecha(self):
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
                "version_of": "P0003",
                **extra_fields,
            },
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert (
            get_pecha_type(metadatas)
            == PechaType.prealigned_commentary_translation_pecha
        )
