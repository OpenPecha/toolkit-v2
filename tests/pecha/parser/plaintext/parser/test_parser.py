from pathlib import Path

from openpecha.pecha.parsers.plaintext.parser import PechaFrameWork

expected_raw_string = {
    "raw_string": [
        "\ufeffརྒྱ་གར་སྐད་དུ།",
        " ",
        "བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།",
        "\n",
        "\n",
        "བོད་སྐད་དུ།",
        " ",
        "བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ།",
        "\n",
        "\n",
        "སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ།",
        " ",
        "།",
        "\n",
        "\n",
        'ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།"',
        " ",
        "བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་།",
        " ",
        "།ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ།",
        " ",
        "།བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི།",
        " ",
        "།ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ།",
        " ",
        "།",
        "\n",
        "\n",
        "སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད།",
        " ",
        "།སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ།",
        " ",
        "།དེ་ཕྱིར་གཞན་དོན་བསམ་པ་བདག་ལ་མེད།",
        " ",
        "།རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས།",
        " ",
        "།",
        "\n",
        "\n",
        'ch2-"སྡིག་པ་བཤགས་པ།"',
        " ",
        "དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས།",
        " ",
        "།འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ།",
        " ",
        "།བདག་དང་སྐལ་བ་མཉམ་པ་གཞན་གྱིས་ཀྱང་།",
        " ",
        "།ཅི་སྟེ་འདི་དག་མཐོང་ན་དོན་ཡོད་འགྱུར།",
        " ",
        "།",
        "\n",
        "\n",
        "དལ་འབྱོར་འདི་ནི་རྙེད་པར་ཤིན་ཏུ་དཀའ།",
        " ",
        "།སྐྱེས་བུའི་དོན་སྒྲུབ་ཐོབ་པར་གྱུར་པ་ལ།",
        " ",
        "།གལ་ཏེ་འདི་ལ་ཕན་པ་མ་བསྒྲུབས་ན།",
        " ",
        "།ཕྱིས་འདི་ཡང་དག་འབྱོར་པར་ག་ལ་འགྱུར།",
        " ",
        "།",
        "\n",
        "\n",
        "ཇི་ལྟར་མཚན་མོ་མུན་ནག་སྤྲིན་རུམ་ན།",
        " ",
        "།གློག་འགྱུ་སྐད་ཅིག་བར་སྣང་སྟོན་པ་ལྟར།",
        " ",
        "།དེ་བཞིན་སངས་རྒྱས་མཐུ་ཡིས་བརྒྱ་ལམ་ན།",
        " ",
        "།འཇིག་རྟེན་བསོད་ནམས་བློ་གྲོས་ཐང་འགའ་འབྱུང་།",
        " ",
        "།",
    ],
}

expected_chapter_output = [
    {
        "number": "1",
        "name": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
        "index_start": 17,
        "index_end": 38,
    },
    {"number": "2", "name": "སྡིག་པ་བཤགས་པ།", "index_start": 41, "index_end": 71},
]


expected_tsawa_output = [
    {"index_start": 0, "index_end": 2},
    {"index_start": 5, "index_end": 7},
    {"index_start": 10, "index_end": 12},
    {"index_start": 16, "index_end": 25},
    {"index_start": 28, "index_end": 36},
    {"index_start": 40, "index_end": 49},
    {"index_start": 52, "index_end": 60},
    {"index_start": 63, "index_end": 71},
]


def test_chapter_parser_pipeline():
    DATA = Path(__file__).parent / "data"
    input_file = DATA / "basefile.txt"
    input_text = input_file.read_text(encoding="utf-8")

    openpecha_framework = PechaFrameWork(input_text)
    assert "raw_string" in openpecha_framework.data
    assert openpecha_framework.data == expected_raw_string

    pipeline_definition = ["chapter_parser_pipe"]
    openpecha_framework.parser_pipeline(pipeline_definition)
    assert "Chapter" in openpecha_framework.data
    assert openpecha_framework.data["Chapter"] == expected_chapter_output


def test_tsawa_parser_pipe():
    DATA = Path(__file__).parent / "data"
    input_file = DATA / "basefile.txt"
    input_text = input_file.read_text(encoding="utf-8")

    openpecha_framework = PechaFrameWork(input_text)
    pipeline_definition = ["tsawa_parser_pipe"]
    openpecha_framework.parser_pipeline(pipeline_definition)
    assert "Tsawa" in openpecha_framework.data
    assert openpecha_framework.data["Tsawa"] == expected_tsawa_output


test_chapter_parser_pipeline()
