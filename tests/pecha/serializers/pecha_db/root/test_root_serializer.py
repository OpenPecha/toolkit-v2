from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.pecha.serializers.pecha_db.utils import FormatPechaCategory
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"
null = None


class TestRootSerializer(TestCase):
    def setUp(self):
        self.pecha_category: List[Dict[Any, Any]] = [
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
        root_opf = DATA_DIR / "bo/IE60BBDE8"
        root_pecha = Pecha.from_path(root_opf)
        ann_id = "3635/segmentation-039B.json"

        serializer = RootSerializer()

        formmated_category = FormatPechaCategory().format_root_category(
            root_pecha, self.pecha_category
        )
        json_output = serializer.serialize(
            pecha=root_pecha, ann_id=ann_id, pecha_category=formmated_category
        )
        expected_json_path = DATA_DIR / "expected_root_output.json"
        assert json_output == read_json(expected_json_path)

    def test_root_translation_pecha(self):
        root_opf = DATA_DIR / "bo/IE60BBDE8"
        translation_opf = DATA_DIR / "en/I62E00D78"

        root_pecha = Pecha.from_path(root_opf)
        translation_pecha = Pecha.from_path(translation_opf)

        ann_id = "3635/segmentation-039B.json"
        translation_ann_id = "D93E/alignment-0216.json"

        formmated_category = FormatPechaCategory().format_root_category(
            root_pecha, self.pecha_category
        )

        serializer = RootSerializer()
        json_output = serializer.serialize(
            root_pecha,
            ann_id,
            formmated_category,
            translation_pecha,
            translation_ann_id,
        )

        expected_json_path = DATA_DIR / "expected_translation_output.json"
        assert json_output == read_json(expected_json_path)
