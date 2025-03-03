from pathlib import Path
from typing import Dict, List, Union
from unittest import TestCase, mock

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db import Serializer

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


class TestSerializerIsCommentary(TestCase):
    def setUp(self):
        self.serializer = Serializer()

    def test_root_pecha(self):
        # this is the root pecha

        metadatas: list[MetadataType] = [
            {
                "translation_of": None,
                "commentary_of": None,
                "version_of": None,
                **extra_fields,
            },
        ]
        assert not self.serializer.is_commentary_pecha(metadatas)

    def test_root_translation_pecha(self):
        # translation of root pecha
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
        assert not self.serializer.is_commentary_pecha(metadatas)

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
        assert self.serializer.is_commentary_pecha(metadatas)

    def test_commentary_translation_pecha(self):
        # translation of commentary pecha
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
        assert self.serializer.is_commentary_pecha(metadatas)


class TestSerializer(TestCase):
    def setUp(self):
        self.root_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/bo/IE60BBDE8")
        )
        self.root_translation_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/en/I62E00D78")
        )
        self.commentary_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/commentary/simple/data/bo/I6944984E")
        )
        self.commentary_translation_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/commentary/simple/data/en/I94DBDA91")
        )
        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_pecha.metadata.to_dict(),
        }
        self.root_translation_pecha_metadata = {
            "translation_of": "IE60BBDE8",
            "commentary_of": None,
            "version_of": None,
            **self.root_translation_pecha.metadata.to_dict(),
        }
        self.commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
        }
        self.commentary_translation_pecha_metadata = {
            "translation_of": "I6944984E",
            "commentary_of": None,
            "version_of": None,
            **self.commentary_translation_pecha.metadata.to_dict(),
        }

    @mock.patch("openpecha.pecha.serializers.pecha_db.root.RootSerializer.serialize")
    def test_root_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_pecha]
        metadatas = [self.root_pecha_metadata]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(self.root_pecha, None)

    @mock.patch("openpecha.pecha.serializers.pecha_db.root.RootSerializer.serialize")
    def test_root_translation_pecha(self, mock_translation_serialize):
        mock_translation_serialize.return_value = {}

        pechas = [self.root_translation_pecha, self.root_pecha]
        metadatas = [self.root_translation_pecha_metadata, self.root_pecha_metadata]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas)

        mock_translation_serialize.assert_called_once()
        mock_translation_serialize.assert_called_with(
            self.root_translation_pecha, self.root_pecha
        )

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.simple_commentary.SimpleCommentarySerializer.serialize"
    )
    def test_commentary_pecha(self, mock_commentary_serialize):
        mock_commentary_serialize.return_value = {}
        pechas = [self.commentary_pecha, self.root_pecha]
        metadatas = [self.commentary_pecha_metadata, self.root_pecha_metadata]

        serializer = Serializer()
        serializer.serialize(pechas, metadatas)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_pecha, self.root_pecha.metadata.title["EN"]
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

        serializer = Serializer()
        serializer.serialize(pechas, metadatas)

        mock_commentary_serialize.assert_called_once()
        mock_commentary_serialize.assert_called_with(
            self.commentary_translation_pecha,
            self.root_pecha.metadata.title["EN"],
            self.commentary_pecha,
        )
