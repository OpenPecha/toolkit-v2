from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.serializers import SerializerLogicHandler
from openpecha.utils import read_json


class TestAlignedPechaSerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.target_opf_path =  Path("tests/pecha/serializers/json/data/ID8Sv2ynVKZX8wIt")
        self.source_opf_path =  Path("tests/pecha/serializers/json/data/6vjxAfJTuTJS04XY")
        self.target_opf = Pecha.from_path(self.target_opf_path)
        self.source_opf = Pecha.from_path(self.source_opf_path)

    
    def test_translation_alignment_serializer(self):
        target_annotations = [
            {
                "id":"Tm3Uewnh3ySsvgIE",
                "type":"segmentation"
            },
            {
                "id":"pdpDABvI2yRSISt6",
                "type":"alignment"
            }]
        source_annotations = [
            {
                "id": "vLtbNleDhsAnICle",
                "type":"alignment",
                "aligned_to": "pdpDABvI2yRSISt6"
            }]
        target = {
            "pecha": self.target_opf,
            "annotations": target_annotations
        }
        source = {
            "pecha": self.source_opf,
            "annotations": source_annotations
        }
        serialized_data = SerializerLogicHandler().serialize(target, source)

        if hasattr(serialized_data, 'model_dump'):
            serialized_dict = serialized_data.model_dump()
        else:
            serialized_dict = serialized_data
        
        expected_serialized_data = read_json(
            self.DATA_DIR / "translation_alignment_one.json"
        )
        assert serialized_dict == expected_serialized_data


class TestCustomAlignedPechaSerializer(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.target_opf_path =  Path("tests/pecha/serializers/json/data/Vj8Y63ztAMKTWxFu")
        self.source_opf_path =  Path("tests/pecha/serializers/json/data/XH0b7XLRxxrEGncv")
        self.target_opf = Pecha.from_path(self.target_opf_path)
        self.source_opf = Pecha.from_path(self.source_opf_path)

    
    def test_translation_alignment_serializer(self):
        target_annotations = [
            {
                "id": "6q4epxlzV7qet1SV",
                "type": "alignment"
            },
            {
                "id": "SBlFlCttljxUhOYM",
                "type": "alignment"
            },
            {
                "id": "koFhb2tdmZ6z3DjA",
                "type": "segmentation"
            }
        ]
        source_annotations = [
            {
                "id": "f1k4V3N8jC9kiOFa",
                "type": "alignment",
                "aligned_to": "koFhb2tdmZ6z3DjA"
            }
        ]
        target = {
            "pecha": self.target_opf,
            "annotations": target_annotations
        }
        source = {
            "pecha": self.source_opf,
            "annotations": source_annotations
        }
        serialized_data = SerializerLogicHandler().serialize(target, source)

        print("SERIALIZED DATA \n", serialized_data)