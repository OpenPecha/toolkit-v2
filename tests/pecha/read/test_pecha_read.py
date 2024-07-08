from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.layer import Layer, LayerEnum


def test_pecha_read():
    DATA = Path(__file__).parent / "data"
    pecha = Pecha.from_path(DATA / "IE7D6875F" / "IE7D6875F.opf")
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


test_pecha_read()
