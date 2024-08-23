import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from stam import AnnotationStore, Offset, Selector

from openpecha.alignment import Alignment, AlignmentMetaData
from openpecha.alignment.metadata import AlignmentRelationEnum
from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha.layer import (
    LayerCollectionEnum,
    LayerEnum,
    LayerGroupEnum,
    get_layer_group,
)
from openpecha.pecha.metadata import PechaMetaData


class AnnotationMetadata:
    """
    Class to store metadata for annotations.
    """

    def __init__(
        self,
        dataset_id: str,
        base_text: str,
        annotation_category: LayerGroupEnum,
        annotation_type: LayerEnum,
    ):
        self.dataset_id = dataset_id
        self.base_text = base_text
        self.annotation_category = annotation_category
        self.annotation_type = annotation_type


class PlainTextLineAlignedParser:
    """
    Class to parse plain text lines and create aligned annotations.
    """

    def __init__(self, source_text: str, target_text: str, metadata: dict):
        self.source_text = source_text
        self.target_text = target_text
        self.metadata = metadata

    @classmethod
    def from_files(
        cls, source_path: Path, target_path: Path, metadata_path: Path
    ) -> "PlainTextLineAlignedParser":
        """
        Create a parser instance from file paths.
        """
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        with open(metadata_path) as f:
            metadata = json.load(f)
        return cls(source_text, target_text, metadata)

    def parse(self, output_path: Path) -> Optional[Alignment]:
        """
        Parse the source and target texts, create annotations, and save to files.
        """

        alignment_type = LayerCollectionEnum(self.metadata["metadata"]["type"])
        (source_ann_store, source_ann_store_name), (
            target_ann_store,
            target_ann_store_name,
        ) = self.parse_pechas(alignment_type.value, output_path)
        self.source_ann_store = source_ann_store
        self.target_ann_store = target_ann_store

        alignment = self.create_alignment(source_ann_store_name, target_ann_store_name)
        if alignment:
            alignment.write(output_path)
        return alignment

    def create_alignment(
        self, source_ann_store_name: str, target_ann_store_name: str
    ) -> Optional[Alignment]:
        if not self.source_ann_store or not self.target_ann_store:
            return None

        """ building alignment metadata """
        metadata: Dict = defaultdict(lambda: defaultdict(dict))

        metadata["metadata"] = self.metadata["metadata"]
        source_id = self.source_ann_store.id()
        resource = [
            resource
            for resource in self.source_ann_store.resources()
            if resource.id() != "metadata"
        ][0]

        metadata["segments_metadata"][source_id] = {
            "type": self.metadata["source"]["type"],
            "relation": AlignmentRelationEnum.source.value,
            "lang": self.metadata["source"]["language"],
            "base": resource.id(),
            "layer": source_ann_store_name,
        }

        target_id = self.target_ann_store.id()
        resource = [
            resource
            for resource in self.target_ann_store.resources()
            if resource.id() != "metadata"
        ][0]
        metadata["segments_metadata"][target_id] = {
            "type": self.metadata["target"]["type"],
            "relation": AlignmentRelationEnum.target.value,
            "lang": self.metadata["target"]["language"],
            "base": resource.id(),
            "layer": target_ann_store_name,
        }

        alignment_metadata = AlignmentMetaData.from_dict(metadata)
        segment_pairs = [
            ((source_id, source_ann.id()), (target_id, target_ann.id()))
            for source_ann, target_ann in zip(
                self.source_ann_store.annotations(), self.target_ann_store.annotations()
            )
        ]

        alignment = Alignment.from_segment_pairs(segment_pairs, alignment_metadata)
        return alignment

    def parse_pechas(self, dataset_id: str, output_path: Path):

        source_metadata = PechaMetaData(**self.metadata["source"])
        target_metadata = PechaMetaData(**self.metadata["target"])

        source_ann_metadata = AnnotationMetadata(
            dataset_id=dataset_id,
            base_text=self.source_text,
            annotation_category=get_layer_group(LayerEnum(source_metadata.type)),
            annotation_type=LayerEnum(source_metadata.type),
        )
        target_ann_metadata = AnnotationMetadata(
            dataset_id=dataset_id,
            base_text=self.target_text,
            annotation_category=get_layer_group(LayerEnum(target_metadata.type)),
            annotation_type=LayerEnum(target_metadata.type),
        )

        (source_ann_store, source_ann_store_name) = create_pecha_stam(
            source_ann_metadata, source_metadata, output_path
        )
        (target_ann_store, target_ann_store_name) = create_pecha_stam(
            target_ann_metadata, target_metadata, output_path
        )
        return (source_ann_store, source_ann_store_name), (
            target_ann_store,
            target_ann_store_name,
        )


