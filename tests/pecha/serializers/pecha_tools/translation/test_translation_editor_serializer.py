from pathlib import Path
from typing import Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_tools import Serializer
from openpecha.utils import read_json

expected_root_serialized_json = read_json(
    "tests/pecha/serializers/pecha_tools/translation/data/serialized_root.json"
)
expected_root_translation_serialized_json = read_json(
    "tests/pecha/serializers/pecha_tools/translation/data/serialized_root_translation.json"
)
expected_commentary_serialized_json = read_json(
    "tests/pecha/serializers/pecha_tools/translation/data/serialized_commentary.json"
)

null = None


class TestSerializer(TestCase):
    def setUp(self):
        self.root_display_pecha = Pecha.from_path(
            Path(
                "tests/pecha/serializers/pecha_tools/translation/data/root/bo/IA6E66F92"
            )
        )
        self.root_pecha = Pecha.from_path(
            Path(
                "tests/pecha/serializers/pecha_tools/translation/data/root/bo/IE60BBDE8"
            )
        )
        self.root_translation_pecha = Pecha.from_path(
            Path(
                "tests/pecha/serializers/pecha_tools/translation/data/root/en/I62E00D78"
            )
        )
        self.commentary_pecha = Pecha.from_path(
            Path(
                "tests/pecha/serializers/pecha_tools/translation/data/commentary/bo/I6944984E"
            )
        )
        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            "annotations": [
                {
                    "annotaion_type": "segmentation",
                    "annotation_title": "test title",
                    "relationship": None,
                    "layer_name": "B8B3/segmentation-74F4.json",
                }
            ],
            **self.root_display_pecha.metadata.to_dict(),
        }
        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": "IA6E66F92",
            "annotations": [
                {
                    "annotaion_type": "segmentation",
                    "annotation_title": "test title",
                    "relationship": None,
                    "layer_name": "3635/segmentation-039B.json",
                }
            ],
            **self.root_pecha.metadata.to_dict(),
        }
        self.root_translation_pecha_metadata = {
            "translation_of": "IE60BBDE8",
            "commentary_of": None,
            "version_of": None,
            "annotations": [
                {
                    "annotaion_type": "Alignment",
                    "annotation_title": "test title",
                    "relationship": (
                        "translation_of",
                        "IE60BBDE8",
                        "3635/segmentation-039B.json",
                    ),
                    "layer_name": "E949/Alignment-2F29.json",
                }
            ],
            **self.root_translation_pecha.metadata.to_dict(),
        }
        self.commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
            "version_of": None,
            "annotations": [
                {
                    "annotaion_type": "Alignment",
                    "annotation_title": "test title",
                    "relationship": (
                        "commentary_of",
                        "IE60BBDE8",
                        "3635/segmentation-039B.json",
                    ),
                    "layer_name": "E949/Alignment-2F29.json",
                }
            ],
            **self.commentary_pecha.metadata.to_dict(),
        }

        self.pecha_category: List[Dict] = [
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Madhyamaka", "bo": "དབུ་མ།", "lzh": "中观"},
                "parent": None,
            },
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Madhyamaka treatises", "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།", "lzh": "中观论著"},
                "parent": "madhyamaka",
            },
        ]

    def test_root_pecha(self):
        pechas = [self.root_pecha]
        metadatas = [self.root_pecha_metadata]
        pecha_category = self.pecha_category
        layer_name = None
        editor_type = "translation"

        serializer = Serializer()
        root_serialized_json = serializer.serialize(
            pechas, metadatas, pecha_category, editor_type, layer_name
        )
        assert (
            root_serialized_json["base_text"]
            == expected_root_serialized_json["base_text"]
        )
        assert (
            root_serialized_json["annotations"]
            == expected_root_serialized_json["annotations"]
        )

    def test_root_translation_pecha(self):
        pechas = [self.root_translation_pecha, self.root_display_pecha]
        metadatas = [
            self.root_translation_pecha_metadata,
            self.root_display_pecha_metadata,
        ]
        pecha_category = self.pecha_category
        layer_name = None
        editor_type = "translation"

        serializer = Serializer()
        root_translation_serialized_json = serializer.serialize(
            pechas, metadatas, pecha_category, editor_type, layer_name
        )
        assert (
            root_translation_serialized_json["base_text"]
            == expected_root_translation_serialized_json["base_text"]
        )
        assert (
            root_translation_serialized_json["annotations"]
            == expected_root_translation_serialized_json["annotations"]
        )

    def test_commentary_pecha(self):
        pechas = [self.commentary_pecha, self.root_display_pecha]
        metadatas = [self.commentary_pecha_metadata, self.root_display_pecha_metadata]
        pecha_category = self.pecha_category
        layer_name = None
        editor_type = "translation"

        serializer = Serializer()
        commentary_serialized_json = serializer.serialize(
            pechas, metadatas, pecha_category, editor_type, layer_name
        )
        assert (
            commentary_serialized_json["base_text"]
            == expected_commentary_serialized_json["base_text"]
        )
        assert (
            commentary_serialized_json["annotations"]
            == expected_commentary_serialized_json["annotations"]
        )
