from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.json_serializer import JsonSerializer


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
        layer_name = "B5FE/segmentation-4FD1.json"
        annotations = serializer.get_annotations(
            pecha=self.root_pecha, layer_name=layer_name
        )
        expected_annotations = [
            {
                "id": "59EBB25F49",
                "Span": {"start": 0, "end": 206},
                "index": 1,
                "segmentation_type": "segmentation",
            },
            {
                "id": "1C6219999D",
                "Span": {"start": 207, "end": 359},
                "index": 2,
                "segmentation_type": "segmentation",
            },
            {
                "id": "2E324FF8E3",
                "Span": {"start": 360, "end": 506},
                "index": 3,
                "segmentation_type": "segmentation",
            },
            {
                "id": "248229AD9C",
                "Span": {"start": 507, "end": 673},
                "index": 4,
                "segmentation_type": "segmentation",
            },
            {
                "id": "AFF893CC4A",
                "Span": {"start": 674, "end": 843},
                "index": 5,
                "segmentation_type": "segmentation",
            },
            {
                "id": "E6350684CA",
                "Span": {"start": 844, "end": 1034},
                "index": 6,
                "segmentation_type": "segmentation",
            },
            {
                "id": "8725807438",
                "Span": {"start": 1035, "end": 1213},
                "index": 7,
                "segmentation_type": "segmentation",
            },
            {
                "id": "D2BACBFB51",
                "Span": {"start": 1214, "end": 1402},
                "index": 8,
                "segmentation_type": "segmentation",
            },
            {
                "id": "E9DCF0CBEB",
                "Span": {"start": 1403, "end": 1616},
                "index": 9,
                "segmentation_type": "segmentation",
            },
        ]
        assert annotations == expected_annotations

        # Alignment Layer
        layer_name = "B014/alignment-2127.json"
        annotations = serializer.get_annotations(
            pecha=self.commentary_pecha, layer_name=layer_name
        )
        expected_annotations = [
            {
                "id": "5ED5D59969",
                "Span": {"start": 0, "end": 42},
                "index": 1,
                "alignment_index": "1",
                "segmentation_type": "alignment",
            },
            {
                "id": "9DAD7F460F",
                "Span": {"start": 43, "end": 117},
                "index": 2,
                "alignment_index": "2",
                "segmentation_type": "alignment",
            },
            {
                "id": "6850060CDD",
                "Span": {"start": 118, "end": 198},
                "index": 3,
                "alignment_index": "3",
                "segmentation_type": "alignment",
            },
            {
                "id": "88F8B42309",
                "Span": {"start": 199, "end": 290},
                "index": 4,
                "alignment_index": "4",
                "segmentation_type": "alignment",
            },
            {
                "id": "1F86B74B46",
                "Span": {"start": 291, "end": 452},
                "index": 5,
                "alignment_index": "5",
                "segmentation_type": "alignment",
            },
            {
                "id": "E92B454ED1",
                "Span": {"start": 453, "end": 659},
                "index": 6,
                "alignment_index": "6",
                "segmentation_type": "alignment",
            },
            {
                "id": "63937BDD48",
                "Span": {"start": 660, "end": 756},
                "index": 7,
                "alignment_index": "7",
                "segmentation_type": "alignment",
            },
            {
                "id": "BC7A7FDA98",
                "Span": {"start": 757, "end": 1065},
                "index": 8,
                "alignment_index": "8",
                "segmentation_type": "alignment",
            },
            {
                "id": "23834A44D3",
                "Span": {"start": 1066, "end": 1142},
                "index": 9,
                "alignment_index": "9",
                "segmentation_type": "alignment",
            },
        ]
        assert annotations == expected_annotations


if __name__ == "__main__":
    test = TestJsonSerializer()

    test.setUp()
    test.test_get_annotations()
