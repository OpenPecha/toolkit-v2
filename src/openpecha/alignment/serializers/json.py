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
            self.source_pecha.layer_path
            / self.alignment.metadata["source"]["base"]
            / self.alignment.metadata["source"]["layer"]
        )
        target_pecha_ann_file = (
            self.target_pecha.layer_path
            / self.alignment.metadata["target"]["base"]
            / self.alignment.metadata["target"]["layer"]
        )

        self.source_ann_store = AnnotationStore(file=source_pecha_ann_file.as_posix())
        self.target_ann_store = AnnotationStore(file=target_pecha_ann_file.as_posix())

        return self.source_ann_store, self.target_ann_store

    @staticmethod
    def get_standard_json(metadata: Dict[str, str]):
        neccessary_metadata = {
            k: v for k, v in metadata.items() if k not in ["pecha_id", "base", "layer"]
        }
        neccessary_metadata["content"] = [[]]  # type: ignore
        return {"books": [neccessary_metadata]}

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
        source_ann_type = LayerEnum(
            self.alignment.metadata["source"]["layer"].split("-")[0]
        )
        ann_store, _ = self.source_pecha.get_layer(source_base, source_ann_type)

        source_segments = []
        root_segment_count = 1
        root_segment_mapping: Dict[
            str, int
        ] = {}  # mapping of root ann id and root segment count
        for ann in ann_store.data(
            set=ann_dataset, key=ann_key, value=ann_value
        ).annotations():
            root_ann = next(ann.annotations(), None)
            if root_ann:
                source_segments.append(f"<1><{root_segment_count}>{str(ann)}")
                root_segment_mapping[root_ann.id()] = root_segment_count
                root_segment_count += 1

            else:
                source_segments.append(str(ann))

        del ann_store

        target_base = self.alignment.metadata["target"]["base"]
        target_ann_type = LayerEnum(
            self.alignment.metadata["target"]["layer"].split("-")[0]
        )
        ann_store, _ = self.target_pecha.get_layer(target_base, target_ann_type)

        target_segments = []
        for ann in ann_store.data(
            set=ann_dataset, key=ann_key, value=ann_value
        ).annotations():
            commentary_ann = next(ann.annotations(), None)
            if commentary_ann:
                paired_root_ann_id = None
                for _, segment_pair in self.alignment.segment_pairs.items():
                    if self.target_pecha.id_ not in segment_pair:
                        continue
                    if isinstance(segment_pair[self.target_pecha.id_], list):
                        if commentary_ann.id() in segment_pair[self.target_pecha.id_]:
                            paired_root_ann_id = segment_pair[self.source_pecha.id_]
                            paired_root_segment_count = root_segment_mapping.get(
                                paired_root_ann_id
                            )
                            target_segments.append(
                                f"<1><{paired_root_segment_count}>{str(ann)}"
                            )
                    if isinstance(segment_pair[self.target_pecha.id_], str):
                        if commentary_ann.id() == segment_pair[self.target_pecha.id_]:
                            paired_root_ann_id = segment_pair[self.source_pecha.id_]
                            paired_root_segment_count = root_segment_mapping.get(
                                paired_root_ann_id
                            )
                            target_segments.append(
                                f"<1><{paired_root_segment_count}>{str(ann)}"
                            )

            else:
                target_segments.append(str(ann))

        del ann_store

        output_path.mkdir(parents=True, exist_ok=True)

        """ write the json files"""
        root_json = self.get_standard_json(self.alignment.metadata["source"])
        root_json["books"][0]["content"][0] = source_segments
        (output_path / "root.json").write_text(
            json.dumps(root_json, ensure_ascii=False, indent=2)
        )

        commentary_json = self.get_standard_json(self.alignment.metadata["target"])

        commentary_json["books"][0]["content"][0] = target_segments
        (output_path / "commentary.json").write_text(
            json.dumps(commentary_json, ensure_ascii=False, indent=2)
        )
