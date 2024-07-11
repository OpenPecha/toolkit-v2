from pathlib import Path
from typing import List

from stam import AnnotationStore, Offset, Selector, TextResource

from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid


class PlainTextLineAlignedParser:
    def __init__(self, source_text: str, target_text: str):
        self.source_text = source_text
        self.target_text = target_text

    @classmethod
    def from_files(cls, source_path: Path, target_path: Path):
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        return cls(source_text, target_text)

    def parse(self, output_path: Path):
        source_lines = split_text_into_lines(self.source_text)
        target_lines = split_text_into_lines(self.target_text)

        dataset_id = f"root_commentary_{get_uuid()[:3]}"

        source_ann_store, source_base_resource = set_up_stam_ann_store(
            output_path, self.source_text, dataset_id
        )
        target_ann_store, target_base_resource = set_up_stam_ann_store(
            output_path, self.target_text, dataset_id
        )

        source_ann_store = annotate_in_stam_model(
            source_ann_store, source_lines, dataset_id, source_base_resource
        )
        target_ann_store = annotate_in_stam_model(
            target_ann_store, target_lines, dataset_id, target_base_resource
        )

        source_ann_store.to_file(
            Path(output_path / f"{source_ann_store.id()}" / "source.json").as_posix()
        )
        target_ann_store.to_file(
            Path(output_path / f"{target_ann_store.id()}" / "target.json").as_posix()
        )

        return source_ann_store, target_ann_store


def set_up_stam_ann_store(output_path: Path, base_text: str, dataset_id: str):
    pecha_id = get_initial_pecha_id()
    pecha_path = _mkdir(output_path / pecha_id)
    ann_store = AnnotationStore(id=pecha_id)

    base_path = _mkdir(pecha_path / "base")
    base_file_name = get_uuid()
    Path(base_path / f"{base_file_name}.txt").write_text(base_text, encoding="utf-8")
    resource = ann_store.add_resource(
        id=base_file_name, filename=Path(base_path / f"{base_file_name}.txt").as_posix()
    )
    ann_store.add_dataset(id=dataset_id)
    return ann_store, resource


def annotate_in_stam_model(
    ann_store, lines: List[str], dataset_id: str, resource: TextResource
) -> AnnotationStore:
    """Create annotation for each line in the text"""
    unique_ann_data_id = get_uuid()
    char_count = 0
    for line in lines:
        target = Selector.textselector(
            resource,
            Offset.simple(char_count, char_count + len(line)),
        )
        char_count += len(line)
        data = [
            {
                "id": unique_ann_data_id,
                "set": dataset_id,
                "key": "structure type",
                "value": "root",
            }
        ]
        ann_store.annotate(id=get_uuid(), target=target, data=data)

    return ann_store


def split_text_into_lines(text: str) -> List[str]:
    """Split text into lines and add newline to each lines"""
    lines = text.split("\n")
    lines = [
        line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)
    ]
    return lines