def create_pecha_stam(
    ann_metadata: AnnotationMetadata, metadata: PechaMetaData, output_path: Path
) -> AnnotationStore:

    """create new annotation store for the given annotation layer"""
    ann_store_id = get_initial_pecha_id()
    pecha_path = _mkdir(output_path / ann_store_id)
    ann_store = AnnotationStore(id=ann_store_id)

    """ create base file for new annotation store"""
    base_dir = _mkdir(pecha_path / "base")
    base_file_name = get_uuid()[:4]
    base_file_path = base_dir / f"{base_file_name}.txt"
    base_file_path.write_text(ann_metadata.base_text, encoding="utf-8")
    ann_resource = ann_store.add_resource(
        id=base_file_name, filename=base_file_path.as_posix()
    )

    """ write metadata"""
    metadata_ann_store = AnnotationStore(id=ann_store_id)
    metadata_dataset = metadata_ann_store.add_dataset(
        id=LayerCollectionEnum.metadata.value
    )
    metadata_ann_resource = metadata_ann_store.add_resource(
        id=base_file_name, filename=base_file_path.as_posix()
    )

    data = []
    for key, value in metadata.model_dump().items():
        if isinstance(value, datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S.%f")
        if isinstance(value, List):
            for v in value:
                data.append(
                    {
                        "id": get_uuid(),
                        "set": metadata_dataset.id(),
                        "key": key,
                        "value": v,
                    }
                )
            continue
        if isinstance(value, dict):
            for k, v in value.items():
                data.append(
                    {
                        "id": get_uuid(),
                        "set": metadata_dataset.id(),
                        "key": k,
                        "value": v,
                    }
                )
            continue
        data.append(
            {
                "id": get_uuid(),
                "set": metadata_dataset.id(),
                "key": key,
                "value": value,
            }
        )

    metadata_ann_store.annotate(
        id=get_uuid(),
        target=Selector.resourceselector(resource=metadata_ann_resource),
        data=data,
    )

    save_stam(metadata_ann_store, output_path, pecha_path / "metadata.json")

    ann_dataset = ann_store.add_dataset(id=ann_metadata.dataset_id)

    """ create annotation for each line in new annotation store"""
    lines = split_text_into_lines(ann_metadata.base_text)
    unque_ann_data_id = get_uuid()
    char_count = 0
    for line in lines:
        target = Selector.textselector(
            ann_resource,
            Offset.simple(char_count, char_count + len(line)),
        )
        char_count += len(line)

        ann_store.annotate(
            id=get_uuid(),
            target=target,
            data=[
                {
                    "id": unque_ann_data_id,
                    "set": ann_dataset.id(),
                    "key": ann_metadata.annotation_category.value,
                    "value": ann_metadata.annotation_type.value,
                }
            ],
        )

    """save the new annotation store"""
    ann_output_dir = _mkdir(pecha_path / "layers" / base_file_name)
    ann_store_filename = f"{ann_metadata.annotation_type.value}-{get_uuid()[:3]}.json"
    ann_store_path = ann_output_dir / ann_store_filename
    ann_store_path = save_stam(ann_store, output_path, ann_store_path)

    return (ann_store, ann_store_path.name)


def split_text_into_lines(text: str) -> List[str]:
    """
    Split text into lines and ensure each line ends with a newline character.
    """
    lines = text.split("\n")
    return [line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)]


def save_stam(
    ann_store: AnnotationStore, base_path: Path, ann_store_path: Path
) -> Path:
    """
    Save the annotation store to a file.
    """
    ann_store_path.parent.mkdir(parents=True, exist_ok=True)

    ann_json_str = ann_store.to_json_string()
    ann_json_dict = convert_absolute_to_relative_path(ann_json_str, ann_store_path)
    with open(ann_store_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(ann_json_dict, indent=2, ensure_ascii=False))

    return ann_store_path


def convert_absolute_to_relative_path(json_string: str, ann_store_path: Path):
    """
    convert the absolute to relative path for base file in json string of annotation store
    """
    json_object = json.loads(json_string)
    for resource in json_object["resources"]:
        original_path = Path(resource["@include"])
        if ann_store_path.name == "metadata.json":
            resource["@include"] = f"base/{original_path.name}"
        else:
            resource["@include"] = f"../../base/{original_path.name}"
    return json_object
