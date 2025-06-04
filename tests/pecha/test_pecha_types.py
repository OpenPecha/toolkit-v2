from typing import List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel
from openpecha.pecha.pecha_types import PechaType, get_pecha_type
from tests.pecha import DummyMetadataModel, SharedPechaSetup


class TestPechaType(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()

    def test_root_pecha(self):
        pechas: list[Pecha] = [self.root_pecha]
        metadatas: list[DummyMetadataModel] = [self.root_pecha_metadata]
        annotations: dict[str, List[AnnotationModel]] = {
            self.root_pecha.id: self.root_pecha_annotations
        }
        annotation_path = "B8B3/segmentation-74F4.json"

        assert (
            get_pecha_type(pechas, metadatas, annotations, annotation_path)
            == PechaType.root_pecha
        )

    def test_root_translation_pecha(self):
        pechas: list[Pecha] = [self.root_translation_pecha, self.root_pecha]
        metadatas: list[DummyMetadataModel] = [
            self.root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations: dict[str, List[AnnotationModel]] = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.root_translation_pecha.id: self.root_translation_pecha_annotations,
        }
        annotation_path = "9813/alignment-AE0B.json"

        assert (
            get_pecha_type(pechas, metadatas, annotations, annotation_path)
            == PechaType.root_translation_pecha
        )

    def test_commentary_pecha(self):
        pechas: list[Pecha] = [self.commentary_pecha, self.root_pecha]
        metadatas: list[DummyMetadataModel] = [
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations: dict[str, List[AnnotationModel]] = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.commentary_pecha_annotations,
        }
        annotation_path = "BEC3/alignment-90C0.json"

        assert (
            get_pecha_type(pechas, metadatas, annotations, annotation_path)
            == PechaType.commentary_pecha
        )

    def test_commentary_translation_pecha(self):
        pechas: list[Pecha] = [
            self.commentary_translation_pecha,
            self.commentary_pecha,
            self.root_pecha,
        ]
        metadatas: list[DummyMetadataModel] = [
            self.commentary_translation_pecha_metadata,
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations: dict[str, List[AnnotationModel]] = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.commentary_pecha_annotations,
            self.commentary_translation_pecha.id: self.commentary_translation_pecha_annotations,
        }
        annotation_path = "EB60/alignment-6786.json"
        assert (
            get_pecha_type(pechas, metadatas, annotations, annotation_path)
            == PechaType.commentary_translation_pecha
        )

    def test_prealigned_root_translation_pecha(self):
        pechas: list[Pecha] = [self.root_translation_pecha, self.root_pecha]
        metadatas: list[DummyMetadataModel] = [
            self.prealigned_root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations: dict[str, List[AnnotationModel]] = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.root_translation_pecha.id: self.prealigned_root_translation_pecha_annotations,
        }
        annotation_path = "D93E/alignment-0216.json"
        assert (
            get_pecha_type(pechas, metadatas, annotations, annotation_path)
            == PechaType.prealigned_root_translation_pecha
        )

    def test_prealigned_commentary_pecha(self):
        pechas: list[Pecha] = [self.commentary_pecha, self.root_pecha]
        metadatas: list[DummyMetadataModel] = [
            self.prealigned_commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations: dict[str, List[AnnotationModel]] = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.prealigned_commentary_pecha_annotations,
        }
        annotation_path = "E949/alignment-2F29.json"
        assert (
            get_pecha_type(pechas, metadatas, annotations, annotation_path)
            == PechaType.prealigned_commentary_pecha
        )

    def test_prealigned_commentary_translation_pecha(self):
        pechas: list[Pecha] = [
            self.prealigned_commentary_translation_pecha,
            self.commentary_pecha,
            self.root_pecha,
        ]
        metadatas: list[DummyMetadataModel] = [
            self.prealigned_commentary_translation_pecha_metadata,
            self.prealigned_commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations: dict[str, List[AnnotationModel]] = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.prealigned_commentary_pecha_annotations,
            self.prealigned_commentary_translation_pecha.id: self.prealigned_commentary_translation_pecha_annotations,
        }
        annotation_path = "757D/alignment-C2B5.json"
        assert (
            get_pecha_type(pechas, metadatas, annotations, annotation_path)
            == PechaType.prealigned_commentary_translation_pecha
        )
