import re
from pathlib import Path

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.parsers import BaseParser


class ChonjukPlainTextParser(BaseParser):
    def __init__(self, text: str):
        self.text = text
        self.components = [ChapterParser(self.text)]

    def parse(self, output_path: Path = PECHAS_PATH):
        pecha = Pecha.create(output_path)
        base_name = pecha.set_base(self.text)

        for component in self.components:
            component(base_name)


class ChapterParser:
    def __init__(self, text: str):
        self.text = text

    def __call__(self, base_name: str):
        chapter_regex = (
            r"ch(\d+)-\"([\u0F00-\u0FFF]+)\"\s*([\u0F00-\u0FFF\s\n]+)[\u0F00-\u0FFF]"
        )
        # Find all matches
        matches = re.finditer(chapter_regex, self.text)

        chapter_matches = []
        # Iterate over the matches and store the spans
        for match in matches:
            curr_match = {
                "chapter_number_span": match.span(1),
                "title_span": match.span(2),
                "content_span": match.span(3),
            }
            chapter_matches.append(curr_match)

        # Get the updated text with no annotations
        def keep_groups(match):
            return " ".join(match.groups())

        cleaned_text = re.sub(chapter_regex, keep_groups, self.text)  # noqa
        # Get the updated chapter co-ordinate
        updated_chapter_matches = []
        offset = 0
        for chapter_match in chapter_matches:
            offset += 2  # Account for 'ch' and '-'
            chapter_no_span = chapter_match["chapter_number_span"]
            updated_chapter_no_span = (
                chapter_no_span[0] - offset,
                chapter_no_span[1] - offset,
            )
            offset += 1  # Account for '"'

            title_span = chapter_match["title_span"]
            updated_title_span = (title_span[0] - offset, title_span[1] - offset)
            offset += 1  # Account for  '"' and substract a space

            content_span = chapter_match["content_span"]
            spaces = content_span[0] - title_span[1] - 1
            offset += spaces
            updated_content_span = (content_span[0] - offset, content_span[1] - offset)

            updated_chapter_matches.append(
                {
                    "chapter_number_span": updated_chapter_no_span,
                    "title_span": updated_title_span,
                    "content_span": updated_content_span,
                }
            )
