from typing import Dict, List
from unittest import TestCase, mock

from openpecha.pecha.serializers.pecha_db import Serializer
from openpecha.pecha.serializers.pecha_db.utils import FormatPechaCategory
from tests.pecha import SharedPechaSetup

null = None


class TestSerializer(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()
        self.pecha_category: List[Dict] = [
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Madhyamaka", "bo": "དབུ་མ།", "lzh": "中观"},
                "parent": null,
            },
            {
                "description": null,
                "short_description": null,
                "name": {
                    "en": "Madhyamaka treatises",
                    "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།",
                    "lzh": "中观论著",
                },
                "parent": "madhyamaka",
            },
        ]

    @mock.patch("openpecha.pecha.serializers.pecha_db.root.RootSerializer.serialize")
    def test_root_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_pecha]
        metadatas = [self.root_pecha_metadata]
        annotations = {self.root_pecha.id: self.root_pecha_annotations}
        annotation_path = "B8B3/segmentation-74F4.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, annotation_path
        )

        formmatted_category = FormatPechaCategory().format_root_category(
            self.root_pecha, self.pecha_category
        )
        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha, annotation_path, formmatted_category
        )

    @mock.patch("openpecha.pecha.serializers.pecha_db.root.RootSerializer.serialize")
    def test_root_translation_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_translation_pecha, self.root_pecha]
        metadatas = [
            self.root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.root_translation_pecha.id: self.root_translation_pecha_annotations,
        }
        annotation_path = "D93E/alignment-0216.json"
        root_ann_path = "B8B3/segmentation-74F4.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, annotation_path
        )

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha,
            root_ann_path,
            self.pecha_category,
            self.root_translation_pecha,
            annotation_path,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.simple_commentary.SimpleCommentarySerializer.serialize"
    )
    def test_commentary_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}
        pechas = [self.commentary_pecha, self.root_pecha]
        metadatas = [self.commentary_pecha_metadata, self.root_pecha_metadata]
        annotations = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.commentary_pecha_annotations,
        }
        annotation_path = "BEC3/alignment-90C0.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, annotation_path
        )

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_pecha,
            annotation_path,
            self.pecha_category,
            self.root_pecha.metadata.title["en"],
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.simple_commentary.SimpleCommentarySerializer.serialize"
    )
    def test_commentary_translation_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}
        pechas = [
            self.commentary_translation_pecha,
            self.commentary_pecha,
            self.root_pecha,
        ]
        metadatas = [
            self.commentary_translation_pecha_metadata,
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.commentary_pecha_annotations,
            self.commentary_translation_pecha.id: self.commentary_translation_pecha_annotations,
        }
        translation_ann_path = "FD22/alignment-599A.json"
        annotation_path = "BEC3/alignment-90C0.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, translation_ann_path
        )

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_pecha,
            annotation_path,
            self.pecha_category,
            self.root_pecha.metadata.title["en"],
            self.commentary_translation_pecha,
            translation_ann_path,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary.PreAlignedCommentarySerializer.serialize"
    )
    def test_prealigned_commentary_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}

        pechas = [self.commentary_pecha, self.root_pecha]
        metadatas = [
            self.prealigned_commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.prealigned_commentary_pecha_annotations,
        }

        annotation_path = "E949/alignment-2F29.json"
        root_alignment_path = "B8B3/alignment-F81A.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, annotation_path
        )

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.root_pecha,
            root_alignment_path,
            self.commentary_pecha,
            annotation_path,
            self.pecha_category,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary.PreAlignedCommentarySerializer.serialize"
    )
    def test_prealigned_commentary_segmentation_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}

        pechas = [self.commentary_pecha, self.root_pecha]
        metadatas = [
            self.prealigned_commentary_segmentation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.commentary_pecha.id: self.prealigned_commentary_segmentation_pecha_annotations,
        }

        annotation_path = "E949/alignment-2F29.json"
        root_alignment_path = "B8B3/alignment-F81A.json"
        commentary_segmentation_path = "E949/segmentation-2134.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, annotation_path
        )

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.root_pecha,
            root_alignment_path,
            self.commentary_pecha,
            annotation_path,
            self.pecha_category,
            commentary_segmentation_path,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.prealigned_root_translation.PreAlignedRootTranslationSerializer.serialize"
    )
    def test_prealigned_root_translation_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_translation_pecha, self.root_pecha]
        metadatas = [
            self.prealigned_root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.root_translation_pecha.id: self.prealigned_root_translation_pecha_annotations,
        }

        annotation_path = "D93E/alignment-0216.json"
        root_alignment_path = "B8B3/alignment-F81A.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, annotation_path
        )

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha,
            root_alignment_path,
            self.root_translation_pecha,
            annotation_path,
            self.pecha_category,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.prealigned_root_translation.PreAlignedRootTranslationSerializer.serialize"
    )
    def test_prealigned_root_translation_segmentation_pecha(
        self, mock_translation_serialize
    ):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_translation_pecha, self.root_pecha]
        metadatas = [
            self.prealigned_root_translation_segmentation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotations = {
            self.root_pecha.id: self.root_pecha_annotations,
            self.root_translation_pecha.id: self.prealigned_root_translation_segmentation_pecha_annotations,
        }

        annotation_path = "D93E/alignment-0216.json"
        root_alignment_path = "B8B3/alignment-F81A.json"
        translation_segmentation_id = "D93E/segmentation-2143.json"

        serializer = Serializer()
        serializer.serialize(
            pechas, metadatas, annotations, self.pecha_category, annotation_path
        )

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha,
            root_alignment_path,
            self.root_translation_pecha,
            annotation_path,
            self.pecha_category,
            translation_segmentation_id,
        )
