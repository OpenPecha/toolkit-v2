from typing import List, Tuple


class AlignmentMetadata:
    pass


class Alignment:
    def __init__(
        self,
        metadata: AlignmentMetadata,
        parser_segment_pairs=None,
        alignment_segment_pairs=None,
    ):
        self.metadata = metadata
        self.parser_segment_pairs = parser_segment_pairs
        self.alignment_segment_pairs = alignment_segment_pairs

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
        metadata: AlignmentMetadata,
    ):
        return cls(metadata=metadata, parser_segment_pairs=segment_pairs)

    def save(self, path: str):
        pass
