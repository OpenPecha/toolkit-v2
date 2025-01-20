import tempfile
from pathlib import Path
from unittest import TestCase, mock

from openpecha.alignment.serializers.translation import TextTranslationSerializer
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"


class TestTextTranslationSerializer(TestCase):
    def setUp(self):
        # Create the patcher and set return_value
        self.patcher = mock.patch(
            "openpecha.alignment.serializers.translation.CategoryExtractor.get_category",
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

    def test_translation_serializer(self):
        root_opf = DATA_DIR / "bo/IFA46BBC2"
        translation_opf = DATA_DIR / "en/I6EA29D09"
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_dir = Path(tmpdirname)

            serializer = TextTranslationSerializer()
            json_output = serializer.serialize(root_opf, translation_opf, output_dir)

            expected_json_path = DATA_DIR / "expected_output.json"
            assert read_json(json_output) == read_json(expected_json_path)

    def tearDown(self):
        # Stop the patch
        self.patcher.stop()


serializer = TestTextTranslationSerializer()
serializer.setUp()
serializer.test_translation_serializer()
serializer.tearDown()