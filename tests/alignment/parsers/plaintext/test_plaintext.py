from pathlib import Path

from openpecha.alignment.parsers.plaintext import PlainTextLineAlignedParser
from openpecha.pecha import Pecha


def get_data_dir():
    return Path(__file__).parent / "data"


def get_metadata():
    return {
        "source": {
            "annotation_category": "Structure Type",
            "annotation_label": "Segment",
        },
        "target": {
            "annotation_category": "Structure Type",
            "annotation_label": "Comment",
        },
    }


def test_plaintext_parse():
    DATA_DIR = get_data_dir()
    source_path = DATA_DIR / "segments.txt"
    target_path = DATA_DIR / "comments.txt"

    metadata = get_metadata()
    plaintext = PlainTextLineAlignedParser.from_files(
        source_path, target_path, metadata
    )
    plaintext.parse()

    assert (
        len(plaintext.source_segments) == 5
    ), "plaintext parser is not parsing source_segments correctly"
    assert (
        len(plaintext.target_segments) == 5
    ), "plaintext parser is not parsing target_segments correctly"


def test_plaintext_save():
    DATA_DIR = get_data_dir()
    source_path = DATA_DIR / "segments.txt"
    target_path = DATA_DIR / "comments.txt"

    metadata = get_metadata()
    plaintext = PlainTextLineAlignedParser.from_files(
        source_path, target_path, metadata
    )
    source_pecha, target_pecha = plaintext.save()

    assert isinstance(
        source_pecha, Pecha
    ), f"source_pecha is not an instance of Pecha, but {type(source_pecha)}"
    assert isinstance(
        target_pecha, Pecha
    ), f"target_pecha is not an instance of Pecha, but {type(target_pecha)}"
