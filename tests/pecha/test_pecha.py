from openpecha.pecha import Pecha
from openpecha.pecha.annotation import Annotation


def get_segments():
    return {
        "f2b056668a0c4ad3a085bdcd8e2d7adb": "རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།",
        "b696df2dbe314e8a87881a2bc391d0d5": "བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པའི་ལེགས་པར་སྦྱར་བ།",
    }


def get_metadata():
    return {
        "annotation_category": "Structure Type",
        "annotation_label": "Segment",
    }


def get_expected_annotations():
    expected_annotations = [
        Annotation(
            id_="f2b056668a0c4ad3a085bdcd8e2d7adb",
            segment="རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།",
            start=0,
            end=39,
            metadata={},
        ),
        Annotation(
            id_="b696df2dbe314e8a87881a2bc391d0d5",
            segment="བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པའི་ལེགས་པར་སྦྱར་བ།",
            start=39,
            end=103,
            metadata={},
        ),
    ]
    return expected_annotations


def test_pecha_set_annotations():
    pecha_id = "IE7D6875F"
    segments = get_segments()
    metadata = get_metadata()
    pecha = Pecha(pecha_id=pecha_id, segments=segments, metadata=metadata)
    assert isinstance(
        pecha, Pecha
    ), "Not able to create Pecha object with id, segments and metadata"

    annotations = list(pecha.set_annotations())
    assert (
        annotations == get_expected_annotations()
    ), "Pecha not able to set annotations for the segments"
