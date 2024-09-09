import re
from pathlib import Path
from typing import Callable, Dict, List

from stam import Offset, Selector

from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum


class PlainTextParser:
    def __init__(
        self, text: str, segmenter: Callable[[str], List[str]], annotation_name: str
    ):
        self.text = text
        self.segmenter = segmenter
        self.annotation_name = annotation_name

    @staticmethod
    def space_segmenter(text: str) -> List[Dict]:
        res = []
        char_count = 0
        for word in text.split(" "):
            res.append(
                {
                    "annotation_text": word,
                    "start": char_count,
                    "end": char_count + len(word),
                }
            )
            char_count += len(word) + 1
        return res

    @staticmethod
    def new_line_segmenter(text: str) -> List[Dict]:
        res = []
        char_count = 0
        for line in text.split("\n"):
            res.append(
                {
                    "annotation_text": line,
                    "start": char_count,
                    "end": char_count + len(line),
                }
            )
            char_count += len(line) + 1
        return res

    @staticmethod
    def regex_segmenter(
        text: str, pattern: str, group_mapping: List[str]
    ) -> List[Dict]:
        if "annotation_text" not in group_mapping:
            raise ValueError("group_mapping must contain 'annotation_text'")

        matches = re.finditer(pattern, text)
        result = []

        for match in matches:
            groups = match.groups()
            if len(groups) == len(group_mapping):
                segment_data = {group_mapping[i]: groups[i] for i in range(len(groups))}

                # Add start and end indices for the "annotation_text" group
                annotation_index = group_mapping.index("annotation_text")
                start, end = match.span(
                    annotation_index + 1
                )  # +1 because group 0 is the entire match
                segment_data["start"] = start
                segment_data["end"] = end

                result.append(segment_data)
            else:
                raise ValueError(
                    "Number of groups in pattern does not match the number of provided group meanings"
                )

        return result

    @staticmethod
    def is_annotation_name_valid(annotation_name: str) -> bool:
        return annotation_name in [layer.value for layer in LayerEnum]

    def parse(self, output_path: Path):
        segments = self.segmenter(self.text)
        """ check if annotation name is in LayerEnum """
        if not self.is_annotation_name_valid(self.annotation_name):
            raise ValueError("Invalid annotation name")

        """create pecha file"""
        pecha_id = get_initial_pecha_id()
        pecha_path = _mkdir(output_path / pecha_id)
        pecha = Pecha(pecha_id=pecha_id, pecha_path=pecha_path)

        """ create base file for new annotation store"""
        basefile_name, base_content = get_uuid()[:4], self.text
        pecha.set_base(basefile_name, base_content)

        """ create annotation layer """
        ann_store = pecha.create_ann_store(
            basefile_name, LayerEnum(self.annotation_name)
        )
        ann_resource = next(ann_store.resources())
        ann_dataset = next(ann_store.datasets())
        ann_type_id = get_uuid()
        for segment in segments:
            assert isinstance(segment, dict)
            text_selector = Selector.textselector(
                ann_resource, Offset.simple(segment["start"], segment["end"])
            )
            ann_data = [
                {"id": get_uuid(), "set": ann_dataset.id(), "key": k, "value": v}
                for k, v in segment.items()
                if k not in ["start", "end", "annotation_text"]
            ]
            pecha.annotate(
                ann_store,
                text_selector,
                LayerEnum(self.annotation_name),
                ann_type_id,
                ann_data,
            )
        pecha.save_ann_store(ann_store, LayerEnum(self.annotation_name), basefile_name)
