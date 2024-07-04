import json
from enum import Enum
from pathlib import Path
from typing import Dict

from stam import AnnotationStore, Offset, Selector

from openpecha.config import PECHA_ANNOTATION_STORE_ID, PECHA_DATASET_ID
from openpecha.ids import get_uuid
from openpecha.pecha.annotation import Annotation


class LayerEnum(Enum):
    segment = "Segment"
    commentaries = "Comment"


class LayerGroupEnum(Enum):
    structure_type = "Structure Type"


def get_annotation_category(layer_label: LayerEnum) -> LayerGroupEnum:
    """return the annotation category for the layer label"""
    return LayerGroupEnum.structure_type


def convert_relative_to_absolute_path(json_data, absolute_base_path: Path):
    """call after loading the stam from json"""
    for resource in json_data["resources"]:
        original_path = Path(resource["@include"])
        resource["@include"] = str(absolute_base_path / original_path)
    return json_data


class Layer:
    def __init__(self, annotation_label: LayerEnum, annotations: Dict[str, Annotation]):
        self.annotation_label = annotation_label
        self.annotations = annotations

    @classmethod
    def from_path(cls, layer_file_path: Path):
        """get annotation label"""
        annotation_label = LayerEnum(layer_file_path.stem.split("-")[0])
        """ load annotations from json"""
        with open(layer_file_path) as f:
            json_data = json.load(f)
        absolute_base_path = layer_file_path.parents[4]
        json_data = convert_relative_to_absolute_path(json_data, absolute_base_path)
        annotation_store = AnnotationStore(string=json.dumps(json_data))

        layer_annotations: Dict[str, Annotation] = {}
        for annotation in annotation_store.annotations():
            annotation_id, segment = annotation.id(), str(annotation)
            start = annotation.offset().begin().value()
            end = annotation.offset().end().value()
            layer_annotations[annotation_id] = Annotation(
                segment=segment, start=start, end=end
            )

        return cls(annotation_label, layer_annotations)

    def set_annotation(self, annotation: Annotation, annotation_id=None):
        if not annotation_id:
            annotation_id = get_uuid()
        self.annotations[annotation_id] = annotation

    def convert_absolute_to_relative_path(self, absolute_base_path: Path):
        """call before saving the stam in json"""
        json_string = self.annotation_store.to_json()
        json_object = json.loads(json_string)
        for resource in json_object["resources"]:
            original_path = Path(resource["@include"])
            resource["@include"] = str(original_path.relative_to(absolute_base_path))
        return json_object

    def write(self, base_file_path: Path, export_path: Path):
        self.base_file_path = base_file_path
        """write annotations in stam data model"""
        self.annotation_store = AnnotationStore(id=PECHA_ANNOTATION_STORE_ID)
        self.resource = self.annotation_store.add_resource(
            id=base_file_path.name, filename=base_file_path.as_posix()
        )
        self.dataset = self.annotation_store.add_dataset(id=PECHA_DATASET_ID)
        annotation_category = get_annotation_category(self.annotation_label).value
        self.dataset.add_key(annotation_category)
        unique_annotation_data_id = get_uuid()
        base_text = self.base_file_path.read_text(encoding="utf-8")
        for annotation_id, annotation in self.annotations.items():
            if (
                annotation.segment
                != base_text[annotation.start : annotation.end]  # noqa
            ):
                raise ValueError(
                    f"Annotation segment does not match the base text at {annotation_id}"
                )
            target = Selector.textselector(
                self.resource,
                Offset.simple(annotation.start, annotation.end),
            )
            data = [
                {
                    "id": unique_annotation_data_id,
                    "key": annotation_category,
                    "value": self.annotation_label.value,
                    "set": self.dataset.id(),
                }
            ]
            self.annotation_store.annotate(
                id=annotation_id,
                target=target,
                data=data,
            )
        """ save annotations in json"""
        pecha_json = self.convert_absolute_to_relative_path(export_path)
        """ add four uuid digits to the layer file name for uniqueness"""
        layer_dir = base_file_path.parent.parent / "layers" / base_file_path.stem
        layer_file_path = (
            layer_dir / f"{self.annotation_label.value}-{get_uuid()[:4]}.json"
        )
        with open(
            layer_file_path,
            "w",
        ) as f:
            f.write(json.dumps(pecha_json, indent=4, ensure_ascii=False))
