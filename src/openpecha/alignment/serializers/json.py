import json
from pathlib import Path
from typing import Dict

from stam import Annotation, AnnotationStore

from openpecha.alignment.alignment import Alignment
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum


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

        self.source_ann_store = AnnotationStore(file=root_segment_file.as_posix())
        self.target_ann_store = AnnotationStore(file=commentary_segment_file.as_posix())

        return self.source_ann_store, self.target_ann_store

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

    @staticmethod
    def is_meaning_segment(ann: Annotation):
        metadata: Dict[str, str] = {}
        for ann_data in ann:
            metadata[ann_data.key().id()] = str(ann_data.value())

        if LayerGroupEnum.structure_type.value not in metadata:
            raise ValueError(
                f"ann id {ann.id()} does not have {LayerGroupEnum.structure_type.value} value"
            )

        return (
            metadata[LayerGroupEnum.structure_type.value]
            == LayerEnum.meaning_segment.value
        )

    def serialize(self, output_path: Path):
        root_segments = []
        commentary_segments = []

        for _, segment_pair in self.alignment.segment_pairs.items():
            """get the root segment"""
            if self.source_pecha.id_ in segment_pair:
                root_ann = self.source_ann_store.annotation(
                    segment_pair[self.source_pecha.id_]
                )
                if self.is_meaning_segment(root_ann):
                    root_string_segment = str(root_ann)
                else:
                    root_string_segment = str(
                        root_ann.target().annotation(self.source_ann_store)
                    )

                root_segments.append(root_string_segment)
                del root_ann
            """ get the commentary segment"""
            if self.target_pecha.id_ in segment_pair:
                if isinstance(segment_pair[self.target_pecha.id_], str):
                    commentary_ann = self.target_ann_store.annotation(
                        segment_pair[self.target_pecha.id_]
                    )

                    if self.is_meaning_segment(commentary_ann):
                        commentary_segment_string = str(commentary_ann)
                    else:
                        commentary_segment_string = str(
                            commentary_ann.target().annotation(self.target_ann_store)
                        )

                    commentary_segments.append(commentary_segment_string)
                    del commentary_ann

                if isinstance(segment_pair[self.target_pecha.id_], list):
                    commentary_anns = [
                        self.target_ann_store.annotation(segment_id)
                        for segment_id in segment_pair[self.target_pecha.id_]
                    ]
                    if self.is_meaning_segment(commentary_anns[0]):
                        commentary_segment_strings = [
                            str(commentary_ann) for commentary_ann in commentary_anns
                        ]
                    else:
                        commentary_segment_strings = [
                            str(
                                commentary_ann.target().annotation(
                                    self.target_ann_store
                                )
                            )
                            for commentary_ann in commentary_anns
                        ]

                    commentary_segments.extend(commentary_segment_strings)
                    del commentary_anns

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
