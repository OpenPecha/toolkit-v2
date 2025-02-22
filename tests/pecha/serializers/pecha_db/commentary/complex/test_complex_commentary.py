from pathlib import Path
from unittest import TestCase, mock

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.complex_commentary import (
    ComplexCommentarySerializer,
)
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"

MOCK_BO_TO_EN_TRANSLATION = {
    "Commentary on the Structure of the Sutra": {
        "data": [],
        "Demonstrating the Unbroken Lineage of the Buddha": {"data": []},
        "Demonstrating the Characteristics of Diligent Application": {"data": []},
        "Demonstrating the Basis of the Characteristics of Intense Application": {
            "data": []
        },
    }
}

MOCK_EN_TO_BO_TRANSLATION = {
    "མདོའི་གཞུང་གི་འགྲེལ་བཤད།": {
        "data": [],
        "སངས་རྒྱས་ཀྱི་མཐར་ཐུག་གི་ཡེ་ཤེས་རྒྱུན་མི་ཆད་པའི་བསྟན་པ།": {"data": []},
    }
}

MOCK_ZH_TO_BO_TRANSLATION = {
    "སྔོན་གླེང་།": {"data": []},
    "བཞི། མདོ་འདིའི་སྒྲིག་གཞི།": {
        "data": [],
        "ལྔ་པ། མདོ་འདིའི་ལོ་ཙཱ་བ།": {
            "data": [],
            "ལྔ་པ། མདོ་འདིའི་ལོ་ཙཱ་བ།": {"data": []},
        },
    },
    "དྲུག་པ། མདོ་འདིའི་འགྲེལ་བཤད་བྱེད་མཁན།": {"data": []},
}


class TestCommentarySerializer(TestCase):
    def setUp(self):
        # Create the patcher and set return_value
        self.patcher = mock.patch(
            "openpecha.pecha.serializers.pecha_db.commentary.complex_commentary.ComplexCommentarySerializer.get_category",
            return_value={
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
            },
        )
        # Start the patch
        self.mock_get_category = self.patcher.start()

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.complex_commentary.get_en_content_translation",
        return_value=MOCK_BO_TO_EN_TRANSLATION,
    )
    def test_bo_commentary_serializer(self, mock_get_en_translation):
        pecha = Pecha.from_path(DATA_DIR / "bo/I0EB9B939")

        serializer = ComplexCommentarySerializer()
        serialized_json = serializer.serialize(pecha, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "bo/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.complex_commentary.get_bo_content_translation",
        return_value=MOCK_EN_TO_BO_TRANSLATION,
    )
    def test_en_commentary_serializer(self, mock_get_bo_translation):
        pecha = Pecha.from_path(DATA_DIR / "en/I088F7504")

        serializer = ComplexCommentarySerializer()
        serialized_json = serializer.serialize(pecha, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "en/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    @mock.patch(
        "openpecha.pecha.serializers.pecha_db.commentary.complex_commentary.get_bo_content_translation",
        return_value=MOCK_ZH_TO_BO_TRANSLATION,
    )
    def test_zh_commentary_serializer(self, mock_get_bo_translation):
        pecha = Pecha.from_path(DATA_DIR / "zh/I8BCEC781")

        serializer = ComplexCommentarySerializer()
        serialized_json = serializer.serialize(pecha, "Vajra Cutter")

        expected_serialized_json = read_json(DATA_DIR / "zh/commentary_serialized.json")
        assert serialized_json == expected_serialized_json

    def tearDown(self):
        # Stop the patch
        self.patcher.stop()
