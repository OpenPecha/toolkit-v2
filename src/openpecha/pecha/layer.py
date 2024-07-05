import json
from collections import defaultdict
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


class Layer:
    def __init__(
        self,
        annotation_type: LayerEnum,
        annotations: Dict[str, Annotation] = defaultdict(),
    ):
        self.annotation_type = annotation_type
        self.annotations = annotations

    def set_annotation(self, annotation: Annotation, annotation_id=None):
        if not annotation_id:
            annotation_id = get_uuid()
        self.annotations[annotation_id] = annotation

    def covert_to_relative_path(self, json_string: str, export_path: Path):
        """convert the absolute path to relative path for base file path in json string"""
        json_object = json.loads(json_string)
        for resource in json_object["resources"]:
            original_path = Path(resource["@include"])
            resource["@include"] = str(original_path.relative_to(export_path))
        return json_object

    def write(self, base_file_path: Path, export_path: Path):
        self.base_file_path = base_file_path
        """write annotations in stam data model"""
        self.annotation_store = AnnotationStore(id=PECHA_ANNOTATION_STORE_ID)
        self.resource = self.annotation_store.add_resource(
            id=base_file_path.name, filename=base_file_path.as_posix()
        )
        self.dataset = self.annotation_store.add_dataset(id=PECHA_DATASET_ID)
        annotation_category = get_annotation_category(self.annotation_type).value
        self.dataset.add_key(annotation_category)
        unique_annotation_data_id = get_uuid()
        for annotation_id, annotation in self.annotations.items():
            target = Selector.textselector(
                self.resource,
                Offset.simple(annotation.start, annotation.end),
            )
            data = [
                {
                    "id": unique_annotation_data_id,
                    "key": annotation_category,
                    "value": self.annotation_type.value,
                    "set": self.dataset.id(),
                }
            ]
            self.annotation_store.annotate(
                id=annotation_id,
                target=target,
                data=data,
            )
        """ save annotations in json"""
        json_string = self.annotation_store.to_json_string()
        json_object = self.covert_to_relative_path(json_string, export_path)
        """ add four uuid digits to the layer file name for uniqueness"""
        layer_dir = base_file_path.parent.parent / "layers" / base_file_path.stem
        layer_file_path = (
            layer_dir / f"{self.annotation_type.value}-{get_uuid()[:4]}.json"
        )
        with open(
            layer_file_path,
            "w",
        ) as f:
            f.write(json.dumps(json_object, indent=4, ensure_ascii=False))
