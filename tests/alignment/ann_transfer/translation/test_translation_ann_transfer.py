import json
import os
from pathlib import Path
from unittest.mock import patch

from openpecha.alignment.alignment import AlignmentEnum
from openpecha.alignment.ann_transfer.translation import TranslationAlignmentAnnTransfer
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"

source = {"pecha_path": DATA_DIR / "IAEB27E9F", "source_base_name": "275D"}
target = {"pecha_path": DATA_DIR / "IFA46BBC2", "target_base_name": "4665"}
translation = {
    "pecha_path": DATA_DIR / "I6EA29D09",
    "translation_base_name": "564C",
}
expected_alignment_data = read_json(
    DATA_DIR / "expected_pecha_display_segment_alignment.json"
)


def test_coordinate_normalization():
    with patch(
        "openpecha.alignment.ann_transfer.translation.TranslationAlignmentAnnTransfer.update_metadata"
    ) as mock_update_metadata:
        coordinate_normalisation = TranslationAlignmentAnnTransfer(
            source, target, translation
        )
        coordinate_normalisation.transfer_annotation()
        target_metadata_update = mock_update_metadata.call_args_list[0][1][
            "new_metadata"
        ]
        translation_metadata_update = mock_update_metadata.call_args_list[-1][1][
            "new_metadata"
        ]
        pecha_display_alignment_segment_layer_path = translation_metadata_update[
            AlignmentEnum.pecha_display_alignments.value
        ][0]["translation"]
        transfered_layer_path = target_metadata_update["segmentation_transfered"][0][
            "transfered"
        ]
        assert Path(pecha_display_alignment_segment_layer_path).exists()
        assert Path(transfered_layer_path).exists()
        assert json.dumps(coordinate_normalisation.alignment_data) == json.dumps(
            expected_alignment_data
        )
        os.remove(Path(transfered_layer_path))
        os.remove(Path(pecha_display_alignment_segment_layer_path))


test_coordinate_normalization()
