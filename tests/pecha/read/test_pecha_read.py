from pathlib import Path

from stam import AnnotationStore, TextResource

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum
from openpecha.pecha.metadata import MetaData


def test_pecha_read():
    DATA = Path(__file__).parent / "data"
    pecha_path = DATA / "I4F3221FF"
    pecha = Pecha.from_path(pecha_path)
    assert pecha.id_ == "I4F3221FF"

    ann_store = pecha.get_annotation_store(LayerEnum.root_segment)
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

    """ getting metadata """
    key = dataset.key(LayerGroupEnum.resource_type.value)
    metadata_ann = list(
        dataset.data(key, value=LayerEnum.metadata.value).annotations()
    )[0]
    text_resource = metadata_ann.target().resource(ann_store)
    assert isinstance(text_resource, TextResource)
    metadata_obj = MetaData.from_text(text_resource.text())
    assert isinstance(metadata_obj, MetaData)


test_pecha_read()
