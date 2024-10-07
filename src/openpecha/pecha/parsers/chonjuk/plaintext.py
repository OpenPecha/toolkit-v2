import re
from pathlib import Path
from typing import Dict, List, Union

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers import BaseParser


class ChonjukChapterParser(BaseParser):
    def __init__(self):
        self.regex = (
            r"ch(\d+)-\"([\u0F00-\u0FFF]+)\"\s*([\u0F00-\u0FFF\s\n]+)[\u0F00-\u0FFF]"
        )
        self.updated_text = ""
        self.annotations: List[Dict] = []

    def get_initial_annotations(self, text: str):
        """
        Process:Find Chapter annotations in the text before removing the string annotations
        Output: Return the initial chapter annotations
        """

        # Find all matches
        matches = re.finditer(self.regex, text)

        chapter_anns = []
        # Iterate over the matches and store the spans
        for match in matches:
            curr_match = {
                "chapter_number": match.span(1),
                "chapter_title": match.span(2),
                LayerEnum.chapter.value: match.span(3),
            }
            chapter_anns.append(curr_match)
        return chapter_anns

    def get_updated_text(self, text: str):
        """
        Process: Remove the chapter string annotations from the text
        """

        def keep_groups(match):
            return " ".join(match.groups())

        cleaned_text = re.sub(self.regex, keep_groups, text)
        return cleaned_text

    def get_annotations(self, text: str):
        """
        Process: Update the chapter annotations after removing the string annotations
        Output: Return the updated chapter annotations
        """
        initial_anns = self.get_initial_annotations(text)
        updated_anns = []
        offset = 0
        for chapter_match in initial_anns:
            offset += 2  # Account for 'ch' and '-'
            chapter_number = chapter_match["chapter_number"]
            updated_chapter_number = (
                chapter_number[0] - offset,
                chapter_number[1] - offset,
            )
            offset += 1  # Account for '"'

            chapter_title = chapter_match["chapter_title"]
            updated_chapter_title = (
                chapter_title[0] - offset,
                chapter_title[1] - offset,
            )
            offset += 1  # Account for  '"' and substract a space

            chapter = chapter_match[LayerEnum.chapter.value]
            spaces = chapter[0] - chapter_title[1] - 1
            offset += spaces
            updated_chapter = (chapter[0] - offset, chapter[1] - offset)

            updated_anns.append(
                {
                    "chapter_number": updated_chapter_number,
                    "chapter_title": updated_chapter_title,
                    LayerEnum.chapter.value: updated_chapter,
                }
            )
        return updated_anns

    def parse(
        self,
        input: str,
        output_path: Path = PECHAS_PATH,
        metadata: Union[Dict, Path] = None,
    ):

        self.cleaned_text = self.get_updated_text(input)
        self.annotations = self.get_annotations(input)

        pecha = Pecha.create(output_path)
        base_name = pecha.set_base(self.cleaned_text)
        layer = pecha.add_layer(base_name, LayerEnum.chapter)

        for ann in self.annotations:
            pecha.add_annotation(layer, ann, LayerEnum.chapter)

        layer.save()
