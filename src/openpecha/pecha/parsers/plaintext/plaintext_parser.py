import re
from typing import Callable, Dict, List

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
            else:
                raise ValueError(
                    "Number of groups in pattern does not match the number of provided group meanings"
                )

        return result

    @staticmethod
    def is_annotation_name_valid(annotation_name: str) -> bool:
        return annotation_name in [layer.value for layer in LayerEnum]

    def parse(self):
        segments = self.segmenter(self.text)
        """ check if annotation name is in LayerEnum """
        if not self.is_annotation_name_valid(self.annotation_name):
            raise ValueError("Invalid annotation name")

        return segments
