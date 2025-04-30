from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"
null = None


class TestRootSerializer(TestCase):
    def setUp(self):
        self.pecha_category = [
            {
                "description": {"en": "", "bo": ""},
                "short_description": {"en": "", "bo": ""},
                "name": {"en": "The Buddha's Teachings", "bo": "སངས་རྒྱས་ཀྱི་བཀའ།"},
                "parent": null,
            },
            {
                "description": {"en": "", "bo": ""},
                "short_description": {"en": "", "bo": ""},
                "name": {"en": "Vajra Cutter", "bo": "རྡོ་རྗེ་གཅོད་པ།"},
                "parent": "the-buddha's-teachings",
            },
        ]

    def test_root_pecha(self):
        root_opf = DATA_DIR / "bo/IE60BBDE8"
        root_pecha = Pecha.from_path(root_opf)
        ann_id = "3635/segmentation-039B.json"

        serializer = RootSerializer()
        json_output = serializer.serialize(
            pecha=root_pecha, ann_id=ann_id, pecha_category=self.pecha_category
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
