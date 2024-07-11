import json
from pathlib import Path
from typing import List, Tuple

from stam import AnnotationStore, Offset, Selector, TextResource

from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum


class AnnotationMetadata:
    """
    Class to store metadata for annotations.
    """

    def __init__(
        self,
        dataset_id: str,
        resource: TextResource,
        annotation_category: LayerGroupEnum,
        annotation_type: LayerEnum,
    ):
        self.dataset_id = dataset_id
        self.resource = resource
        self.annotation_category = annotation_category
        self.annotation_type = annotation_type


class PlainTextLineAlignedParser:
    """
    Class to parse plain text lines and create aligned annotations.
    """

    def __init__(self, source_text: str, target_text: str):
        self.source_text = source_text
        self.target_text = target_text

    @classmethod
    def from_files(
        cls, source_path: Path, target_path: Path
    ) -> "PlainTextLineAlignedParser":
        """
        Create a parser instance from file paths.
        """
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        return cls(source_text, target_text)

    def parse(self, output_path: Path) -> Tuple[AnnotationStore, AnnotationStore]:
        """
        Parse the source and target texts, create annotations, and save to files.
        """
        source_lines = split_text_into_lines(self.source_text)
        target_lines = split_text_into_lines(self.target_text)

        dataset_id = f"root_commentary_{get_uuid()[:3]}"

        source_ann_store, source_base_resource = set_up_stam_ann_store(
            output_path, self.source_text, dataset_id
        )
        target_ann_store, target_base_resource = set_up_stam_ann_store(
            output_path, self.target_text, dataset_id
        )

        source_ann_metadata = AnnotationMetadata(
            dataset_id=dataset_id,
            resource=source_base_resource,
            annotation_category=LayerGroupEnum.structure_type,
            annotation_type=LayerEnum.root_segment,
        )
        target_ann_metadata = AnnotationMetadata(
            dataset_id=dataset_id,
            resource=target_base_resource,
            annotation_category=LayerGroupEnum.structure_type,
            annotation_type=LayerEnum.comment,
        )

        source_ann_store = annotate_in_stam_model(
            source_ann_store, source_lines, source_ann_metadata
        )
        target_ann_store = annotate_in_stam_model(
            target_ann_store, target_lines, target_ann_metadata
        )

        source_ann_file_name = (
            f"{source_ann_metadata.annotation_type.value}-{get_uuid()[:3]}.json"
        )
        target_ann_file_name = (
            f"{target_ann_metadata.annotation_type.value}-{get_uuid()[:3]}.json"
        )
        save_annotation_store(source_ann_store, output_path, source_ann_file_name)
        save_annotation_store(target_ann_store, output_path, target_ann_file_name)

        return source_ann_store, target_ann_store


def set_up_stam_ann_store(
    output_path: Path, base_text: str, dataset_id: str
) -> Tuple[AnnotationStore, TextResource]:
    """
    Set up the stam annotation store and add base text as a resource.
    """
    pecha_id = get_initial_pecha_id()
    pecha_path = _mkdir(output_path / pecha_id)
    ann_store = AnnotationStore(id=pecha_id)

    base_path = _mkdir(pecha_path / "base")
    base_file_name = get_uuid()
    base_file_path = base_path / f"{base_file_name}.txt"
    base_file_path.write_text(base_text, encoding="utf-8")

    resource = ann_store.add_resource(
        id=base_file_name, filename=base_file_path.as_posix()
    )
    ann_store.add_dataset(id=dataset_id)

    return ann_store, resource


def annotate_in_stam_model(
    ann_store: AnnotationStore, lines: List[str], ann_metadata: AnnotationMetadata
) -> AnnotationStore:
    """
    Create annotations for each line in the text.
    """
    char_count = 0
    for line in lines:
        target = Selector.textselector(
            ann_metadata.resource,
            Offset.simple(char_count, char_count + len(line)),
        )
        char_count += len(line)

        ann_store.annotate(
            id=get_uuid(),
            target=target,
            data=[
                {
                    "id": get_uuid(),
                    "set": ann_metadata.dataset_id,
                    "key": ann_metadata.annotation_category.value,
                    "value": ann_metadata.annotation_type.value,
                }
            ],
        )

    return ann_store


def split_text_into_lines(text: str) -> List[str]:
    """
    Split text into lines and ensure each line ends with a newline character.
    """
    lines = text.split("\n")
    return [line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)]


def save_annotation_store(
    ann_store: AnnotationStore, output_path: Path, filename: str
) -> Path:
    """
    Save the annotation store to a file.
    """
    output_file_path = output_path / ann_store.id() / "layers" / filename
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    ann_json_str = ann_store.to_json_string()
    ann_json_dict = convert_absolute_to_relative_path(ann_json_str, output_path)
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(ann_json_dict, indent=4, ensure_ascii=False))

    return output_file_path


def convert_absolute_to_relative_path(json_string: str, output_path: Path):
    """
    convert the absolute to relative path for base file in json string of annotation store
    """
    json_object = json.loads(json_string)
    for resource in json_object["resources"]:
        original_path = Path(resource["@include"])
        resource["@include"] = str(original_path.relative_to(output_path))
    return json_object
