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
            {"id": "59EBB25F49", "index": 1, "segmentation_type": "segmentation"},
            {"id": "1C6219999D", "index": 2, "segmentation_type": "segmentation"},
            {"id": "2E324FF8E3", "index": 3, "segmentation_type": "segmentation"},
            {"id": "248229AD9C", "index": 4, "segmentation_type": "segmentation"},
            {"id": "AFF893CC4A", "index": 5, "segmentation_type": "segmentation"},
            {"id": "E6350684CA", "index": 6, "segmentation_type": "segmentation"},
            {"id": "8725807438", "index": 7, "segmentation_type": "segmentation"},
            {"id": "D2BACBFB51", "index": 8, "segmentation_type": "segmentation"},
            {"id": "E9DCF0CBEB", "index": 9, "segmentation_type": "segmentation"},
        ]
        assert annotations == expected_annotations


if __name__ == "__main__":
    test = TestJsonSerializer()

    test.setUp()
    test.test_get_annotations()
