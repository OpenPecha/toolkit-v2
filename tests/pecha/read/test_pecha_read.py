from pathlib import Path

from stam import AnnotationStore

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum


def test_pecha_read():
    DATA = Path(__file__).parent / "data"
    pecha_path = DATA / "I91F9CE06"
    pecha = Pecha.from_path(pecha_path)
    assert pecha.id_ == "I91F9CE06"

    ann_store = pecha.get_annotation_store(LayerEnum.root_segment)
    assert isinstance(ann_store, AnnotationStore)

    expected_anns = [
        "\ufeffརྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།\n",
        "བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ།\n",
        "སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །\n",
        "བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །\n",  # noqa
        "སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ། །དེ་ཕྱིར་གཞན་དོན་བསམ་པ་བདག་ལ་མེད། །རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས། །",  # noqa
    ]
    for ann, expected_ann in zip(ann_store.annotations(), expected_anns):
        assert str(ann) == expected_ann


test_pecha_read()
