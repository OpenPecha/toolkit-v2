from pathlib import Path

from openpecha.pecha.serializers.commentary import CommentarySerializer


def test_commentary_serializer():
    DATA_DIR = Path(__file__).parent / "data"
    pecha_path = DATA_DIR / "IC3797777"

    serializer = CommentarySerializer()
    formatted_sapche_anns = serializer.serialize(pecha_path, "རྡོ་རྗེ་གཅོད་པ།")
    expected_formatted_sapche_anns = {
        "མདོའི་ལུས་ཀྱི་འགྲེལ་པ།": {
            "data": [],
            "སངས་རྒྱས་ཀྱི་གདུང་རྒྱུན་མི་འཆད་པ་བསྟན་པ།": {
                "data": [
                    "<1><1>རྒྱ་གར་སྐད་དུ། །ཨཱརྱ་བྷ་ག་བ་ཏཱི་པྲཛྙཱ་པཱ་ར་མི་ཏཱ་བཛྲ་ཙྪེ་དི་ཀཱ་ཡཱཿསཔྟ་དཱརྠ་ཊཱི་ཀཱ།"
                ]
            },
        },
        "ཚིག་གི་དོན་བཤད་པ།": {
            "data": [],
            "སངས་རྒྱས་ཀྱི་གདུང་རྒྱུན་མི་འཆད་པ་བསྟན་པ།": {
                "data": [
                    "ཚིག་གི་དོན་བཤད་པ།\nསངས་རྒྱས་ཀྱི་གདུང་རྒྱུན་མི་འཆད་པ་བསྟན་པ།",
                    "མཚུངས་མེད་སངས་རྒྱས་ཆོས་རྣམས་སྐྱེད་མཛད་ལ། །\nགང་ཞིག་ཆོས་དབྱིངས་གསོ་བའི་མ་མ་སྟེ། །\nདབྱེ་དཀའི་རྡོ་རྗེ་གཞན་དོན་གྲུབ་གང་ཡིན། །\nགང་ཞིག་བཟུང་བས་འཕགས་ཀུན་སྐྱེད་པའམ་ཡིན། །",
                ]
            },
        },
    }
    assert formatted_sapche_anns == expected_formatted_sapche_anns


test_commentary_serializer()
