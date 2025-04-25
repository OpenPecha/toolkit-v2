from pathlib import Path
from typing import Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel, PechaAlignment
from openpecha.pecha.layer import LayerEnum
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
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/root/IA6E66F92"
        )
        self.root_translation_pecha_path = Path(
            "tests/pecha/serializers/pecha_db/root/data/en/I62E00D78"
        )
        self.commentary_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/commentary/I77BD6EA9"
        )

        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.root_translation_pecha = Pecha.from_path(self.root_translation_pecha_path)
        self.commentary_pecha = Pecha.from_path(self.commentary_pecha_path)

        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="IA6E66F92",
                    type=LayerEnum.segmentation,
                    document_id="d2",
                    id="B8B3/Segmentation-74F4.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation",
                    aligned_to=None,
                ),
                AnnotationModel(
                    pecha_id="IA6E66F92",
                    type=LayerEnum.segmentation,
                    document_id="d2",
                    id="B8B3/Alignment-F81A.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ alignment",
                    aligned_to=None,
                ),
            ],
        }
        self.root_translation_pecha_metadata = {
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
                        pecha_id="IE60BBDE8", alignment_id="3635/Segmentation-039B.json"
                    ),
                )
            ],
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


work = TestPechaType()
work.setUp()
work.test_root_pecha()
work.test_root_translation_pecha()
work.test_commentary_pecha()
