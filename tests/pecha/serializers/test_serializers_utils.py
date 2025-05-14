from unittest import TestCase

from openpecha.pecha.serializers.utils import (
    find_related_pecha_id,
    get_metadatachain_from_metadatatree,
)
from tests.pecha import DummyMetadataModel, SharedPechaSetup


def test_find_related_pecha_id():
    test_setup = SharedPechaSetup()
    test_setup.setup_pechas()

    # Test Root Pecha
    annotations = {
        test_setup.root_pecha.id: test_setup.root_pecha_annotations,
    }
    ann_path = test_setup.root_pecha_annotations[0].path
    assert find_related_pecha_id(annotations, ann_path) == test_setup.root_pecha.id

    # Test Root Translation Pecha
    annotations = {
        test_setup.root_translation_pecha.id: test_setup.root_translation_pecha_annotations,
        test_setup.root_pecha.id: test_setup.root_pecha_annotations,
    }
    ann_path = test_setup.root_translation_pecha_annotations[0].path
    assert (
        find_related_pecha_id(annotations, ann_path)
        == test_setup.root_translation_pecha.id
    )

    # Test Commentary Pecha
    annotations = {
        test_setup.commentary_pecha.id: test_setup.commentary_pecha_annotations,
        test_setup.root_pecha.id: test_setup.root_pecha_annotations,
    }
    ann_path = test_setup.commentary_pecha_annotations[0].path
    assert (
        find_related_pecha_id(annotations, ann_path) == test_setup.commentary_pecha.id
    )


class TestGetMetadataChain(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()

        # Set up `id` field in metadatas (Not included in Backend Db)
        self.root_pecha_metadata = DummyMetadataModel(
            **{
                "id": self.root_pecha.id,
                "translation_of": None,
                "commentary_of": None,
                **self.root_pecha.metadata.to_dict(),
            }
        )
        self.root_translation_pecha_metadata = DummyMetadataModel(
            **{
                "id": self.root_translation_pecha.id,
                "translation_of": self.root_pecha.id,
                "commentary_of": None,
                **self.root_translation_pecha.metadata.to_dict(),
            }
        )
        self.commentary_pecha_metadata = DummyMetadataModel(
            **{
                "id": self.commentary_pecha.id,
                "translation_of": None,
                "commentary_of": self.root_pecha.id,
                **self.commentary_pecha.metadata.to_dict(),
            }
        )
        self.commentary_translation_pecha_metadata = DummyMetadataModel(
            **{
                "id": self.commentary_translation_pecha.id,
                "translation_of": self.commentary_pecha.id,
                "commentary_of": None,
                **self.commentary_translation_pecha.metadata.to_dict(),
            }
        )

        self.metadatatree = [
            self.root_pecha_metadata,
            self.commentary_pecha_metadata,
            self.commentary_translation_pecha_metadata,
            self.root_translation_pecha_metadata,
        ]

    def test_root_pecha(self):
        metadatachain = get_metadatachain_from_metadatatree(
            self.metadatatree, self.root_pecha.id
        )
        assert metadatachain == [self.root_pecha_metadata]

    def test_root_translation(self):
        metadatachain = get_metadatachain_from_metadatatree(
            self.metadatatree, self.root_translation_pecha_metadata.id  # type: ignore
        )
        assert metadatachain == [
            self.root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]

    def test_commentary_pecha(self):
        metadatachain = get_metadatachain_from_metadatatree(
            self.metadatatree, self.commentary_pecha.id
        )
        assert metadatachain == [
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]

    def test_commentary_translation_pecha(self):
        metadatachain = get_metadatachain_from_metadatatree(
            self.metadatatree, self.commentary_translation_pecha.id
        )
        assert metadatachain == [
            self.commentary_translation_pecha_metadata,
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
