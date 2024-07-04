from pathlib import Path

from openpecha.alignment.parsers.plaintext import PlainTextLineAlignedParser
from openpecha.pecha import Pecha


def get_data_dir():
    return Path(__file__).parent / "data"


def get_metadata():
    return {
        "source": {
            "annotation_label": "Segment",
        },
        "target": {
            "annotation_label": "Comment",
        },
    }


def test_PlainTextLineAlignedParser_parse():
    DATA_DIR = get_data_dir()
    source_path = DATA_DIR / "segments.txt"
    target_path = DATA_DIR / "comments.txt"

    metadata = get_metadata()
    plaintext = PlainTextLineAlignedParser.from_files(
        source_path, target_path, metadata
    )
    source_pecha, target_pecha = plaintext.parse()

    assert isinstance(
        source_pecha, Pecha
    ), f"source_pecha is not an instance of Pecha, but {type(source_pecha)}"
    assert isinstance(
        target_pecha, Pecha
    ), f"target_pecha is not an instance of Pecha, but {type(target_pecha)}"
