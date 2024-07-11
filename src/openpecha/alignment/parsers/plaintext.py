from pathlib import Path
from typing import List, Tuple

from stam import AnnotationStore, Offset, Selector, TextResource

from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid


class AnnotationMetadata:
    def __init__(
        self,
        dataset_id: str,
        resource: TextResource,
        annotation_category: str,
        annotation_type: str,
    ):
        self.dataset_id = dataset_id
        self.resource = resource
        self.annotation_category = annotation_category
        self.annotation_type = annotation_type


class PlainTextLineAlignedParser:
    def __init__(self, source_text: str, target_text: str):
        """
        Initialize the parser with source and target texts.
        """
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
            annotation_category="structure type",
            annotation_type="root",
        )
        target_ann_metadata = AnnotationMetadata(
            dataset_id=dataset_id,
            resource=target_base_resource,
            annotation_category="structure type",
            annotation_type="comment",
        )
        source_ann_store = annotate_in_stam_model(
            source_ann_store, source_lines, source_ann_metadata
        )
        target_ann_store = annotate_in_stam_model(
            target_ann_store, target_lines, target_ann_metadata
        )

        save_annotation_store(source_ann_store, output_path, "source.json")
        save_annotation_store(target_ann_store, output_path, "target.json")

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
                    "key": ann_metadata.annotation_category,
                    "value": ann_metadata.annotation_type,
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
) -> None:
    """
    Save the annotation store to a file.
    """
    file_path = output_path / ann_store.id() / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    ann_store.to_file(file_path.as_posix())
