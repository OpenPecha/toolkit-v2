from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.json_serializer import JsonSerializer
from openpecha.utils import read_json


class TestJsonSerializer(TestCase):
    def setUp(self):
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/root/I6556B464"
        )
        self.commentary_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/commentary/I015AFFA7"
        )
        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.commentary_pecha = Pecha.from_path(self.commentary_pecha_path)

        self.DATA_DIR = Path(__file__).parent / "data"

    def test_get_base(self):
        serializer = JsonSerializer()
        base = serializer.get_base(self.root_pecha)

        expected_base = Path(
            "tests/alignment/commentary_transfer/data/root/I6556B464/base/B5FE.txt"
        ).read_text(encoding="utf-8")
        assert base == expected_base

    def test_get_annotations(self):
        serializer = JsonSerializer()

        # SEGMENTATION
        layer_path = "B5FE/segmentation-4FD1.json"
        annotations = serializer.get_annotations(
            pecha=self.root_pecha, layer_paths=layer_path
        )
        expected_annotations = read_json(
            self.DATA_DIR / "segmentation_annotations.json"
        )
        assert annotations == expected_annotations

        # ALIGNMENT
        layer_path = "B014/alignment-2127.json"
        annotations = serializer.get_annotations(
            pecha=self.commentary_pecha, layer_paths=layer_path
        )
        expected_annotations = read_json(self.DATA_DIR / "alignment_annotations.json")
        assert annotations == expected_annotations

        # SEGMENTATION AND ALIGNMENT(Annotations for Edition)
        layer_paths = ["B014/segmentation-33FC.json", "B014/alignment-2127.json"]
        annotations = serializer.get_annotations(
            pecha=self.commentary_pecha, layer_paths=layer_paths
        )
        expected_annotations = read_json(self.DATA_DIR / "edition_annotations.json")
        assert annotations == expected_annotations
