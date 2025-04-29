from typing import Dict, List
from unittest import TestCase

from openpecha.pecha.pecha_types import (
    PechaType,
    get_pecha_type,
    is_commentary_related_pecha,
    is_root_related_pecha,
)
from tests.pecha import SharedPechaSetup

MetadataType = Dict[str, str | Dict[str, str] | List[str] | None]


class TestPechaType(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()

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
        metadatas: list[MetadataType] = [self.root_pecha_metadata]
        assert get_pecha_type(metadatas) == PechaType.root_pecha

    def test_root_translation_pecha(self):
        metadatas: list[MetadataType] = [
            self.root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.root_translation_pecha

    def test_commentary_pecha(self):
        metadatas: list[MetadataType] = [
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.commentary_pecha

    def test_commentary_translation_pecha(self):
        metadatas: list[MetadataType] = [
            self.commentary_translation_pecha_metadata,
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.commentary_translation_pecha

    def test_prealigned_root_translation_pecha(self):
        metadatas: list[MetadataType] = [
            self.prealigned_root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.prealigned_root_translation_pecha

    def test_prealigned_commentary_pecha(self):
        metadatas: list[MetadataType] = [
            self.prealigned_commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.prealigned_commentary_pecha

    def test_prealigned_commentary_translation_pecha(self):

        metadatas: list[MetadataType] = [
            self.prealigned_commentary_translation_pecha_metadata,
            self.prealigned_commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert (
            get_pecha_type(metadatas)
            == PechaType.prealigned_commentary_translation_pecha
        )
