import json
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field
from stam import Annotation as StamAnnotation
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

    @classmethod
    def from_path(cls, layer_file_path: Path):
        """get annotation label"""
        annotation_label = LayerEnum(layer_file_path.stem.split("-")[0])
        layer_id = layer_file_path.stem.split("-")[1]
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
                id_=annotation_id, segment=segment, start=start, end=end
            )

        return Layer(
            id_=layer_id,
            annotation_type=annotation_label,
            annotations=layer_annotations,
            annotation_store=annotation_store,
        )

    def get_annotations(self):
        if not self.annotation_store:
            return None
        for ann in self.annotation_store:
            yield self.parse_annotation(ann)

    def get_annotation(self, ann_id: str):
        if not self.annotation_store:
            return None
        ann = self.annotation_store.annotation(id=ann_id)
        return self.parse_annotation(ann)

    def parse_annotation(self, ann: StamAnnotation):
        ann_id = ann.id()
        ann_segment = str(ann)
        start = ann.offset().begin().value()
        end = ann.offset().end().value()

        parsed_ann = {"id": ann_id, "segment": ann_segment, "start": start, "end": end}

        for ann_data in ann:
            key, value = ann_data.key().id(), str(ann_data.value())
            if key in LayerGroupEnum._value2member_map_:
                parsed_ann["annotation_category"] = key
                parsed_ann["annotation_type"] = value
            else:
                parsed_ann["payloads"] = defaultdict(str)
                parsed_ann["payloads"][key] = value

        return parsed_ann

    def set_annotation(self, annotation: Annotation):
        self.annotations[annotation.id_] = annotation

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

        unique_ann_data_id = get_uuid()
        ann_data_ids: Dict[Tuple[str, str], str] = {}

        for annotation_id, annotation in self.annotations.items():
            target = Selector.textselector(
                resource,
                Offset.simple(annotation.start, annotation.end),
            )

            data = [
                {
                    "id": unique_ann_data_id,
                    "key": annotation_category,
                    "value": self.annotation_type.value,
                    "set": self.dataset.id(),
                }
            ]
            """
                add metadata to the annotation if exists
                if the metadata is already added, get the id from the dictionary,
                else create a new id and add to the dictionary
            """
            if annotation.metadata:
                for key, value in annotation.metadata.items():
                    if (key, value) in ann_data_ids:
                        ann_data_id = ann_data_ids[(key, value)]
                    else:
                        ann_data_id = get_uuid()
                        ann_data_ids[(key, value)] = ann_data_id
                    data.append(
                        {
                            "id": ann_data_id,
                            "key": key,
                            "value": value,
                            "set": self.dataset.id(),
                        }
                    )

            self.annotation_store.annotate(
                id=annotation_id,
                target=target,
                data=data,
            )
        """ save annotations in json"""
        json_string = self.annotation_store.to_json_string()
        json_object = convert_to_relative_path(json_string, output_path)
        """ add four uuid digits to the layer file name for uniqueness"""
        layer_dir = base_file_path.parent.parent / "layers" / base_file_path.stem
        layer_file_path = layer_dir / f"{self.annotation_type.value}-{self.id_}.json"
        with open(
            layer_file_path,
            "w",
        ) as f:
            f.write(json.dumps(json_object, indent=4, ensure_ascii=False))


def convert_relative_to_absolute_path(json_data, absolute_base_path: Path):
    """call after loading the stam from json"""
    for resource in json_data["resources"]:
        original_path = Path(resource["@include"])
        resource["@include"] = str(absolute_base_path / original_path)
    return json_data


def convert_to_relative_path(json_string: str, output_path: Path):
    """convert the absolute path to relative path for base file path in json string"""
    json_object = json.loads(json_string)
    for resource in json_object["resources"]:
        original_path = Path(resource["@include"])
        resource["@include"] = str(original_path.relative_to(output_path))
    return json_object
