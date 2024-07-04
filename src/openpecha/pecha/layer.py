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
    commentaries = "Commentaries"


def get_annotation_category():
    # TODO
    # Return annotation category based on the annotation label
    return "Structure Type"


class Layer:
    def __init__(self, annotation_label: LayerEnum, annotations: Dict[str, Annotation]):
        self.annotation_label = annotation_label
        self.annotations = annotations

    def covert_to_relative_path(self, json_string: str, export_path: Path):
        """convert the absolute path to relative path for base file path in json string"""
        json_object = json.loads(json_string)
        for resource in json_object["resources"]:
            original_path = Path(resource["@include"])
            resource["@include"] = str(original_path.relative_to(export_path))
        return json_object

    def write_layer(self, base_file_path: Path, export_path: Path):
        """write annotations in stam data model"""
        self.annotation_store = AnnotationStore(id=PECHA_ANNOTATION_STORE_ID)
        self.resource = self.annotation_store.add_resource(
            id=base_file_path.name, filename=base_file_path.as_posix()
        )
        self.dataset = self.annotation_store.add_dataset(id=PECHA_DATASET_ID)

        annotation_category = get_annotation_category()
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
        json_string = self.annotation_store.to_json_string()
        json_object = self.covert_to_relative_path(json_string, export_path)
        with open(
            export_path / f"{self.annotation_label.value}.json",
            "w",
        ) as f:
            f.write(json.dumps(json_object, indent=4, ensure_ascii=False))
