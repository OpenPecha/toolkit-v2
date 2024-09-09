import re
from typing import Callable, List


class PlainTextParser:
    def __init__(
        self, text: str, segmenter: Callable[[str], List[str]], annotation_name: str
    ):
        self.text = text
        self.segmenter = segmenter
        self.annotation_name = annotation_name

    @staticmethod
    def space_segmenter(text: str):
        return text.split(" ")

    @staticmethod
    def new_line_segmenter(text: str):
        return text.split("\n")

    @staticmethod
    def regex_segmenter(text: str, pattern: str, group_mapping: List[str]):
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

    def parse(self):
        segments = self.segmenter(self.text)
        print(segments)
