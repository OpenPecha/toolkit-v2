from pathlib import Path
from unittest import TestCase, mock

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel, PechaAlignment
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.serializers.pecha_db import Serializer

null = None


class TestSerializer(TestCase):
    def setUp(self):
        self.root_display_pecha = Pecha.from_path(
            Path("tests/alignment/commentary_transfer/data/P1/IA6E66F92")
        )
        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_display_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="IA6E66F92",
                    type=LayerEnum.segmentation,
                    document_id="d1",
                    id="B8B3/Segmentation-74F4.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤",
                    aligned_to=None,
                )
            ],
        }
        self.root_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/bo/IE60BBDE8")
        )
        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": "IA6E66F92",
            **self.root_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="IE60BBDE8",
                    type=LayerEnum.alignment,
                    document_id="d2",
                    id="3635/Segmentation-039B.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1",
                    aligned_to=PechaAlignment(
                        pecha_id="IA6E66F92", alignment_id="B8B3/Segmentation-74F4.json"
                    ),
                )
            ],
        }

        self.root_translation_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/en/I62E00D78")
        )
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

        self.commentary_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/commentary/simple/data/bo/I6944984E")
        )
        self.commentary_pecha_metadata = {
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
                        pecha_id="IE60BBDE8", alignment_id="3635/Segmentation-039B.json"
                    ),
                )
            ],
        }

        self.commentary_translation_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/commentary/simple/data/en/I94DBDA91")
        )
        self.commentary_translation_pecha_metadata = {
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
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                    aligned_to=PechaAlignment(
                        pecha_id="I6944984E", alignment_id="E949/Alignment-2F29.json"
                    ),
                )
            ],
        }
        self.pecha_category = [
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

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_pecha, self.pecha_category
        )

    @mock.patch("openpecha.pecha.serializers.pecha_db.root.RootSerializer.serialize")
    def test_root_translation_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_translation_pecha, self.root_display_pecha]
        metadatas = [
            self.root_translation_pecha_metadata,
            self.root_display_pecha_metadata,
        ]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_display_pecha,
            self.pecha_category,
            self.root_translation_pecha,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.simple_commentary.SimpleCommentarySerializer.serialize"
    )
    def test_commentary_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}
        pechas = [self.commentary_pecha, self.root_display_pecha]
        metadatas = [self.commentary_pecha_metadata, self.root_display_pecha_metadata]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_pecha,
            self.pecha_category,
            self.root_display_pecha.metadata.title["EN"],
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.simple_commentary.SimpleCommentarySerializer.serialize"
    )
    def test_commentary_translation_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}
        pechas = [
            self.commentary_translation_pecha,
            self.commentary_pecha,
            self.root_display_pecha,
        ]
        metadatas = [
            self.commentary_translation_pecha_metadata,
            self.commentary_pecha_metadata,
            self.root_display_pecha_metadata,
        ]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_pecha,
            self.pecha_category,
            self.root_display_pecha.metadata.title["EN"],
            self.commentary_translation_pecha,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary.PreAlignedCommentarySerializer.serialize"
    )
    def test_prealigned_commentary_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}
        pechas = [self.commentary_pecha, self.root_pecha, self.root_display_pecha]
        metadatas = [
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
            self.root_display_pecha_metadata,
        ]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.root_display_pecha,
            self.root_pecha,
            self.commentary_pecha,
            self.pecha_category,
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.prealigned_root_translation.PreAlignedRootTranslationSerializer.serialize"
    )
    def test_prealigned_root_translation_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_translation_pecha, self.root_pecha, self.root_display_pecha]
        metadatas = [
            self.root_translation_pecha_metadata,
            self.root_pecha_metadata,
            self.root_display_pecha_metadata,
        ]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas, self.pecha_category)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_display_pecha,
            self.root_pecha,
            self.root_translation_pecha,
            self.pecha_category,
        )
