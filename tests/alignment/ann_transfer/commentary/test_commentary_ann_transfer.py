from pathlib import Path
from unittest import mock

from openpecha.alignment.ann_transfer.commentary import CommentaryAlignmentAnnTransfer

DATA_DIR = Path(__file__).parent / "data"

source = {"source_pecha_path": DATA_DIR / "P2/IA6ED8F68", "source_base_name": "CCF2"}
target = {"target_pecha_path": DATA_DIR / "P1/I44F30CFF", "target_base_name": "9829"}

commentary = {
    "commentary_pecha_path": DATA_DIR / "P3/IBB99C5E4",
    "commentary_base_name": "E3E4",
}


@mock.patch(
    "openpecha.alignment.ann_transfer.commentary.CommentaryAlignmentAnnTransfer.update_metadata",
    return_value=None,
)
def test_alignment_ann_transfer(mock_update_metadata):
    ann_transfer = CommentaryAlignmentAnnTransfer(source, target, commentary)
    ann_transfer.transfer_annotation()


test_alignment_ann_transfer()
