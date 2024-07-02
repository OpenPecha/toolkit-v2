from pathlib import Path

from openpecha.alignment.parsers.plaintext import PlainText
from openpecha.pecha import Pecha


def test_plaintext_parse():
    DATA_DIR = Path(__file__).parent / "data"
    source_path = DATA_DIR / "segments.txt"
    target_path = DATA_DIR / "comments.txt"

    metadata = {
        "source": {
            "annotation_category": "Structure Type",
            "annotation_label": "Segment",
        },
        "target": {
            "annotation_category": "Structure Type",
            "annotation_label": "Comment",
        },
    }
    plaintext = PlainText.from_files(source_path, target_path, metadata)
    plaintext.parse()

    assert (
        len(plaintext.source_segments) == 5
    ), "plaintext parser is not parsing source_segments correctly"
    assert (
        len(plaintext.target_segments) == 5
    ), "plaintext parser is not parsing target_segments correctly"


def test_plaintext_save():
    DATA_DIR = Path(__file__).parent / "data"
    source_path = DATA_DIR / "segments.txt"
    target_path = DATA_DIR / "comments.txt"

    metadata = {
        "source": {
            "annotation_category": "Structure Type",
            "annotation_label": "Segment",
        },
        "target": {
            "annotation_category": "Structure Type",
            "annotation_label": "Comment",
        },
    }
    plaintext = PlainText.from_files(source_path, target_path, metadata)
    source_pecha, target_pecha = plaintext.save()

    assert isinstance(
        source_pecha, Pecha
    ), "plaintext parser is not saving source_pecha as an instance of Pecha"
    assert isinstance(
        target_pecha, Pecha
    ), "plaintext parser is not saving target_pecha as an instance of Pecha"
