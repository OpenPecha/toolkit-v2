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
        self.chapter: Dict[int, List] = {}

    def get_order_of_dharmanexus_base(self, pecha: Pecha):
        """
        For Dharmanexus, the order of the base is stored in the metadata
        in the Pecha bases attribute.
        """
        chapter_dict = {}
        for base_metadata in pecha.metadata.bases:
            basename = next(iter(base_metadata.keys()))
            base_order = base_metadata[basename].get("order")
            if base_order:
                chapter_dict[base_order] = basename

        return chapter_dict

    def create_dharmanexus_content_list(self, pecha):
        chapter_dict = self.get_order_of_dharmanexus_base(pecha)
        for chapter_num in range(1, len(chapter_dict.keys()) + 1):
            basename = chapter_dict[chapter_num]
            self.chapter[chapter_num] = []
            text_index = 1
            for ann_store in pecha.layers[basename][LayerEnum.meaning_segment]:
                for ann in list(ann_store):
                    segment_id = str(ann.data()[0])
                    segment_text = ann.text()[0]
                    self.chapter[chapter_num].append(segment_text)
                    self.mappings[segment_id] = [chapter_num, text_index]
                    text_index += 1

        for chapter_num in range(1, len(self.chapter.keys()) + 1):
            self.contents.append(self.chapter[chapter_num])
        self.chapter = {}

    def serialize(self, pecha_path: Path, source_type: str):
        pecha_id = pecha_path.stem
        pecha = Pecha(pecha_id=pecha_id, pecha_path=pecha_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

        pecha_json = {
            "title": pecha.metadata.title,
            "language": pecha.metadata.language.value,
            "versionSource": " ",
            "completestatus": "done",
            "content": [],
            "direction": "ltr",
        }

        if source_type == "dharmanexus":
            self.create_dharmanexus_content_list(pecha)
            pecha_db_json_path = f"{self.output_path}/{pecha_id}.json"
            mapping_path = f"{self.output_path}/{pecha_id}_mapping.json"
            pecha_json["content"] = self.contents
            write_json(pecha_db_json_path, pecha_json)
            write_json(mapping_path, self.mappings)
            return pecha_db_json_path, mapping_path
        elif source_type == "pedurma":
            self.create_pedurma_content_list(pecha)
            pecha_json["content"] = self.contents
            pecha_db_json_path = f"{self.output_path}/{pecha_id}.json"
            write_json(pecha_db_json_path, pecha_json)

    def create_pedurma_content_list(self, pecha):
        self.contents = []
        for _, layer in pecha.layers.items():
            curr_chapter = []
            meaning_segment_layer = layer[LayerEnum.meaning_segment][0]
            durchen_layer = layer[LayerEnum.durchen][0]
            for ann in meaning_segment_layer:
                meaning_segment = str(ann)
                curr_content = meaning_segment
                text_selection = next(ann.textselections())
                start, end = text_selection.begin(), text_selection.end()
                # Find if durchen ann is present in the segment
                for durchen_ann in durchen_layer:
                    durchen_text_selection = next(durchen_ann.textselections())
                    durchen_start, durchen_end = (
                        durchen_text_selection.begin(),
                        durchen_text_selection.end(),
                    )
                    if durchen_start >= start and durchen_end <= end:
                        ann_data = next(durchen_ann.data())
                        note_ann = str(ann_data.value())
                        # Structure note ann with meaning segment
                        segment_left_side = str(ann)[: durchen_start - start]
                        segment_right_side = str(ann)[durchen_end - end :]
                        note_reprentation = f"<sup>*</sup> <i class='footnote'><b>{str(durchen_ann)}</b> {note_ann}</i>"

                        curr_content = (
                            segment_left_side + note_reprentation + segment_right_side
                        )
                        break
                curr_chapter.append(curr_content)
                curr_content = ""

            self.contents.append(curr_chapter)
