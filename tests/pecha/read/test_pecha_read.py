from pathlib import Path

from stam import AnnotationStore

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum


def test_pecha_read():
    DATA = Path(__file__).parent / "data"
    pecha_path = DATA / "I0F8FC40B"
    pecha = Pecha.from_path(pecha_path)
    assert pecha.id_ == "I0F8FC40B"

    base_path = pecha.base_path / "base"
    basefile_name = list(base_path.rglob("*.txt"))[0].stem
    ann_store = pecha.get_annotation_store(basefile_name, LayerEnum.root_segment)
    assert isinstance(ann_store, AnnotationStore)

    expected_anns = [
        "\ufeffརྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།\n",
        "བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ།\n",
        "སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །\n",
        "བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །\n",  # noqa
        "སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ། །དེ་ཕྱིར་གཞན་དོན་བསམ་པ་བདག་ལ་མེད། །རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས། །",  # noqa
    ]

    """ comparing annotations """
    dataset = list(ann_store.datasets())[0]
    key = dataset.key(LayerGroupEnum.structure_type.value)
    anns = list(dataset.data(key, value=LayerEnum.root_segment.value).annotations())
    for ann, expected_ann in zip(anns, expected_anns):
        assert str(ann) == expected_ann


test_pecha_read()
