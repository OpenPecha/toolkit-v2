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
