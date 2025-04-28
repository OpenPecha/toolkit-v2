from typing import Dict, List
from unittest import TestCase

from openpecha.pecha.annotations import AnnotationModel, PechaAlignment
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.pecha_types import (
    PechaType,
    get_pecha_type,
    is_commentary_related_pecha,
    is_root_related_pecha,
)
from tests.pecha import SharedPechaSetup

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
        root_translation_pecha_metadata = {
            "translation_of": "IE60BBDE8",
            "commentary_of": None,
            "version_of": None,
            **self.root_translation_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I62E00D78",
                    type=LayerEnum.alignment,
                    document_id="d3",
                    id="D93E/Alignment-0216.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ translation 1",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Segmentation-74F4.json"
                    ),
                )
            ],
        }

        metadatas: list[MetadataType] = [
            root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.root_translation_pecha

    def test_commentary_pecha(self):
        commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I6944984E",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="E949/Alignment-2F29.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Segmentation-74F4.json"
                    ),
                )
            ],
        }
        metadatas: list[MetadataType] = [
            commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.commentary_pecha

    def test_commentary_translation_pecha(self):
        commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I6944984E",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="E949/Alignment-2F29.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Segmentation-74F4.json"
                    ),
                )
            ],
        }
        metadatas: list[MetadataType] = [
            self.commentary_translation_pecha_metadata,
            commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.commentary_translation_pecha

    def test_prealigned_root_translation_pecha(self):
        root_translation_pecha_metadata = {
            "translation_of": "IE60BBDE8",
            "commentary_of": None,
            "version_of": None,
            **self.root_translation_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I62E00D78",
                    type=LayerEnum.alignment,
                    document_id="d3",
                    id="D93E/Alignment-0216.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ translation 1",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Alignment-F81A.json"
                    ),
                )
            ],
        }
        metadatas: list[MetadataType] = [
            root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.prealigned_root_translation_pecha

    def test_prealigned_commentary_pecha(self):
        commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I6944984E",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="E949/Alignment-2F29.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Alignment-F81A.json"
                    ),
                )
            ],
        }
        metadatas: list[MetadataType] = [
            commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert get_pecha_type(metadatas) == PechaType.prealigned_commentary_pecha

    def test_prealigned_commentary_translation_pecha(self):
        commentary_translation_pecha_metadata = {
            "translation_of": "I6944984E",
            "commentary_of": None,
            "version_of": None,
            **self.commentary_translation_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I94DBDA91",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="FD22/Alignment-599A.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary translation",
                    aligned_to=PechaAlignment(
                        pecha_id="I6944984E", alignment_id="E949/Alignment-2F29.json"
                    ),
                )
            ],
        }
        commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I6944984E",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="E949/Alignment-2F29.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Alignment-F81A.json"
                    ),
                )
            ],
        }
        metadatas: list[MetadataType] = [
            commentary_translation_pecha_metadata,
            commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        assert (
            get_pecha_type(metadatas)
            == PechaType.prealigned_commentary_translation_pecha
        )
