from pathlib import Path
from typing import Dict, List

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.serializers import BaseSerializer
from openpecha.utils import write_json


class PechaDBSerializer(BaseSerializer):
    def __init__(self, output_path: Path = PECHAS_PATH):
        self.output_path = output_path
        self.contents: List[List[str]] = []
        self.mappings: Dict[str, List[int]] = {}
        self.chapter: List[str] = []

    def create_dharmanexus_content_list(self, pecha):
        for _, layers in pecha.layers.items():
            chapter_num = 1
            for ann_store in layers[LayerEnum.meaning_segment]:
                for ann in list(ann_store):
                    segment_id = str(ann.data()[0])
                    segment_text = ann.text()[0]
                    self.chapter.append(segment_text)
                    text_index = len(self.chapter)
                    self.mappings[segment_id] = [chapter_num, text_index]
            chapter_num += 1
            self.contents.append(self.chapter)
            self.chapter = []

    def serialize(self, pecha_path: Path, source_type: str) -> str:
        pecha_id = pecha_path.stem
        pecha = Pecha(pecha_id=pecha_id, pecha_path=pecha_path)
        if source_type == "dharmanexus":
            self.create_dharmanexus_content_list(pecha)
            pecha_json = {
                "title": pecha.metadata.title,
                "language": pecha.metadata.language.value,
                "versionSource": " ",
                "completestatus": "done",
                "content": self.contents,
                "direction": "ltr",
            }
            pecha_db_json_path = f"{self.output_path}/{pecha_id}.json"
            mapping_path = f"{self.output_path}/{pecha_id}_mapping.json"
            write_json(pecha_db_json_path, pecha_json)
            write_json(mapping_path, self.mappings)
            return pecha_db_json_path, mapping_path
        elif source_type == "pedurma":
            pass