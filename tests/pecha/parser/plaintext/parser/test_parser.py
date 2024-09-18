from pathlib import Path

from openpecha.pecha.parsers.plaintext.parser import PechaFrameWork

expected_chapter_output = {
    "raw_string": [
        "\ufeffརྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར། ",
        "",
        "བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། ",
        "",
        "སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །",
        "",
        'ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།" བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །',
        "",
        "སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ། །དེ་ཕྱིར་གཞན་དོན་བསམ་པ་བདག་ལ་མེད། །རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས། །",
        "",
        'ch2-"སྡིག་པ་བཤགས་པ།" དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས། །འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ། །བདག་དང་སྐལ་བ་མཉམ་པ་གཞན་གྱིས་ཀྱང་། །ཅི་སྟེ་འདི་དག་མཐོང་ན་དོན་ཡོད་འགྱུར། །',
        "",
        "དལ་འབྱོར་འདི་ནི་རྙེད་པར་ཤིན་ཏུ་དཀའ། །སྐྱེས་བུའི་དོན་སྒྲུབ་ཐོབ་པར་གྱུར་པ་ལ། །གལ་ཏེ་འདི་ལ་ཕན་པ་མ་བསྒྲུབས་ན། །ཕྱིས་འདི་ཡང་དག་འབྱོར་པར་ག་ལ་འགྱུར། །",
        "",
        "ཇི་ལྟར་མཚན་མོ་མུན་ནག་སྤྲིན་རུམ་ན། །གློག་འགྱུ་སྐད་ཅིག་བར་སྣང་སྟོན་པ་ལྟར། །དེ་བཞིན་སངས་རྒྱས་མཐུ་ཡིས་བརྒྱ་ལམ་ན། །འཇིག་རྟེན་བསོད་ནམས་བློ་གྲོས་ཐང་འགའ་འབྱུང་། །",
        "",
    ],
    "chapter": [
        {
            "chapter_number": "1",
            "chapter_name": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
            "start_index": 6,
        },
        {"chapter_number": "2", "chapter_name": "སྡིག་པ་བཤགས་པ།", "start_index": 10},
    ],
}


def test_chapter_parser_pipeline():
    DATA = Path(__file__).parent / "data"
    input_file = DATA / "basefile.txt"
    input_text = input_file.read_text(encoding="utf-8")

    openpecha_framework = PechaFrameWork(input_text)
    pipeline_definition = ["chapter_parser_pipe"]
    openpecha_framework.parser_pipeline(pipeline_definition)
    assert openpecha_framework.data == expected_chapter_output


test_chapter_parser_pipeline()
