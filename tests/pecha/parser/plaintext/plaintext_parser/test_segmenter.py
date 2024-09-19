from openpecha.pecha.parsers.plaintext.plaintext_parser import (
    PlainTextParser,
    count_whitespace_details,
)


def test_count_whitespace_details():
    text = " Hello world!\n\n"
    result = count_whitespace_details(text)
    assert result == {"start_whitespace": 1, "end_whitespace": 2}

    text = "Hello world!\n\n"
    result = count_whitespace_details(text)
    assert result == {"start_whitespace": 0, "end_whitespace": 2}

    text = " Hello world!"
    result = count_whitespace_details(text)
    assert result == {"start_whitespace": 1, "end_whitespace": 0}

    text = "Hello world!"
    result = count_whitespace_details(text)
    assert result == {"start_whitespace": 0, "end_whitespace": 0}


def test_space_segmenter():
    input = "བཀྲ་ཤིས་བདེ་ལེགས། །བདེ་ལེགས་བཀྲ་ཤིས། །"
    parser = PlainTextParser(input, PlainTextParser.space_segmenter, "")
    assert parser.segmenter(input) == [
        {"annotation_text": "བཀྲ་ཤིས་བདེ་ལེགས།", "start": 0, "end": 17},
        {"annotation_text": "།བདེ་ལེགས་བཀྲ་ཤིས།", "start": 18, "end": 36},
        {"annotation_text": "།", "start": 37, "end": 38},
    ]


def test_new_line_segmenter():
    input = "བཀྲ་ཤིས་བདེ་ལེགས།\n།བདེ་ལེགས་བཀྲ་ཤིས།\n།"
    parser = PlainTextParser(input, PlainTextParser.new_line_segmenter, "")
    assert parser.segmenter(input) == [
        {"annotation_text": "བཀྲ་ཤིས་བདེ་ལེགས།", "start": 0, "end": 17},
        {"annotation_text": "།བདེ་ལེགས་བཀྲ་ཤིས།", "start": 18, "end": 36},
        {"annotation_text": "།", "start": 37, "end": 38},
    ]


def test_regex_segmenter():
    input = """
    རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།

    ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།" བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་།

    སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ།

    ch2-"སྡིག་པ་བཤགས་པ།" དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས། །འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ།

    དལ་འབྱོར་འདི་ནི་རྙེད་པར་ཤིན་ཏུ་དཀའ། །སྐྱེས་བུའི་དོན་སྒྲུབ་ཐོབ་པར་གྱུར་པ་ལ། །གལ་ཏེ་འདི་ལ་ཕན་པ་མ་བསྒྲུབས་ན།

    ཇི་ལྟར་མཚན་མོ་མུན་ནག་སྤྲིན་རུམ་ན། །གློག་འགྱུ་སྐད་ཅིག་བར་སྣང་སྟོན་པ་ལྟར། །དེ་བཞིན་སངས་རྒྱས་མཐུ་ཡིས་བརྒྱ་ལམ་ན།
    """
    pattern = r"ch(\d+)-\"([\u0F00-\u0FFF]+)\"\s*([\u0F00-\u0FFF\s\n]+)"
    group_mapping = ["chapter_number", "chapter_name", "annotation_text"]
    parser = PlainTextParser(
        input, lambda x: PlainTextParser.regex_segmenter(x, pattern, group_mapping), ""
    )
    assert parser.segmenter(input) == [
        {
            "chapter_number": "1",
            "chapter_name": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
            "annotation_text": "བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་།\n\n    སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ།\n\n    ",
            "start": 87,
            "end": 210,
        },
        {
            "chapter_number": "2",
            "chapter_name": "སྡིག་པ་བཤགས་པ།",
            "annotation_text": "དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས། །འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ།\n\n    དལ་འབྱོར་འདི་ནི་རྙེད་པར་ཤིན་ཏུ་དཀའ། །སྐྱེས་བུའི་དོན་སྒྲུབ་ཐོབ་པར་གྱུར་པ་ལ། །གལ་ཏེ་འདི་ལ་ཕན་པ་མ་བསྒྲུབས་ན།\n\n    ཇི་ལྟར་མཚན་མོ་མུན་ནག་སྤྲིན་རུམ་ན། །གློག་འགྱུ་སྐད་ཅིག་བར་སྣང་སྟོན་པ་ལྟར། །དེ་བཞིན་སངས་རྒྱས་མཐུ་ཡིས་བརྒྱ་ལམ་ན།\n    ",
            "start": 231,
            "end": 534,
        },
    ]
