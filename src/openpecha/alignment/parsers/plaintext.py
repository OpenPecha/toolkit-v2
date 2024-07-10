from pathlib import Path
from typing import List

from stam import AnnotationStore, Offset, Selector

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

    def parse(
        self,
    ):
        source_lines = split_text_into_lines(self.source_text)
        target_lines = split_text_into_lines(self.target_text)

        dataset_id = f"root_commentary_{get_uuid()[:3]}"

        source_ann_store = create_stam_segment_annotation(source_lines, dataset_id)
        target_ann_store = create_stam_segment_annotation(target_lines, dataset_id)

        source_ann_store.save("source_ann.json")
        target_ann_store.save("target_ann.json")


def create_stam_segment_annotation(
    lines: List[str], dataset_id: str
) -> AnnotationStore:
    ann_store = AnnotationStore(id=get_initial_pecha_id())
    base_file_name = get_uuid()
    resource = ann_store.add_resource(
        id=base_file_name, filename=f"{base_file_name}.txt"
    )
    ann_dataset = ann_store.add_dataset(id=dataset_id)

    """ Create annotation for each line in the text"""
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
                "set": ann_dataset.id,
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
