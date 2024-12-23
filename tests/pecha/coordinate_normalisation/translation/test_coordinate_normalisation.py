import json
import os
from pathlib import Path
from unittest.mock import patch

from openpecha.pecha.coordinate_normalisation import CoordinateNormalisation
from openpecha.utils import read_json

DATA_DIR = Path(__file__).parent / "data"

source = {"source_pecha_path": DATA_DIR / "IAEB27E9F", "source_base_name": "275D"}
target = {"target_pecha_path": DATA_DIR / "IFA46BBC2", "target_base_name": "4665"}
translation = {
    "translation_pecha_path": DATA_DIR / "I6EA29D09",
    "translation_base_name": "564C",
}
expected_alignment_data = read_json(
    DATA_DIR / "expected_pecha_display_segment_alignment.json"
)


def test_coordinate_normalization():
    with patch(
        "openpecha.pecha.coordinate_normalisation.CoordinateNormalisation.update_metadata"
    ) as mock_update_metadata:
        coordinate_normalisation = CoordinateNormalisation(source, target, translation)
        coordinate_normalisation.normalise_coordinate()
        target_metadata_update = mock_update_metadata.call_args_list[0][1]["dict_data"]
        translation_metadata_update = mock_update_metadata.call_args_list[-1][1][
            "dict_data"
        ]
        pecha_display_alignment_segment_layer_path = translation_metadata_update[
            "pecha_display_segment_alignments"
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
