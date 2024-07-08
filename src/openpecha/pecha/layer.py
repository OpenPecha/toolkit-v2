import json
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field
from stam import AnnotationDataSet, AnnotationStore, Offset, Selector

from openpecha.config import PECHA_ANNOTATION_STORE_ID, PECHA_DATASET_ID
from openpecha.ids import get_fourchar_uuid, get_uuid
from openpecha.pecha.annotation import Annotation


class LayerEnum(Enum):
    segment = "Segment"
    commentaries = "Comment"


class LayerGroupEnum(Enum):
    structure_type = "Structure Type"


def get_annotation_category(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category for the layer label"""
    if layer_type == LayerEnum.segment:
        return LayerGroupEnum.structure_type
    return LayerGroupEnum.structure_type


class Layer(BaseModel):
    id_: str = Field(default_factory=get_fourchar_uuid)
    annotation_type: LayerEnum
    annotations: Dict[str, Annotation] = defaultdict()

    annotation_store: Optional[AnnotationStore] = None
    dataset: Optional[AnnotationDataSet] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def set_annotation(self, annotation: Annotation):
        self.annotations[annotation.id_] = annotation

    def covert_to_relative_path(self, json_string: str, output_path: Path):
        """convert the absolute path to relative path for base file path in json string"""
        json_object = json.loads(json_string)
        for resource in json_object["resources"]:
            original_path = Path(resource["@include"])
            resource["@include"] = str(original_path.relative_to(output_path))
        return json_object

    def write(self, base_file_path: Path, output_path: Path):
        base_file_path = base_file_path
        """write annotations in stam data model"""
        self.annotation_store = AnnotationStore(id=PECHA_ANNOTATION_STORE_ID)
        resource = self.annotation_store.add_resource(
            id=base_file_path.name, filename=base_file_path.as_posix()
        )
        self.dataset = self.annotation_store.add_dataset(id=PECHA_DATASET_ID)
        annotation_category = get_annotation_category(self.annotation_type).value
        self.dataset.add_key(annotation_category)
        unique_annotation_data_id = get_uuid()
        for annotation_id, annotation in self.annotations.items():
            target = Selector.textselector(
                resource,
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
        json_object = self.covert_to_relative_path(json_string, output_path)
        """ add four uuid digits to the layer file name for uniqueness"""
        layer_dir = base_file_path.parent.parent / "layers" / base_file_path.stem
        layer_file_path = layer_dir / f"{self.annotation_type.value}-{self.id_}.json"
        with open(
            layer_file_path,
            "w",
        ) as f:
            f.write(json.dumps(json_object, indent=4, ensure_ascii=False))
