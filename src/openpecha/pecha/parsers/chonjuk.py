import json
import re
from pathlib import Path
from typing import Dict, List

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers import BaseParser


class ChonjukChapterParser(BaseParser):
    def __init__(self):
        self.regex = (
            r"ch(\d+)-\"([\u0F00-\u0FFF]+)\"\s*([\u0F00-\u0FFF\s\n]+)[\u0F00-\u0FFF]"
        )
        self.updated_text = ""
        self.annotations: List[Dict] = []

    def get_initial_ann_spans(self, text: str):
        """
        Process: - Extract Chapter annotations in the text before removing the string annotations
                 - Store the spans of the chapter annotations
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
                AnnotationType.CHAPTER.value: match.span(3),
            }
            chapter_anns.append(curr_match)
        return chapter_anns

    def get_updated_text(self, text: str):
        """
        Process: Remove the chapter string annotations from the text
        """
        pattern = r"ch\d+-\"[\u0F00-\u0FFF]+\"\s*"

        cleaned_text = re.sub(pattern, "", text)
        return cleaned_text

    def get_annotations(self, text: str):
        """
        Process: Update the chapter annotations after removing the string annotations
        Output: Return the updated chapter annotations
        """
        initial_ann_spans = self.get_initial_ann_spans(text)
        chapter_anns = []
        offset = 0
        for ann_spans in initial_ann_spans:
            start, end = ann_spans["chapter_number"]
            chapter_number = text[start:end]

            start, end = ann_spans["chapter_title"]
            chapter_title = text[start:end]

            start, end = ann_spans[AnnotationType.CHAPTER.value]
            # Update the offset (2 is char length of 'ch' before chapter number)
            offset += start - ann_spans["chapter_number"][0] + 2

            Chapter_span = start - offset, end - offset
            chapter_anns.append(
                {
                    "chapter_number": chapter_number,
                    "chapter_title": chapter_title,
                    AnnotationType.CHAPTER.value: {
                        "start": Chapter_span[0],
                        "end": Chapter_span[1],
                    },
                }
            )
        return chapter_anns

    def parse(
        self,
        input: str,
        metadata: Dict | Path,
        output_path: Path = PECHAS_PATH,
    ) -> Pecha:
        if isinstance(metadata, Path):
            with open(metadata) as f:
                metadata = json.load(f)
        assert isinstance(metadata, dict)

        output_path.mkdir(parents=True, exist_ok=True)

        self.cleaned_text = self.get_updated_text(input)
        self.annotations = self.get_annotations(input)

        pecha = Pecha.create(output_path)
        base_name = pecha.set_base(self.cleaned_text)
        layer, _ = pecha.add_layer(base_name, AnnotationType.CHAPTER)

        for ann in self.annotations:
            pecha.add_annotation(layer, ann, AnnotationType.CHAPTER)

        pecha.set_metadata({"id": pecha.id, "parser": self.name, **metadata})
        layer.save()
        return pecha
