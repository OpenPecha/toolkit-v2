import json
from pathlib import Path
from typing import Dict

from stam import AnnotationStore, Offset, Selector

from openpecha.config import PECHAS_PATH
from openpecha.ids import get_uuid
from openpecha.pecha.annotation import Annotation


class Pecha:
    def __init__(
        self, pecha_id: str, segments: Dict[str, str], metadata: Dict[str, str]
    ) -> None:
        self.pecha_id = pecha_id
        self.segments = segments
        self.metadata = metadata

    @classmethod
    def from_path(cls, path: str):
        pass

    @classmethod
    def from_id(cls, pecha_id: str):
        pass

    def set_annotations(self):
        """set annotations for the segments"""
        char_count = 0
        for segment_id, segment in self.segments.items():
            annotation = Annotation(
                id_=segment_id,
                segment=segment,
                start=char_count,
                end=char_count + len(segment),
            )
            char_count += len(segment)
            yield annotation

    def create_pecha_folder(self, base_path: Path):
        pecha_dir = base_path.joinpath(self.pecha_id)
        opf_dir = pecha_dir.joinpath(f"{self.pecha_id}.opf")
        metadata_dir = opf_dir.joinpath("metadata.json")
        base_dir = opf_dir.joinpath("base")
        layers_dir = opf_dir.joinpath("layers")
        layer_id_dir = layers_dir.joinpath(self.pecha_id)

        pecha_dir.mkdir(exist_ok=True)
        opf_dir.mkdir(exist_ok=True)
        metadata_dir.write_text(
            json.dumps(self.metadata, indent=4, ensure_ascii=False), encoding="utf-8"
        )

        base_dir.mkdir(exist_ok=True)
        base_dir.joinpath(f"{self.pecha_id}.txt").write_text(self.base_text)
        layers_dir.mkdir(exist_ok=True)
        layer_id_dir.mkdir(exist_ok=True)

        self.annotation_fn = layer_id_dir
        self.base_fn = base_dir.joinpath(f"{self.pecha_id}.txt")

    def write_annotations(self, base_path: Path = PECHAS_PATH):
        self.base_text = "".join(self.segments.values())
        self.annotations = self.set_annotations()

        self.create_pecha_folder(base_path)
        """write annotations in stam data model"""
        self.annotation_store = AnnotationStore(id="PechaAnnotationStore")
        self.resource = self.annotation_store.add_resource(
            id=self.pecha_id, filename=self.base_fn.as_posix()
        )
        self.dataset = self.annotation_store.add_dataset(id="PechaDataSet")
        self.dataset.add_key(self.metadata["annotation_category"])

        unique_annotation_data_id = get_uuid()
        for annotation in self.annotations:
            target = Selector.textselector(
                self.resource,
                Offset.simple(annotation.start, annotation.end),
            )
            data = [
                {
                    "id": unique_annotation_data_id,
                    "key": self.metadata["annotation_category"],
                    "value": self.metadata["annotation_label"],
                    "set": self.dataset.id(),
                }
            ]
            self.annotation_store.annotate(
                id=annotation.id_,
                target=target,
                data=data,
            )
        """ save annotations in stam data model"""
        self.annotation_store.set_filename(
            self.annotation_fn.joinpath(
                f"{self.metadata['annotation_label']}.json"
            ).as_posix()
        )
        self.annotation_store.save()
