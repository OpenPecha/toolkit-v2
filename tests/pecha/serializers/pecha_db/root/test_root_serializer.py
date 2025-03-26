from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.root import RootSerializer
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"


class TestTranslationSerializer(TestCase):
    def setUp(self):
        self.category = {
            "bo": [
                {"name": "སངས་རྒྱས་ཀྱི་བཀའ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "འགྲེལ་པ།", "heDesc": "", "heShortDesc": ""},
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
            ],
            "en": [
                {"name": "The Buddha's Teachings", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
                {"name": "Commentaries", "enDesc": "", "enShortDesc": ""},
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
            ],
        }

    def test_root_pecha(self):
        root_opf = DATA_DIR / "bo/IE60BBDE8"
        root_pecha = Pecha.from_path(root_opf)

        serializer = RootSerializer()
        json_output = serializer.serialize(
            pecha=root_pecha, pecha_category=self.category
        )

        expected_json_path = DATA_DIR / "expected_root_output.json"
        assert json_output == read_json(expected_json_path)

    def test_root_translation_pecha(self):
        root_opf = DATA_DIR / "bo/IE60BBDE8"
        translation_opf = DATA_DIR / "en/I62E00D78"

        root_pecha = Pecha.from_path(root_opf)
        translation_pecha = Pecha.from_path(translation_opf)

        serializer = RootSerializer()
        json_output = serializer.serialize(
            pecha=translation_pecha,
            root_pecha=root_pecha,
            pecha_category=self.category,
        )

        expected_json_path = DATA_DIR / "expected_translation_output.json"
        assert json_output == read_json(expected_json_path)

    def tearDown(self):
        pass
