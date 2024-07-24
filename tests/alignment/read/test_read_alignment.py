from pathlib import Path
from typing import Dict

from openpecha.alignment import Alignment
from openpecha.pecha import Pecha


def test_read_alignment():
    DATA = Path(__file__).parent / "data"
    alignment_path = DATA / "A0FAF24AC"
    source_id, target_id = (
        "I72772C62",
        "I01F61FAA",
    )
    pechas: Dict[str, Pecha] = {
        source_id: Pecha.from_path(DATA / source_id),
        target_id: Pecha.from_path(DATA / target_id),
    }
    alignment = Alignment.from_path(alignment_path, pechas=pechas)
    assert isinstance(alignment, Alignment)


test_read_alignment()
