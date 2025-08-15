from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.json import JsonSerializer
from openpecha.pecha.serializers import SerializerLogicHandler
from openpecha.utils import read_json, write_json


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

    # def test_serialize_alignment(self):
    #     serializer = JsonSerializer()

    #     # ALIGNMENT
    #     layer_path = "B014/alignment-2127.json"
    #     annotations = serializer.serialize(
    #         pecha=self.commentary_pecha, layer_paths=layer_path
    #     )
    #     expected_annotations = read_json(self.DATA_DIR / "alignment_annotations.json")
    #     assert annotations == expected_annotations

    # def test_serialize_segmentation_and_alignment(self):
    #     serializer = JsonSerializer()

    #     # SEGMENTATION AND ALIGNMENT(Annotations for Edition)
    #     layer_paths = ["B014/segmentation-33FC.json", "B014/alignment-2127.json"]
    #     annotations = serializer.serialize(
    #         pecha=self.commentary_pecha, layer_paths=layer_paths
    #     )
    #     expected_annotations = read_json(self.DATA_DIR / "edition_annotations.json")
    #     assert annotations == expected_annotations

    def test_insertion_on_get_edition_base(self):
        serializer = JsonSerializer()

        pecha_path = self.DATA_DIR / "IA099A11B"
        pecha = Pecha.from_path(pecha_path)
        edition_layer_path = "4C00/version-9D95.json"
        edition_base = serializer.get_edition_base(pecha, edition_layer_path)
        expected_edition_base = Path(self.DATA_DIR / "insertion.txt").read_text(
            encoding="utf-8"
        )
        assert edition_base == expected_edition_base

    def test_deletion_on_get_edition_base(self):
        serializer = JsonSerializer()

        pecha_path = self.DATA_DIR / "IA099A11B"
        pecha = Pecha.from_path(pecha_path)
        edition_layer_path = "4C00/version-658D.json"
        edition_base = serializer.get_edition_base(pecha, edition_layer_path)
        expected_edition_base = Path(self.DATA_DIR / "deletion.txt").read_text(
            encoding="utf-8"
        )
        assert edition_base == expected_edition_base

    def test_insertion_and_deletion_on_get_edition_base(self):
        serializer = JsonSerializer()

        pecha_path = self.DATA_DIR / "IA099A11B"
        pecha = Pecha.from_path(pecha_path)
        edition_layer_path = "4C00/version-6816.json"
        edition_base = serializer.get_edition_base(pecha, edition_layer_path)
        expected_edition_base = Path(
            self.DATA_DIR / "insertion_and_deletion.txt"
        ).read_text(encoding="utf-8")
        assert edition_base == expected_edition_base


class TestSerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.opf_path =  Path("tests/pecha/serializers/json/data/ID8Sv2ynVKZX8wIt")
        self.opf = Pecha.from_path(self.opf_path)

    
    def test_critical_serializer(self):
        annotations = [
            {
                "id":"Tm3Uewnh3ySsvgIE",
                "type":"segmentation"
            },
            {
                "id":"pdpDABvI2yRSISt6",
                "type":"alignment"
            }]
        target = {
            "pecha": self.opf,
            "annotations": annotations
        }
        serialized_data = SerializerLogicHandler().serialize(target)

        if hasattr(serialized_data, 'model_dump'):
            serialized_dict = serialized_data.model_dump()
        else:
            serialized_dict = serialized_data

        expected_serialized_data = read_json(
            self.DATA_DIR / "critical_annotations.json"
        )
        assert serialized_dict == expected_serialized_data
    

    def test_diplomatic_serializer(self):
        annotations = [
            {"id":"ko2uLrLUEyeejg7y",
                "type":"version"
            }]
        target = {
            "pecha": self.opf,
            "annotations": annotations
        }
        serialized_data = SerializerLogicHandler().serialize(target)

        if hasattr(serialized_data, 'model_dump'):
            serialized_dict = serialized_data.model_dump()
        else:
            serialized_dict = serialized_data

        expected_serialized_data = read_json(
            self.DATA_DIR / "diplomatic_annotations.json"
        )
        assert serialized_dict == expected_serialized_data
