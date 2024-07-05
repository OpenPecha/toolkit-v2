from pathlib import Path
from shutil import rmtree

from openpecha.pecha import Pecha
from openpecha.pecha.annotation import Annotation
from openpecha.pecha.layer import Layer, LayerEnum


def get_data_dir():
    output_path = Path(__file__).parent / "output"
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


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
            (LayerEnum.segment, "bf13"): Layer(
                id_="bf13",
                annotation_type=LayerEnum("Segment"),
                annotations=get_annotations(),
            )
        }
    }


def get_annotations():
    return {
        "f2b056668a0c4ad3a085bdcd8e2d7adb": Annotation(
            start=0,
            end=39,
            metadata={},
        ),
        "b696df2dbe314e8a87881a2bc391d0d5": Annotation(
            start=39,
            end=103,
            metadata={},
        ),
    }


def test_pecha_write():
    pecha_id = "IE7D6875F"
    base = get_base()
    layer = get_layer()
    output_path = get_data_dir()
    expected_output_path = Path(__file__).parent / "expected_output"

    pecha = Pecha(pecha_id=pecha_id, bases=base, layers=layer, metadata=get_metadata())
    pecha.write(output_path=output_path)

    output_file_names = [file.name for file in list(output_path.rglob("*"))]
    expected_file_names = [file.name for file in list(expected_output_path.rglob("*"))]

    """ sort the list """
    output_file_names.sort()
    expected_file_names.sort()

    assert output_file_names == expected_file_names

    """ clean up """
    rmtree(output_path)


test_pecha_write()
