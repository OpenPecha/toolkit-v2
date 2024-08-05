import json
import re
from pathlib import Path

from stam import AnnotationStore, Offset, Selector

from openpecha.alignment.parsers.plaintext import save_stam
from openpecha.config import _mkdir
from openpecha.ids import get_base_id, get_initial_pecha_id, get_uuid
from openpecha.pecha.layer import LayerCollectionEnum, LayerEnum, LayerGroupEnum


class PlainTextChapterAnnotationParser:
    def __init__(self, plain_text: str, meta_data: dict):
        self.plain_text = plain_text
        self.meta_data = meta_data

    @classmethod
    def from_file(cls, file_path: Path, meta_data_path: Path):
        plaintext = file_path.read_text(encoding="utf-8")
        with open(meta_data_path) as f:
            meta_data = json.load(f)
        return cls(plaintext, meta_data)

    def extract_chapters(self):
        chapter_details = []
        pattern = re.compile(r"ch(\d+)-\"([\u0F00-\u0FFF]+)\"")
        matches = pattern.finditer(self.plain_text)

        for match in matches:
            chapter = match.group(1)
            tibetan_text = match.group(2)
            start_index = match.start()
            end_index = match.end()
            chapter_details.append(
                {
                    "chapter": chapter,
                    "tibetan_text": tibetan_text,
                    "start_index": start_index,
                    "end_index": end_index,
                }
            )
        return chapter_details

    def parse(self, output_path: Path):
        pecha_id = get_initial_pecha_id()
        pecha_path = _mkdir(output_path / pecha_id)

        """ metadata """
        with open(pecha_path / "metadata.json", "w") as f:
            json.dump(self.meta_data, f, ensure_ascii=False, indent=2)

        """ base file """
        base_dir = _mkdir(pecha_path / "base")
        base_file_path = base_dir / f"{get_base_id()}.txt"
        base_file_path.write_text(self.plain_text, encoding="utf-8")

        """ chapter annotations """
        layer_dir = _mkdir(pecha_path / "layers")
        ann_store = AnnotationStore(id=pecha_id)
        ann_resource = ann_store.add_resource(
            id=base_file_path.stem, filename=base_file_path.as_posix()
        )
        ann_dataset = ann_store.add_dataset(
            id=LayerCollectionEnum.root_commentory.value
        )

        unique_ann_data_id = get_uuid()
        chapter_details = self.extract_chapters()
        for idx, chapter_detail in enumerate(chapter_details):
            start_index = chapter_detail["start_index"]
            if idx == len(chapter_details) - 1:
                end_index = len(self.plain_text)
            else:
                end_index = chapter_details[idx + 1]["start_index"]

            target = Selector.textselector(
                ann_resource,
                Offset.simple(start_index, end_index),
            )
            data = [
                {
                    "id": unique_ann_data_id,
                    "set": ann_dataset.id(),
                    "key": LayerGroupEnum.structure_type.value,
                    "value": LayerEnum.chapter.value,
                }
            ]

            data.append(
                {
                    "id": get_uuid(),
                    "set": ann_dataset.id(),
                    "key": "Chapter Number",
                    "value": int(chapter_detail["chapter"]),
                }
            )

            data.append(
                {
                    "id": get_uuid(),
                    "set": ann_dataset.id(),
                    "key": "Chapter Name",
                    "value": chapter_detail["tibetan_text"],
                }
            )

            ann_store.annotate(id=get_uuid(), target=target, data=data)

        ann_store_filename = f"{LayerEnum.chapter.value}-{get_uuid()[:3]}.json"

        save_stam(ann_store, output_path, layer_dir / ann_store_filename)

        return pecha_path
