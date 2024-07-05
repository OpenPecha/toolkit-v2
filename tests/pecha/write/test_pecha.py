from pathlib import Path
from shutil import rmtree

from openpecha.pecha import Pecha
from openpecha.pecha.annotation import Annotation
from openpecha.pecha.layer import Layer, LayerEnum


def get_data_dir():
    export_path = Path(__file__).parent / "output"
    export_path.mkdir(parents=True, exist_ok=True)
    return export_path


def get_metadata():
    return {
        "annotation_type": "Segment",
    }


def get_base():
    return {
        "f2b056668a0c4ad3a085bdcd8e2d7adb": "རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པའི་ལེགས་པར་སྦྱར་བ།"  # noqa
    }


def get_layer():
    return {
        "f2b056668a0c4ad3a085bdcd8e2d7adb": {
            LayerEnum("Segment"): Layer(LayerEnum("Segment"), get_annotations())
        }
    }


def get_annotations():
    return {
        "f2b056668a0c4ad3a085bdcd8e2d7adb": Annotation(
            segment="རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།",
            start=0,
            end=39,
            metadata={},
        ),
        "b696df2dbe314e8a87881a2bc391d0d5": Annotation(
            segment="བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པའི་ལེགས་པར་སྦྱར་བ།",
            start=39,
            end=103,
            metadata={},
        ),
    }


def test_pecha_write():
    pecha_id = "IE7D6875F"
    base = get_base()
    layer = get_layer()
    export_path = get_data_dir()
    expected_output_path = Path(__file__).parent / "expected_output"

    pecha = Pecha(pecha_id=pecha_id, bases=base, layers=layer, metadata=get_metadata())
    pecha.write(export_path=export_path)

    output_file_names = [file.name for file in export_path.rglob("*")].sort()
    expected_file_names = [file.name for file in expected_output_path.rglob("*")].sort()

    assert output_file_names == expected_file_names

    """ clean up """
    rmtree(export_path)
