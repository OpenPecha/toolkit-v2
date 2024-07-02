from typing import Dict

from openpecha.pecha.annotation import Annotation


class Pecha:
    def __init__(self, pecha_id: str, segments: Dict[str, str]) -> None:
        self.pecha_id = pecha_id
        self.segments = segments
        self.base_text = "".join(segments.values())
        self.annotations = self.set_annotations()

    @classmethod
    def from_path(cls, path: str):
        pass

    @classmethod
    def from_id(cls, pecha_id: str):
        pass

    def set_annotations(self):
        char_count = 0
        for segment_id, segment in self.segments.items():
            annotation = Annotation(
                annotation_id=segment_id,
                segment=segment,
                start=char_count,
                end=char_count + len(segment),
            )
            char_count += len(segment)
            yield annotation
