from pathlib import Path
from typing import Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"
null = None


class TestRootSerializer(TestCase):
    def setUp(self):
        self.pecha_category: List[Dict] = [
            {
                "description": null,
                "short_description": null,
                "name": {
                    "en": "The Buddha's Teachings",
                    "bo": "སངས་རྒྱས་ཀྱི་བཀའ།",
                    "lzh": "佛陀教法",
                },
                "parent": null,
            },
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Vajra Cutter", "bo": "རྡོ་རྗེ་གཅོད་པ།", "lzh": "金刚经"},
                "parent": "the-buddha's-teachings",
            },
        ]

    def test_root_pecha(self):
        root_opf = DATA_DIR / "bo/IBA6E9270"
        root_pecha = Pecha.from_path(root_opf)
        ann_id = "EE99/segmentation-2A8C.json"

        serializer = RootSerializer()
        json_output = serializer.serialize(
            pecha=root_pecha, ann_id=ann_id, pecha_category=self.pecha_category
        )
        expected_json_path = DATA_DIR / "expected_root_output.json"
        assert json_output == read_json(expected_json_path)

    def test_root_translation_pecha(self):
        root_opf = DATA_DIR / "bo/IBA6E9270"
        translation_opf = DATA_DIR / "en/I5003D420"

        root_pecha = Pecha.from_path(root_opf)
        translation_pecha = Pecha.from_path(translation_opf)

        ann_id = "EE99/segmentation-2A8C.json"
        translation_ann_id = "9813/alignment-AE0B.json"

        serializer = RootSerializer()
        json_output = serializer.serialize(
            root_pecha,
            ann_id,
            self.pecha_category,
            translation_pecha,
            translation_ann_id,
        )

        expected_json_path = DATA_DIR / "expected_translation_output.json"
        assert json_output == read_json(expected_json_path)
