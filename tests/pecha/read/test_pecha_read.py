from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.layer import Layer, LayerEnum


def test_pecha_read():
    DATA = Path(__file__).parent / "data"
    pecha = Pecha.from_path(DATA / "IE7D6875F")
    assert pecha.pecha_id == "IE7D6875F"
    assert "f2b056668a0c4ad3a085bdcd8e2d7adb" in pecha.bases
    assert (
        pecha.bases["f2b056668a0c4ad3a085bdcd8e2d7adb"]
        == "རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པའི་ལེགས་པར་སྦྱར་བ།"
    )

    for layer_key, layer in pecha.layers["f2b056668a0c4ad3a085bdcd8e2d7adb"].items():
        annotation_type, layer_id = layer_key
        assert annotation_type == LayerEnum.segment
        assert isinstance(layer_id, str)
        assert isinstance(layer, Layer)

    first_layer = pecha.layers["f2b056668a0c4ad3a085bdcd8e2d7adb"][
        (LayerEnum.segment, "bf13")
    ]

    annotations = list(first_layer.get_annotations())
    assert annotations == [
        {
            "id": "f2b056668a0c4ad3a085bdcd8e2d7adb",
            "segment": "རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།",
            "start": 0,
            "end": 39,
            "annotation_category": "Structure Type",
            "annotation_type": "Segment",
        },
        {
            "id": "b696df2dbe314e8a87881a2bc391d0d5",
            "segment": "བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པའི་ལེགས་པར་སྦྱར་བ།",
            "start": 39,
            "end": 103,
            "annotation_category": "Structure Type",
            "annotation_type": "Segment",
        },
    ]


test_pecha_read()
