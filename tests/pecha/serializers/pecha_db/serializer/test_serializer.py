from typing import Dict, List
from unittest import TestCase, mock

from openpecha.pecha.serializers.pecha_db import Serializer
from tests.pecha import SharedPechaSetup

null = None


class TestSerializer(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()
        self.pecha_category: List[Dict] = [
            {
                "description": {"en": "", "bo": ""},
                "short_description": {"en": "", "bo": ""},
                "name": {"en": "Madhyamaka", "bo": "དབུ་མ།"},
                "parent": null,
            },
            {
                "description": {"en": "", "bo": ""},
                "short_description": {"en": "", "bo": ""},
                "name": {"en": "Madhyamaka treatises", "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།"},
                "parent": "madhyamaka",
            },
        ]

    @mock.patch("openpecha.pecha.serializers.pecha_db.root.RootSerializer.serialize")
    def test_root_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_pecha]
        metadatas = [self.root_pecha_metadata]
        annotation_id = "B8B3/Segmentation-74F4.json"

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category, annotation_id)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha, annotation_id, self.pecha_category
        )

    @mock.patch("openpecha.pecha.serializers.pecha_db.root.RootSerializer.serialize")
    def test_root_translation_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_translation_pecha, self.root_pecha]
        metadatas = [
            self.root_translation_pecha_metadata,
            self.root_pecha_metadata,
        ]
        annotation_id = "D93E/Alignment-0216.json"
        root_ann_id = "B8B3/Segmentation-74F4.json"

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category, annotation_id)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha,
            root_ann_id,
            self.pecha_category,
            self.root_translation_pecha,
            annotation_id,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.simple_commentary.SimpleCommentarySerializer.serialize"
    )
    def test_commentary_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}
        pechas = [self.commentary_pecha, self.root_pecha]
        metadatas = [self.commentary_pecha_metadata, self.root_pecha_metadata]

        annotation_id = "E949/Alignment-2F29.json"

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category, annotation_id)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_pecha,
            annotation_id,
            self.pecha_category,
            self.root_pecha.metadata.title["EN"],
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

        translation_ann_id = "FD22/Alignment-599A.json"
        annotation_id = "E949/Alignment-2F29.json"

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category, translation_ann_id)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_pecha,
            annotation_id,
            self.pecha_category,
            self.root_pecha.metadata.title["EN"],
            self.commentary_translation_pecha,
            translation_ann_id,
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

        annotation_id = "E949/Alignment-2F29.json"
        root_alignment_id = "B8B3/Alignment-F81A.json"

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category, annotation_id)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.root_pecha,
            root_alignment_id,
            self.commentary_pecha,
            annotation_id,
            self.pecha_category,
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

        annotation_id = "D93E/Alignment-0216.json"
        root_alignment_id = "B8B3/Alignment-F81A.json"

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category, annotation_id)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha,
            root_alignment_id,
            self.root_translation_pecha,
            self.pecha_category,
        )
