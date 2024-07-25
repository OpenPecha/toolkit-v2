import json
from pathlib import Path
from typing import Dict, List, Tuple

from openpecha.alignment.metadata import AlignmentMetaData
from openpecha.config import ALIGNMENT_PATH, _mkdir
from openpecha.github_utils import create_github_repo, upload_folder_to_github
from openpecha.ids import get_uuid
from openpecha.pecha import Pecha


class Alignment:
    def __init__(
        self,
        metadata: AlignmentMetaData,
        base_path: Path = None,
        segment_pairs: Dict[str, Dict[str, str]] = None,
        pechas: Dict[str, Pecha] = None,
    ):
        self.id_ = metadata.id_
        self.base_path = (
            _mkdir(ALIGNMENT_PATH / self.id_) if not base_path else base_path
        )
        self.metadata = metadata
        self.segment_pairs = segment_pairs
        self.pechas = pechas

    @classmethod
    def from_path(cls, path: Path, pechas: Dict[str, Pecha] = None):
        metadata_path = path / "metadata.json"
        with open(metadata_path, encoding="utf-8") as f:
            metadata = json.load(f)
        metadata = AlignmentMetaData.from_dict(
            metadata=metadata["segments_metadata"], alignment_id=metadata["id_"]
        )

        anns_path = path / "alignment.json"
        with open(anns_path, encoding="utf-8") as fp:
            segment_pairs = json.load(fp)

        return cls(
            base_path=path,
            metadata=metadata,
            segment_pairs=segment_pairs,
            pechas=pechas,
        )

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

    def write(self, output_path: Path):
        """ """
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

    def get_segment_pairs(self):
        if not self.segment_pairs:
            return None

        for id_ in self.segment_pairs:
            yield {id_: self.get_segment_pair(id_)}

    def get_segment_pair(self, id_: str):
        if not self.segment_pairs or not self.pechas:
            return None

        segment_pair = {}
        for pecha_id, ann_id in self.segment_pairs[id_].items():
            """get annotation store"""
            ann_type = self.metadata.segments_metadata[pecha_id].type
            pecha_ann_store = self.pechas[pecha_id].get_annotation_store(ann_type)
            ann = pecha_ann_store.annotation(ann_id)
            segment_pair[pecha_id] = str(ann)
        return segment_pair

    def upload_update_with_github(self):
        """upload files if first time"""
        """ update files if already exist"""
        repo_created = create_github_repo(self.id_)
        if repo_created:
            upload_folder_to_github(self.id_, self.base_path)
