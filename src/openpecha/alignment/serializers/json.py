import json
from pathlib import Path
from typing import Dict, List

from stam import Annotation, AnnotationStore

from openpecha.alignment.alignment import Alignment
from openpecha.config import LINE_BREAKERS
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerCollectionEnum, LayerEnum, LayerGroupEnum


class JSONSerializer:
    def __init__(self, alignment: Alignment):
        self.alignment = alignment

    def load_pechas(self, source_pecha: Pecha, target_pecha: Pecha):
        self.source_pecha = source_pecha
        self.target_pecha = target_pecha

        source_pecha_ann_file = (
            self.source_pecha.ann_path
            / self.alignment.metadata["source"]["base"]
            / self.alignment.metadata["source"]["layer"]
        )
        target_pecha_ann_file = (
            self.target_pecha.ann_path
            / self.alignment.metadata["target"]["base"]
            / self.alignment.metadata["target"]["layer"]
        )

        self.source_ann_store = AnnotationStore(file=source_pecha_ann_file.as_posix())
        self.target_ann_store = AnnotationStore(file=target_pecha_ann_file.as_posix())

        return self.source_ann_store, self.target_ann_store

    @staticmethod
    def get_standard_json(metadata: Dict[str, str]):
        return {
            "books": [
                {
                    "title": metadata["title"],
                    "language": metadata["language"],
                    "author": metadata["author"],
                    "versionSource": metadata["versionSource"],
                    "content": [[]],
                    "direction": metadata["direction"],
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

    @staticmethod
    def replace_newline_and_line_breakers(segments: List[str]):
        for i, segment in enumerate(segments):
            segment = segment.replace("\n", "<br>")
            for line_breaker in LINE_BREAKERS:
                segment = segment.replace(line_breaker, f"{line_breaker}<br>")
            segments[i] = segment
        return segments

    def serialize(self, output_path: Path):
        """define the neccessary annotation dataset, key, value"""
        ann_dataset = LayerCollectionEnum.root_commentory.value
        ann_key = LayerGroupEnum.structure_type.value
        ann_value = LayerEnum.meaning_segment.value

        source_base = self.alignment.metadata["source"]["base"]
        source_ann_type = LayerEnum(self.alignment.metadata["source"]["type"])
        ann_store, _ = self.source_pecha.get_annotation_store(
            source_base, source_ann_type
        )

        source_segments = []
        for ann in ann_store.data(
            set=ann_dataset, key=ann_key, value=ann_value
        ).annotations():
            is_not_meaning = next(ann.annotations(), None)
            if is_not_meaning:
                source_segments.append(f"<1>{str(ann)}")
            else:
                source_segments.append(str(ann))

        del ann_store

        target_base = self.alignment.metadata["target"]["base"]
        target_ann_type = LayerEnum(self.alignment.metadata["target"]["type"])
        ann_store, _ = self.target_pecha.get_annotation_store(
            target_base, target_ann_type
        )

        target_segments = []
        for ann in ann_store.data(
            set=ann_dataset, key=ann_key, value=ann_value
        ).annotations():
            is_not_meaning = next(ann.annotations(), None)
            if is_not_meaning:
                target_segments.append(f"<1>{str(ann)}")
            else:
                target_segments.append(str(ann))

        del ann_store

        output_path.mkdir(parents=True, exist_ok=True)
        source_segments = self.replace_newline_and_line_breakers(source_segments)
        target_segments = self.replace_newline_and_line_breakers(target_segments)

        """ write the json files"""
        root_json = self.get_standard_json(self.alignment.metadata["source"])
        root_json["books"][0]["content"][0] = source_segments
        (output_path / "root.json").write_text(
            json.dumps(root_json, ensure_ascii=False, indent=2)
        )

        commentary_json = self.get_standard_json(self.alignment.metadata["target"])

        commentary_json["books"][0]["content"][0] = target_segments
        commentary_json["books"][0]["base_text_titles"] = self.alignment.metadata[
            "source"
        ]["title"]
        (output_path / "commentary.json").write_text(
            json.dumps(commentary_json, ensure_ascii=False, indent=2)
        )
