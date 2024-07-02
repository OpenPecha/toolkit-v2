import json
from pathlib import Path
from typing import Dict

from stam import AnnotationStore, Offset, Selector

from openpecha.config import PECHAS_PATH, _mkdir
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

    def create_pecha_folder(self, export_path: Path):
        self.export_path = export_path

        pecha_dir = _mkdir(export_path.joinpath(self.pecha_id))
        opf_dir = _mkdir(pecha_dir.joinpath(f"{self.pecha_id}.opf"))
        base_dir = _mkdir(opf_dir.joinpath("base"))
        layers_dir = _mkdir(opf_dir.joinpath("layers"))
        layer_id_dir = _mkdir(layers_dir.joinpath(self.pecha_id))

        """ write metadata and base file"""
        self.metadata_fn = opf_dir.joinpath("metadata.json")
        self.metadata_fn.write_text(
            json.dumps(self.metadata, indent=4, ensure_ascii=False), encoding="utf-8"
        )
        self.base_fn = Path(base_dir / f"{self.pecha_id}.txt")
        self.base_fn.write_text(self.base_text)

        self.annotation_fn = layer_id_dir

    def covert_to_relative_path(self, json_string: str):
        """convert the absolute path to relative path for base file path in json string"""
        json_object = json.loads(json_string)
        for resource in json_object["resources"]:
            original_path = Path(resource["@include"])
            resource["@include"] = str(original_path.relative_to(self.export_path))
        return json_object

    def write_annotations(self, export_path: Path = PECHAS_PATH):
        if not hasattr(self, "annotations"):
            self.annotations = self.set_annotations()

        self.base_text = "".join(self.segments.values())

        self.create_pecha_folder(export_path)
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
        json_string = self.annotation_store.to_json_string()
        json_object = self.covert_to_relative_path(json_string)
        with open(
            self.annotation_fn.joinpath(f"{self.metadata['annotation_label']}.json"),
            "w",
        ) as f:
            f.write(json.dumps(json_object, indent=4, ensure_ascii=False))
