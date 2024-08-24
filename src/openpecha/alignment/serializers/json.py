import json
from pathlib import Path

from stam import AnnotationStore

from openpecha.alignment.alignment import Alignment
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum


class JSONSerializer:
    def __init__(self, alignment: Alignment):
        self.alignment = alignment

    def load_pechas(self, source_pecha: Pecha, target_pecha: Pecha):
        self.source_pecha = source_pecha
        self.target_pecha = target_pecha

        root_segment_file = next(
            self.source_pecha.ann_path.rglob(f"{LayerEnum.root_segment.value}*.json")
        )

        commentary_segment_file = next(
            self.target_pecha.ann_path.rglob(
                f"{LayerEnum.commentary_segment.value}*.json"
            )
        )

        source_ann_store = AnnotationStore(file=root_segment_file.as_posix())
        target_ann_store = AnnotationStore(file=commentary_segment_file.as_posix())

        return source_ann_store, target_ann_store

    @staticmethod
    def get_standard_json():
        return {
            "books": [
                {
                    "title": "title",
                    "language": "bo",
                    "author": "author name",
                    "versionSource": " ",
                    "content": [[]],
                    "direction": "ltr",
                }
            ]
        }

    def serialize(self, output_path: Path):
        root_segments = []
        commentary_segments = []

        for _, segment_pair in self.alignment.segment_pairs.items():
            if self.source_pecha.id_ in segment_pair:
                root_segments.append(segment_pair[self.source_pecha.id_])
            if self.target_pecha.id_ in segment_pair:
                if isinstance(segment_pair[self.target_pecha.id_], str):
                    commentary_segments.append(segment_pair[self.target_pecha.id_])
                if isinstance(segment_pair[self.target_pecha.id_], list):
                    commentary_segments.extend(segment_pair[self.target_pecha.id_])

        output_path.mkdir(parents=True, exist_ok=True)

        """ write the json files"""
        root_json = self.get_standard_json()
        root_json["books"][0]["content"] = root_segments
        (output_path / "root.json").write_text(
            json.dumps(root_json, ensure_ascii=False, indent=2)
        )

        commentary_json = self.get_standard_json()
        commentary_json["books"][0]["content"] = commentary_segments
        (output_path / "commentary.json").write_text(
            json.dumps(commentary_json, ensure_ascii=False, indent=2)
        )
