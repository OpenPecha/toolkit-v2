import json
from pathlib import Path
from typing import List, Tuple

from stam import AnnotationStore, Offset, Selector

from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum
from openpecha.pecha.metadata import MetaData


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

    def parse(self, output_path: Path) -> Tuple[AnnotationStore, AnnotationStore]:
        """
        Parse the source and target texts, create annotations, and save to files.
        """

        dataset_id = f"root_commentary_{get_uuid()[:3]}"

        source_ann_metadata = AnnotationMetadata(
            dataset_id=dataset_id,
            base_text=self.source_text,
            annotation_category=LayerGroupEnum.structure_type,
            annotation_type=LayerEnum.root_segment,
        )
        target_ann_metadata = AnnotationMetadata(
            dataset_id=dataset_id,
            base_text=self.target_text,
            annotation_category=LayerGroupEnum.structure_type,
            annotation_type=LayerEnum.comment,
        )

        source_metadata = MetaData(**self.metadata["source"])
        target_metadata = MetaData(**self.metadata["target"])

        source_ann_store = annotate_in_stam_model(
            source_ann_metadata, source_metadata, output_path
        )
        target_ann_store = annotate_in_stam_model(
            target_ann_metadata, target_metadata, output_path
        )

        return source_ann_store, target_ann_store


def annotate_in_stam_model(
    ann_metadata: AnnotationMetadata, metadata: MetaData, output_path: Path
) -> AnnotationStore:

    """create new annotation store for the given annotation layer"""
    ann_store_id = get_initial_pecha_id()
    pecha_path = _mkdir(output_path / ann_store_id)
    ann_store = AnnotationStore(id=ann_store_id)

    """ write metadata"""
    metadata_path = Path(pecha_path / "metadata.txt")
    metadata_path.write_text(metadata.to_formatted_text(), encoding="utf-8")

    """ create base file for new annotation store"""
    base_dir = _mkdir(pecha_path / "base")
    base_file_name = get_uuid()[:3]
    base_file_path = base_dir / f"{base_file_name}.txt"
    base_file_path.write_text(ann_metadata.base_text, encoding="utf-8")
    ann_resource = ann_store.add_resource(
        id=base_file_name, filename=base_file_path.as_posix()
    )

    ann_dataset = ann_store.add_dataset(id=ann_metadata.dataset_id)
    """ point to metadata """
    metadata_resource = ann_store.add_resource(
        id="metadata", filename=metadata_path.as_posix()
    )
    data = [
        {
            "id": get_uuid(),
            "set": ann_dataset.id(),
            "key": LayerGroupEnum.resource_type.value,
            "value": LayerEnum.metadata.value,
        }
    ]
    ann_store.annotate(
        id="metadata",
        target=Selector.resourceselector(resource=metadata_resource),
        data=data,
    )

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
    ann_output_dir = _mkdir(pecha_path / "layers")
    ann_store_filename = f"{ann_metadata.annotation_type.value}-{get_uuid()[:3]}.json"
    ann_store_path = ann_output_dir / ann_store_filename
    ann_store_path = save_annotation_store(ann_store, output_path, ann_store_path)

    return ann_store


def split_text_into_lines(text: str) -> List[str]:
    """
    Split text into lines and ensure each line ends with a newline character.
    """
    lines = text.split("\n")
    return [line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)]


def save_annotation_store(
    ann_store: AnnotationStore, base_path: Path, ann_store_path: Path
) -> Path:
    """
    Save the annotation store to a file.
    """
    ann_store_path.parent.mkdir(parents=True, exist_ok=True)

    ann_json_str = ann_store.to_json_string()
    ann_json_dict = convert_absolute_to_relative_path(ann_json_str, base_path)
    with open(ann_store_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(ann_json_dict, indent=2, ensure_ascii=False))

    return ann_store_path


def convert_absolute_to_relative_path(json_string: str, output_path: Path):
    """
    convert the absolute to relative path for base file in json string of annotation store
    """
    json_object = json.loads(json_string)
    for resource in json_object["resources"]:
        original_path = Path(resource["@include"])
        resource["@include"] = f"../base/{original_path.name}"
    return json_object
