from pathlib import Path

from openpecha.alignment import Alignment


def test_read_alignment():
    DATA = Path(__file__).parent / "data"
    alignment_path = DATA / "A9BB545D5"
    alignment = Alignment.from_path(alignment_path)
    assert isinstance(alignment, Alignment)


test_read_alignment()
