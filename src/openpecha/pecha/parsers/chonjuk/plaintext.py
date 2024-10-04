import re
from pathlib import Path

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers import BaseParser


class ChonjukPlainTextParser(BaseParser):
    def __init__(self, text: str):
        self.text = text
        self.components = [ChapterParser(self.text)]

    def parse(self, output_path: Path = PECHAS_PATH):
        pecha = Pecha.create(output_path)
        base_name = pecha.set_base(self.text)

        for component in self.components:
            component(pecha, base_name)


class ChapterParser:
    def __init__(self, text: str):
        self.text = text

    def __call__(self, pecha: Pecha, base_name: str):
        chapter_regex = (
            r"ch(\d+)-\"([\u0F00-\u0FFF]+)\"\s*([\u0F00-\u0FFF\s\n]+)[\u0F00-\u0FFF]"
        )
        # Find all matches
        matches = re.finditer(chapter_regex, self.text)

        chapter_anns = []
        # Iterate over the matches and store the spans
        for match in matches:
            curr_match = {
                "chapter_number": match.span(1),
                "chapter_title": match.span(2),
                "Chapter": match.span(3),
            }
            chapter_anns.append(curr_match)

        # Get the updated text with no annotations
        def keep_groups(match):
            return " ".join(match.groups())

        cleaned_text = re.sub(chapter_regex, keep_groups, self.text)  # noqa
        # Get the updated chapter co-ordinate
        updated_chapter_anns = []
        offset = 0
        for chapter_match in chapter_anns:
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

            chapter = chapter_match["Chapter"]
            spaces = chapter[0] - chapter_title[1] - 1
            offset += spaces
            updated_chapter = (chapter[0] - offset, chapter[1] - offset)

            updated_chapter_anns.append(
                {
                    "chapter_number": updated_chapter_number,
                    "chapter_title": updated_chapter_title,
                    "Chapter": updated_chapter,
                }
            )

        # add the chapter to the pecha
        chapter_layer = pecha.add_layer(base_name, LayerEnum.chapter)

        for chapter_ann in updated_chapter_anns:
            chapter_layer = pecha.add_annotation(
                chapter_layer, chapter_ann, LayerEnum.chapter
            )

        chapter_layer.save()
