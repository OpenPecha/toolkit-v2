from pathlib import Path

from stam import AnnotationStore

from openpecha.pecha.layer import LayerEnum, get_layer_group
from openpecha.pecha.parsers.plaintext.plaintext_parser import PlainTextParser


def test_ann_on_ann_parse():
    data_folder = Path(__file__).parent / "data"
    pecha_id = "ID00AC0A6"
    basefile_name = "7906"
    ann_store_file_name = "Chapter-7ba.json"
    ann_store_path = (
        data_folder / pecha_id / "layers" / basefile_name / ann_store_file_name
    )

    parser = PlainTextParser(
        ann_store_path, PlainTextParser.two_new_line_segmenter, "Tsawa"
    )

    ann_store_path = parser.parse_ann_on_ann()

    ann_store = AnnotationStore(file=str(ann_store_path))

    ann_dataset = next(ann_store.datasets())
    ann_value = "Tsawa"
    ann_key_value = get_layer_group(LayerEnum("Tsawa")).value
    ann_key = ann_dataset.key(ann_key_value)
    anns = list(ann_key.data(value=ann_value).annotations())

    ann_data = []
    for ann in anns:
        curr_data = {}
        curr_data["content"] = str(ann)
        for data in ann:
            curr_data[data.key().id()] = str(data.value())
        ann_data.append(curr_data)

    assert ann_data == [
        {
            "content": "བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །",
            "Structure_Type": "Tsawa",
        },
        {
            "content": "སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ། །དེ་ཕྱིར་གཞན་དོན་བསམ་པ་བདག་ལ་མེད། །རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས།",
            "Structure_Type": "Tsawa",
        },
        {
            "content": "དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས། །འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ། །བདག་དང་སྐལ་བ་མཉམ་པ་གཞན་གྱིས་ཀྱང་། །ཅི་སྟེ་འདི་དག་མཐོང་ན་དོན་ཡོད་འགྱུར། །",
            "Structure_Type": "Tsawa",
        },
        {
            "content": "དལ་འབྱོར་འདི་ནི་རྙེད་པར་ཤིན་ཏུ་དཀའ། །སྐྱེས་བུའི་དོན་སྒྲུབ་ཐོབ་པར་གྱུར་པ་ལ། །གལ་ཏེ་འདི་ལ་ཕན་པ་མ་བསྒྲུབས་ན། །ཕྱིས་འདི་ཡང་དག་འབྱོར་པར་ག་ལ་འགྱུར། །",
            "Structure_Type": "Tsawa",
        },
        {
            "content": "ཇི་ལྟར་མཚན་མོ་མུན་ནག་སྤྲིན་རུམ་ན། །གློག་འགྱུ་སྐད་ཅིག་བར་སྣང་སྟོན་པ་ལྟར། །དེ་བཞིན་སངས་རྒྱས་མཐུ་ཡིས་བརྒྱ་ལམ་ན། །འཇིག་རྟེན་བསོད་ནམས་བློ་གྲོས་ཐང་འགའ་འབྱུང་།",
            "Structure_Type": "Tsawa",
        },
    ]

    """ clean up"""
    ann_store_path.unlink()


test_ann_on_ann_parse()
