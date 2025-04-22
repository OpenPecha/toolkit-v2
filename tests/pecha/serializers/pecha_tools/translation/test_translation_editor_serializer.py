from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_tools import Serializer
from openpecha.utils import write_json, read_json

expected_root_serialized_json = read_json("tests/pecha/serializers/pecha_tools/translation/data/serialized_root.json")
null = None

class TestTranslationSerializer(TestCase):
    def setUp(self):
        self.root_display_pecha = Pecha.from_path(
            Path("tests/alignment/commentary_transfer/data/P1/IA6E66F92")
        )
        self.root_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/bo/IE60BBDE8")
        )
        self.root_translation_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/pecha_db/root/data/en/I62E00D78")
        )
        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_display_pecha.metadata.to_dict(),
        }
        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": "IA6E66F92",
            "annotations": [
                {
                    "annotaion_type": "Segmentation",
                    "annotation_title": "test title",
                    "relationship": None,
                    "layer_name": "3635/Tibetan_Segment-039B.json"
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
                        "translation_of", "IE60BBDE8", "3635/Tibetan_Segment-039B.json" ),
                    "layer_name": "D93E/English_Segment-0216.json"
                }
            ],
            **self.root_translation_pecha.metadata.to_dict(),
        }
        self.pecha_category = [
            {
                "description": {
                    "en": "",
                    "bo": ""
                },
                "short_description": {
                    "en": "",
                    "bo": ""
                },
                "name": {
                    "en": "Madhyamaka",
                    "bo": "དབུ་མ།"
                },
                "parent": null
            },
            {
                "description": {
                    "en": "",
                    "bo": ""
                },
                "short_description": {
                    "en": "",
                    "bo": ""
                },
                "name": {
                    "en": "Madhyamaka treatises",
                    "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།"
                },
                "parent": "madhyamaka"
            }
        ]
        
    def test_root_pecha(self):
        pechas = [self.root_pecha]
        metadatas = [self.root_pecha_metadata]
        pecha_category = self.pecha_category
        layer_name = None
        editor_type = "translation"

        serializer = Serializer()
        root_serialized_json = serializer.serialize(pechas, metadatas, pecha_category, editor_type, layer_name)
        assert root_serialized_json == expected_root_serialized_json
        

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
        root_translation_serialized_json = serializer.serialize(pechas, metadatas, pecha_category, editor_type, layer_name)
        write_json("tests/pecha/serializers/pecha_tools/translation/data/serialized_root_translation.json", root_translation_serialized_json)
        # assert root_translation_serialized_json == expected_root_translation_serialized_json

    # @mock.patch(
    #     "openpecha.pecha.serializers.pecha_db.commentary.simple_commentary.SimpleCommentarySerializer.serialize"
    # )
    # def test_commentary_pecha(self, mock_commentary_serialize):
    #     mock_commentary_serialize.return_value = {}
    #     pechas = [self.commentary_pecha, self.root_display_pecha]
    #     metadatas = [self.commentary_pecha_metadata, self.root_display_pecha_metadata]

    #     serializer = Serializer()
    #     serializer.serialize(pechas, metadatas, self.pecha_category)

    #     mock_commentary_serialize.assert_called_once()
    #     mock_commentary_serialize.assert_called_with(
    #         self.commentary_pecha,
    #         self.pecha_category,
    #         self.root_display_pecha.metadata.title["EN"],
    #     )

if __name__ == "__main__":
    test_serializer = TestTranslationSerializer()
    test_serializer.setUp()
    test_serializer.test_root_translation_pecha()