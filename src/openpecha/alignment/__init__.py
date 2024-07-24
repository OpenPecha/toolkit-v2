from typing import List, Tuple

from openpecha.alignment.metadata import AlignmentMetaData


class Alignment:
    def __init__(
        self,
        metadata: AlignmentMetaData,
        segment_pairs=None,
    ):
        self.metadata = metadata
        self.segment_pairs = segment_pairs

    @classmethod
    def from_path(cls, path: str):
        pass

    @classmethod
    def from_id(cls, alignment_id: str):
        pass

    @classmethod
    def from_segment_pairs(
        cls,
        segment_pairs: List[Tuple[Tuple[str, str], Tuple[str, str]]],
        metadata: AlignmentMetaData,
    ):
        return cls(metadata=metadata, segment_pairs=segment_pairs)

    def save(self, path: str):
        pass
