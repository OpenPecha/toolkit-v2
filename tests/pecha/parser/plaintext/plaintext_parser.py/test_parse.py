from pathlib import Path

from openpecha.pecha.parsers.plaintext.plaintext_parser import PlainTextParser


def test_parse():
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
        input,
        lambda x: PlainTextParser.regex_segmenter(x, pattern, group_mapping),
        "Chapter",
    )

    output_path = Path(__file__).parent / "output"
    parser.parse(output_path)


test_parse()
