import json
import re
from pathlib import Path
from typing import Dict, List

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

        """ get chapter titles"""
        for match in matches:
            chapter_number = match.group(1)
            title = match.group(2)
            start_index = match.start()
            end_index = match.end()
            chapter_details.append(
                {
                    "chapter number": chapter_number,
                    "title": title,
                    "title_start": start_index,
                    "title_end": end_index,
                }
            )

        """ get chapter details"""
        for idx, chapter_detail in enumerate(chapter_details):
            chapter_detail["chapter_start"] = chapter_detail["title_end"]
            if idx + 1 < len(chapter_details):
                chapter_detail["chapter_end"] = chapter_details[idx + 1]["title_start"]
            else:
                chapter_detail["chapter_end"] = len(self.plain_text)

        return chapter_details

    def remove_chapter_titles(self, chapter_details: List[Dict]):
        """find spacing after Chapter Number and Chapter Name"""
        pattern = r'ch\d+-"[\u0F00-\u0FFF]+"(\s*)'
        matches = re.findall(pattern, self.plain_text)
        spaces_after_title = [len(spaces) for spaces in matches]

        assert len(spaces_after_title) == len(chapter_details), ""
        """remove chapter number and chapter titles"""
        self.plain_text = re.sub('ch\\d+-"[\u0F00-\u0FFF]+"\\s*', "", self.plain_text)

        """ update chapter co ordinate"""
        updated_chapter_details = []
        total_titles_len = 0  # Chapter Length
        total_space_count = 0
        for chapter_detail, space_count in zip(chapter_details, spaces_after_title):
            total_titles_len += (
                chapter_detail["title_end"] - chapter_detail["title_start"]
            )

            total_space_count += space_count
            start = (
                chapter_detail["chapter_start"]
                - total_titles_len
                - total_space_count
                + 1
            )
            end = chapter_detail["chapter_end"] - total_titles_len - total_space_count
            end = end if end < len(self.plain_text) else len(self.plain_text) - 1
            updated_chapter_details.append(
                {
                    "chapter number": chapter_detail["chapter number"],
                    "title": chapter_detail["title"],
                    "start": start,
                    "end": end,
                }
            )
        return updated_chapter_details

    def parse(self, output_path: Path):
        pecha_id = get_initial_pecha_id()
        pecha_path = _mkdir(output_path / pecha_id)

        """ metadata """
        with open(pecha_path / "metadata.json", "w") as f:
            json.dump(self.meta_data, f, ensure_ascii=False, indent=2)

        """ cleaning up base file """
        """ remove chapter number and chapter details """
        chapter_details = self.extract_chapters()
        chapter_details = self.remove_chapter_titles(chapter_details)

        """ base file """
        base_dir = _mkdir(pecha_path / "base")
        base_file_name = get_base_id()
        base_file_path = base_dir / f"{base_file_name}.txt"
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
        for chapter_detail in chapter_details:
            start_index = chapter_detail["start"]
            end_index = chapter_detail["end"]

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
                    "value": int(chapter_detail["chapter number"]),
                }
            )

            data.append(
                {
                    "id": get_uuid(),
                    "set": ann_dataset.id(),
                    "key": "Chapter Name",
                    "value": chapter_detail["title"],
                }
            )

            ann_store.annotate(id=get_uuid(), target=target, data=data)

        ann_store_filename = f"{LayerEnum.chapter.value}-{get_uuid()[:3]}.json"

        save_stam(
            ann_store, output_path, layer_dir / base_file_name / ann_store_filename
        )

        return pecha_path
