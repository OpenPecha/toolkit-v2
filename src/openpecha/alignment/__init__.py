from typing import Dict, List, Tuple

from openpecha.alignment.metadata import AlignmentMetaData
from openpecha.ids import get_uuid


class Alignment:
    def __init__(
        self,
        metadata: AlignmentMetaData,
        segment_pairs: Dict[str, Dict[str, str]] = None,
    ):
        self.id = metadata.id_
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
        """assign uuid for each alignment id"""
        transformed_segment_pairs = {}
        for (source_id, source_ann_id), (target_id, target_ann_id) in segment_pairs:
            transformed_segment_pairs[get_uuid()] = {
                source_id: source_ann_id,
                target_id: target_ann_id,
            }
        return cls(metadata=metadata, segment_pairs=transformed_segment_pairs)

    def save(self, path: str):
        pass
