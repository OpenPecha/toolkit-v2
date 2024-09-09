from pathlib import Path
from shutil import rmtree

from stam import AnnotationStore

from openpecha.pecha.parsers.plaintext.plaintext_parser import PlainTextParser


def test_parse():
    input_file_path = Path(__file__).parent / "data" / "basefile.txt"
    input = input_file_path.read_text(encoding="utf-8")

    pattern = r"ch(\d+)-\"([\u0F00-\u0FFF]+)\"\s*([\u0F00-\u0FFF\s\n]+)"
    group_mapping = ["chapter_number", "chapter_name", "annotation_text"]
    parser = PlainTextParser(
        input,
        lambda x: PlainTextParser.regex_segmenter(x, pattern, group_mapping),
        "Chapter",
    )

    output_path = Path(__file__).parent / "output"
    ann_store_path = parser.parse(output_path)
    ann_store = AnnotationStore(file=str(ann_store_path))

    anns = list(ann_store.annotations())
    assert len(anns) == 2
    ann_data = []
    for ann in anns:
        curr_data = {}
        curr_data["annotation_text"] = str(ann)
        for data in ann:
            curr_data[data.key().id()] = str(data.value())
        ann_data.append(curr_data)

    assert ann_data == [
        {
            "annotation_text": "བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །\n\nསྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ། །དེ་ཕྱིར་གཞན་དོན་བསམ་པ་བདག་ལ་མེད། །རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས། །\n\n",
            "chapter_number": "1",
            "chapter_name": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
            "Structure_Type": "Chapter",
        },
        {
            "annotation_text": "དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས། །འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ། །བདག་དང་སྐལ་བ་མཉམ་པ་གཞན་གྱིས་ཀྱང་། །ཅི་སྟེ་འདི་དག་མཐོང་ན་དོན་ཡོད་འགྱུར། །\n\nདལ་འབྱོར་འདི་ནི་རྙེད་པར་ཤིན་ཏུ་དཀའ། །སྐྱེས་བུའི་དོན་སྒྲུབ་ཐོབ་པར་གྱུར་པ་ལ། །གལ་ཏེ་འདི་ལ་ཕན་པ་མ་བསྒྲུབས་ན། །ཕྱིས་འདི་ཡང་དག་འབྱོར་པར་ག་ལ་འགྱུར། །\n\nཇི་ལྟར་མཚན་མོ་མུན་ནག་སྤྲིན་རུམ་ན། །གློག་འགྱུ་སྐད་ཅིག་བར་སྣང་སྟོན་པ་ལྟར། །དེ་བཞིན་སངས་རྒྱས་མཐུ་ཡིས་བརྒྱ་ལམ་ན། །འཇིག་རྟེན་བསོད་ནམས་བློ་གྲོས་ཐང་འགའ་འབྱུང་། །\n\n\n\n",
            "chapter_number": "2",
            "chapter_name": "སྡིག་པ་བཤགས་པ།",
            "Structure_Type": "Chapter",
        },
    ]

    """ clean up """
    rmtree(output_path)


test_parse()
