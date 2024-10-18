import re
from pathlib import Path
from typing import Dict, List, Optional, Union

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import PechaMetaData
from openpecha.pecha.parsers import BaseParser
from openpecha.utils import read_json


class GoogleDocParser(BaseParser):
    def __init__(self, source_type: str, root_id: Optional[str] = None):
        self.source_type = source_type

        self.root_segment_splitter = "\n"
        self.anns: List[Dict] = []
        self.root_base = ""

    def normalize_text(self, text: str):
        text = self.normalize_whitespaces(text)
        text = self.normalize_newlines(text)
        return text

    @staticmethod
    def normalize_whitespaces(text: str):
        """
        If there are spaces or tab between newlines, it will be removed.
        """
        return re.sub(r"\n[\s\t]+\n", "\n\n", text)

    @staticmethod
    def normalize_newlines(text: str):
        """
        If there are more than 2 newlines continously, it will replace it with 2 newlines.
        """
        return re.sub(r"\n{3,}", "\n\n", text)

    def parse(
        self,
        input: str,
        metadata: Union[Dict, Path],
        output_path: Path = PECHAS_PATH,
    ) -> Pecha:
        input = self.normalize_text(input)
        if input.startswith("\ufeff"):
            input = input[1:]

        char_count = 0
        self.anns = []
        base_text = []
        for segment in input.split(self.root_segment_splitter):
            segment = segment.strip()

            match = re.search(r"^(\d+)\.", segment)
            if match:
                root_idx_num = match.group(1)
                segment = segment.replace(f"{root_idx_num}.", "")
                segment = segment.strip()

                curr_segment_ann = {
                    LayerEnum.meaning_segment.value: {
                        "start": char_count,
                        "end": char_count + len(segment),
                    },
                    "root_idx": int(root_idx_num),
                }

            else:
                curr_segment_ann = {
                    LayerEnum.meaning_segment.value: {
                        "start": char_count,
                        "end": char_count + len(segment),
                    }
                }

            self.anns.append(curr_segment_ann)
            base_text.append(segment)
            char_count += len(segment)
            char_count += 1  # for newline

        # Create pecha and add Meaning Segment Layer
        pecha = Pecha.create(output_path)

        self.root_base = "\n".join(base_text)
        basename = pecha.set_base(self.root_base)
        meaning_segment_layer, _ = pecha.add_layer(basename, LayerEnum.meaning_segment)
        for ann in self.anns:
            pecha.add_annotation(meaning_segment_layer, ann, LayerEnum.meaning_segment)

        if isinstance(metadata, Path):
            metadata = read_json(metadata)
        assert isinstance(metadata, dict)

        pecha.set_metadata(PechaMetaData(id=pecha.id, parser=self.name, **metadata))

        meaning_segment_layer.save()

        return pecha
