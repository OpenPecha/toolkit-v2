import re
from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.serializers import BaseSerializer
from openpecha.utils import read_json


class PechaDBSerializer(BaseSerializer):
    def __init__(self):
        self.contents: List[List[str]] = []
        self.mappings: Dict[str, List[int]] = {}
        self.chapter: Dict[int, List] = {}

    def get_order_of_dharmanexus_base(self, pecha: Pecha):
        """
        For Dharmanexus, the order of the base is stored in the metadata
        in the Pecha bases attribute.
        """
        chapter_dict = {}
        for basename, base_metadata in pecha.metadata.bases.items():
            base_order = base_metadata["order"]
            if base_order:
                chapter_dict[base_order] = basename

        return chapter_dict

    def create_dharmanexus_content_list(self, pecha):
        chapter_dict = self.get_order_of_dharmanexus_base(pecha)
        chapter_num = 1
        self.chapter[chapter_num] = []
        text_index = 1
        for vol_num in range(1, len(chapter_dict.keys()) + 1):
            basename = chapter_dict[vol_num]
            if text_index == 101:
                chapter_num += 1
                text_index = 1
                self.chapter[chapter_num] = []
            for ann_store in pecha.layers[basename][AnnotationType.SEGMENTATION]:
                for ann in list(ann_store):
                    segment_id = str(ann.data()[0])
                    segment_text = ann.text()[0]
                    if text_index == 101:
                        chapter_num += 1
                        text_index = 1
                        self.chapter[chapter_num] = []
                        self.chapter[chapter_num].append(segment_text)
                        self.mappings[segment_id] = [chapter_num, text_index]
                        text_index += 1
                    else:
                        self.chapter[chapter_num].append(segment_text)
                        self.mappings[segment_id] = [chapter_num, text_index]
                        text_index += 1

        for chapter_num in range(1, len(self.chapter.keys()) + 1):
            self.contents.append(self.chapter[chapter_num])
        self.chapter = {}

    def serialize(self, pecha_path: Path, source_type: str):
        pecha_id = pecha_path.stem
        pecha = Pecha(pecha_id=pecha_id, pecha_path=pecha_path)

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
            pecha_json["content"] = self.contents
            return pecha_json, self.mappings
        elif source_type == "pedurma":
            self.create_pedurma_content_list(pecha)
            pecha_json["content"] = self.contents
            return pecha_json

    def create_pedurma_content_list(self, pecha):
        self.contents = []
        for _, layer in pecha.layers.items():
            curr_chapter = []
            meaning_segment_layer = layer[AnnotationType.SEGMENTATION][0]
            durchen_layer = layer[AnnotationType.DURCHEN][0]
            for ann in meaning_segment_layer:
                meaning_segment = str(ann)
                text_selection = next(ann.textselections())
                start, end = text_selection.begin(), text_selection.end()
                offset = 0
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
                        # Remove numbering from the note ann Eg: (3) <«སྣར་»«པེ་»འཇམ་> -> <«སྣར་»«པེ་»འཇམ་>
                        note_ann = re.sub(r"\(\d+\)\s", "", note_ann)
                        # Remove the pointing bracket from note annotaion <«སྣར་»«པེ་»འཇམ་> -> «སྣར་»«པེ་»འཇམ་
                        note_ann = re.sub(r"<|>", "", note_ann)
                        # Structure note ann with meaning segment
                        segment_left_side = meaning_segment[
                            : durchen_end - start + offset
                        ]
                        segment_right_side = meaning_segment[
                            durchen_end - start + offset :
                        ]
                        note_reprentation = f"<sup class='footnote-marker'>*</sup><i class='footnote'><b>{str(durchen_ann)}</b>{note_ann}</i>"

                        meaning_segment = (
                            segment_left_side + note_reprentation + segment_right_side
                        )
                        offset += len(note_reprentation)

                curr_chapter.append(meaning_segment)

            self.contents.append(curr_chapter)


def chapterize_serialized_json(json_file: Path, chapter_size: int = 200):
    """
    Splits JSON content into chapters of fixed size and saves to a new file.
    Input JSON must have structure: {"content": [[text1, text2, ...]]}.
    Returns path to the output file.
    """
    data = read_json(json_file)
    content_data = data["content"][0]

    new_content = []
    for i in range(0, len(content_data), chapter_size):
        new_content.append(content_data[i : i + chapter_size])

    data["content"] = new_content

    return data
