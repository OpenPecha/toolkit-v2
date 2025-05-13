# from pathlib import Path
# from unittest import TestCase, mock
# from typing import Any, List
# from openpecha.pecha import Pecha
# from openpecha.pecha.serializers.pecha_db.commentary.complex_commentary import (
#     ComplexCommentarySerializer,
# )
# from openpecha.utils import read_json
# from tests.pecha import SharedPechaSetup, DummyPechaCategoryModel

# DATA_DIR = Path(__file__).parent / "data"

# null = None

# MOCK_BO_TO_EN_TRANSLATION = {
#     "Commentary on the Structure of the Sutra": {
#         "data": [],
#         "Demonstrating the Unbroken Lineage of the Buddha": {"data": []},
#         "Demonstrating the Characteristics of Diligent Application": {"data": []},
#         "Demonstrating the Basis of the Characteristics of Intense Application": {
#             "data": []
#         },
#     }
# }

# MOCK_EN_TO_BO_TRANSLATION = {
#     "མདོའི་གཞུང་གི་འགྲེལ་བཤད།": {
#         "data": [],
#         "སངས་རྒྱས་ཀྱི་མཐར་ཐུག་གི་ཡེ་ཤེས་རྒྱུན་མི་ཆད་པའི་བསྟན་པ།": {"data": []},
#     }
# }

# MOCK_ZH_TO_BO_TRANSLATION = {
#     "སྔོན་གླེང་།": {"data": []},
#     "བཞི། མདོ་འདིའི་སྒྲིག་གཞི།": {
#         "data": [],
#         "ལྔ་པ། མདོ་འདིའི་ལོ་ཙཱ་བ།": {
#             "data": [],
#             "ལྔ་པ། མདོ་འདིའི་ལོ་ཙཱ་བ།": {"data": []},
#         },
#     },
#     "དྲུག་པ། མདོ་འདིའི་འགྲེལ་བཤད་བྱེད་མཁན།": {"data": []},
# }


# class TestCommentarySerializer(TestCase, SharedPechaSetup):
#     def setUp(self):
#         self.pecha_category: List[Any] = [
#             DummyPechaCategoryModel(
#                 description={"en": "", "bo": ""},
#                 short_description={"en": "", "bo": ""},
#                 name={"en": "Madhyamaka", "bo": "དབུ་མ།"},
#                 parent=null,
#             ),
#             DummyPechaCategoryModel(
#                 description={"en": "", "bo": ""},
#                 short_description={"en": "", "bo": ""},
#                 name={"en": "Entering the Middle Way", "bo": "དབུ་མ་ལ་འཇུག་པ།"},
#                 parent="madhyamaka",
#             ),
#         ]

#     @mock.patch(
#         "openpecha.pecha.serializers.pecha_db.commentary.complex_commentary.get_en_content_translation",
#         return_value=MOCK_BO_TO_EN_TRANSLATION,
#     )
#     def test_bo_commentary_serializer(self, mock_get_en_translation):
#         pecha = Pecha.from_path(DATA_DIR / "bo/I0EB9B939")

#         serializer = ComplexCommentarySerializer()
#         serialized_json = serializer.serialize(
#             pecha, self.pecha_category, "Vajra Cutter"
#         )

#         expected_serialized_json = read_json(DATA_DIR / "bo/commentary_serialized.json")
#         assert serialized_json == expected_serialized_json

#     @mock.patch(
#         "openpecha.pecha.serializers.pecha_db.commentary.complex_commentary.get_bo_content_translation",
#         return_value=MOCK_EN_TO_BO_TRANSLATION,
#     )
#     def test_en_commentary_serializer(self, mock_get_bo_translation):
#         pecha = Pecha.from_path(DATA_DIR / "en/I088F7504")

#         serializer = ComplexCommentarySerializer()
#         serialized_json = serializer.serialize(
#             pecha, self.pecha_category, "Vajra Cutter"
#         )

#         expected_serialized_json = read_json(DATA_DIR / "en/commentary_serialized.json")
#         assert serialized_json == expected_serialized_json

#     @mock.patch(
#         "openpecha.pecha.serializers.pecha_db.commentary.complex_commentary.get_bo_content_translation",
#         return_value=MOCK_ZH_TO_BO_TRANSLATION,
#     )
#     def test_zh_commentary_serializer(self, mock_get_bo_translation):
#         pecha = Pecha.from_path(DATA_DIR / "zh/I8BCEC781")

#         serializer = ComplexCommentarySerializer()
#         serialized_json = serializer.serialize(
#             pecha, self.pecha_category, "Vajra Cutter"
#         )

#         expected_serialized_json = read_json(DATA_DIR / "zh/commentary_serialized.json")
#         assert serialized_json == expected_serialized_json

#     def tearDown(self):
#         pass
