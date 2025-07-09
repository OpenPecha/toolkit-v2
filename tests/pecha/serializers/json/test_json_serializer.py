from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.json import JsonSerializer


class TestJsonSerializer(TestCase):
    def setUp(self):
        self.pecha_path = Path(
            "tests/alignment/commentary_transfer/data/root/I6556B464"
        )
        self.pecha = Pecha.from_path(self.pecha_path)

    def test_get_base(self):
        serializer = JsonSerializer()
        base = serializer.get_base(self.pecha)

        expected_base = Path(
            "tests/alignment/commentary_transfer/data/root/I6556B464/base/B5FE.txt"
        ).read_text(encoding="utf-8")
        assert base == expected_base

    def test_get_annotations(self):
        serializer = JsonSerializer()
        layer_name = "B5FE/segmentation-4FD1.json"

        annotations = serializer.get_annotations(
            pecha=self.pecha, layer_name=layer_name
        )
        expected_annotations = [
            {"index": 1, "segmentation_type": "segmentation"},
            {"index": 2, "segmentation_type": "segmentation"},
            {"index": 3, "segmentation_type": "segmentation"},
            {"index": 4, "segmentation_type": "segmentation"},
            {"index": 5, "segmentation_type": "segmentation"},
            {"index": 6, "segmentation_type": "segmentation"},
            {"index": 7, "segmentation_type": "segmentation"},
            {"index": 8, "segmentation_type": "segmentation"},
            {"index": 9, "segmentation_type": "segmentation"},
        ]
        assert annotations == expected_annotations
