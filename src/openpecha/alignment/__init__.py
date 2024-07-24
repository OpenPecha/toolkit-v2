import json
from pathlib import Path
from typing import Dict, List, Tuple

from openpecha.alignment.metadata import AlignmentMetaData
from openpecha.config import _mkdir
from openpecha.ids import get_uuid


class Alignment:
    def __init__(
        self,
        metadata: AlignmentMetaData,
        segment_pairs: Dict[str, Dict[str, str]] = None,
    ):
        self.id_ = metadata.id_
        self.metadata = metadata
        self.segment_pairs = segment_pairs

    @classmethod
    def from_path(cls, path: Path):
        metadata_path = path / "metadata.json"
        with open(metadata_path, encoding="utf-8") as f:
            metadata = json.load(f)
        metadata = AlignmentMetaData.from_dict(
            metadata=metadata["segments_metadata"], alignment_id=metadata["id_"]
        )

        anns_path = path / "alignment.json"
        with open(anns_path, encoding="utf-8") as fp:
            segment_pairs = json.load(fp)

        return cls(metadata=metadata, segment_pairs=segment_pairs)

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

    def save(self, output_path: Path):
        alignment_id = self.id_
        alignment_path = _mkdir(output_path / alignment_id)

        """ write metadata"""
        metadata_path = alignment_path / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata.to_dict(), f, indent=2)

        """ write alingment annotations"""
        ann_path = alignment_path / "alignment.json"
        with open(ann_path, "w", encoding="utf-8") as fp:
            json.dump(self.segment_pairs, fp, indent=2)
