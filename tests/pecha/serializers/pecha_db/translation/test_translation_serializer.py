from pathlib import Path
from unittest import TestCase, mock

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.translation import TextTranslationSerializer
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"


class TestTextTranslationSerializer(TestCase):
    def setUp(self):
        # Create the patcher and set return_value
        self.patcher = mock.patch(
            "openpecha.pecha.serializers.translation.CategoryExtractor.get_category",
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

    def test_root_serializer(self):
        root_opf = DATA_DIR / "bo/IE60BBDE8"
        root_pecha = Pecha.from_path(root_opf)

        serializer = TextTranslationSerializer()
        json_output = serializer.serialize(pecha=root_pecha, alignment_data=None)

        expected_json_path = DATA_DIR / "expected_root_output.json"
        assert json_output == read_json(expected_json_path)

    def test_translation_serializer(self):
        root_opf = DATA_DIR / "bo/IE60BBDE8"
        translation_opf = DATA_DIR / "en/I62E00D78"

        translation_alignment = {
            "root": "IE60BBDE8/layers/3635/Tibetan_Segment-039B.json",
            "translation": "I62E00D78/layers/D93E/English_Segment-0216.json",
        }

        root_pecha = Pecha.from_path(root_opf)
        translation_pecha = Pecha.from_path(translation_opf)
        with mock.patch(
            "openpecha.pecha.serializers.translation.get_pecha_with_id"
        ) as mock_get_pecha_with_id:
            mock_get_pecha_with_id.return_value = root_pecha

            serializer = TextTranslationSerializer()
            json_output = serializer.serialize(
                pecha=translation_pecha, alignment_data=translation_alignment
            )

            expected_json_path = DATA_DIR / "expected_translation_output.json"
            assert json_output == read_json(expected_json_path)

    def tearDown(self):
        # Stop the patch
        self.patcher.stop()
