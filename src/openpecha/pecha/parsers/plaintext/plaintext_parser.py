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
    def space_segmenter(text: str) -> List[Dict[str, str]]:
        return [{"annotation_text": ann_text} for ann_text in text.split(" ")]

    @staticmethod
    def new_line_segmenter(text: str) -> List[Dict[str, str]]:
        return [{"annotation_text": ann_text} for ann_text in text.split("\n")]

    @staticmethod
    def regex_segmenter(
        text: str, pattern: str, group_mapping: List[str]
    ) -> List[Dict[str, str]]:
        if "annotation_text" not in group_mapping:
            raise ValueError("group_mapping must contain 'annotation_text'")

        matches = re.findall(pattern, text)
        result = []

        for match in matches:
            if len(match) == len(group_mapping):
                # Create a dictionary that maps group meanings to the matched groups
                result.append({group_mapping[i]: match[i] for i in range(len(match))})
                # Add start and end indicies of "annotation_text" group

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
        char_count = 0  # noqa
        for segment in segments:
            text_selector = Selector.textselector(ann_resource, Offset.simple())  # noqa
            pecha.annotate(
                ann_store,
            )
