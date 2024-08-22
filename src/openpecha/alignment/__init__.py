import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from openpecha.alignment.metadata import AlignmentMetaData
from openpecha.config import ALIGNMENT_PATH, _mkdir
from openpecha.github_utils import (
    clone_repo,
    create_github_repo,
    upload_folder_to_github,
)
from openpecha.ids import get_uuid
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerCollectionEnum, LayerEnum, LayerGroupEnum


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
            metadata=metadata, alignment_id=metadata["id_"]
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
    def from_id(cls, alignment_id: str, output_path: Path = ALIGNMENT_PATH):
        alignment_path = clone_repo(alignment_id, output_path)
        return Alignment.from_path(alignment_path)

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

    def load_pechas(self):
        pecha_ids = self.metadata.segments_metadata.keys()
        pechas: Dict[str, Pecha] = {
            pecha_id: Pecha.from_id(pecha_id) for pecha_id in pecha_ids
        }
        if self.pechas is None:
            self.pechas = pechas
        return self.pechas

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
            """get root segment annotation"""
            base_file = self.metadata.segments_metadata[pecha_id].base
            ann_type = self.metadata.segments_metadata[pecha_id].type
            pecha_ann_store = self.pechas[pecha_id].get_annotation_store(
                base_file, ann_type
            )

            """ get chapter annotation"""
            chapter_ann_type = LayerEnum.chapter
            chapter_file_path = next(
                Path(self.pechas[pecha_id].ann_path / f"{base_file}").glob(
                    f"{chapter_ann_type.value}*.json"
                ),
                None,
            )

            if chapter_file_path:
                pecha_ann_store.from_file(chapter_file_path.as_posix())

            """ get segment string and its chapter metadata"""
            ann = pecha_ann_store.annotation(ann_id)
            ann_text_selection = next(ann.textselections())
            ann_text_begin, ann_text_end = (
                ann_text_selection.begin(),
                ann_text_selection.end(),
            )

            data_set = pecha_ann_store.dataset(
                LayerCollectionEnum.root_commentory.value
            )
            key = data_set.key(LayerGroupEnum.structure_type.value)

            ann_data: Dict[str, Any] = {}
            ann_data["string"] = str(ann)
            for chapter_ann in key.data(value=LayerEnum.chapter.value).annotations():
                chapter_ann_text_begin = next(chapter_ann.textselections()).begin()
                chapter_ann_text_end = next(chapter_ann.textselections()).end()
                if (
                    ann_text_begin >= chapter_ann_text_begin
                    and ann_text_end <= chapter_ann_text_end
                ):
                    metadata: Dict[str, str] = {}
                    for ann_metadata in chapter_ann:
                        metadata[str(ann_metadata.key().id())] = str(
                            ann_metadata.value()
                        )

                    ann_data["metadata"] = metadata
                    break
            segment_pair[pecha_id] = ann_data
        return segment_pair

    def upload_update_with_github(self):
        """upload files if first time"""
        """ update files if already exist"""
        repo_created = create_github_repo(self.id_)
        if repo_created:
            upload_folder_to_github(self.id_, self.base_path)
