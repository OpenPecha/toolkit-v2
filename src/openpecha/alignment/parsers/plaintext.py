from pathlib import Path
from typing import Dict

from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha import Pecha
from openpecha.pecha.annotation import Annotation
from openpecha.pecha.layer import Layer, LayerEnum


class PlainTextLineAlignedParser:
    def __init__(self, source_text: str, target_text: str, metadata: dict):
        self.source_text = source_text
        self.target_text = target_text
        self.metadata = metadata

    @classmethod
    def from_files(cls, source_path: Path, target_path: Path, metadata: dict):
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        return cls(source_text, target_text, metadata)

    def create_pecha_layer(self, base_text: str, annotation: LayerEnum):
        """ """
        layer_annotations: Dict[str, Annotation] = {}
        char_count = 0
        for segment in base_text.split("\n"):
            layer_annotations[get_uuid()] = Annotation(
                id_=get_uuid(),
                segment=segment,
                start=char_count,
                end=char_count + len(segment),
            )
            char_count += len(segment)

        return Layer(annotation_label=annotation, annotations=layer_annotations)

    def parse(self):
        source_pecha_id, target_pecha_id = (
            get_initial_pecha_id(),
            get_initial_pecha_id(),
        )

        source_base_fname, target_base_fname = get_uuid(), get_uuid()
        source_base_files = {source_base_fname: self.source_text}
        target_base_files = {target_base_fname: self.target_text}

        source_annotation = LayerEnum(self.metadata["source"]["annotation_label"])
        target_annotation = LayerEnum(self.metadata["target"]["annotation_label"])

        source_layers = {
            source_base_fname: {
                source_annotation: self.create_pecha_layer(
                    self.source_text, source_annotation
                )
            }
        }
        target_layers = {
            target_base_fname: {
                target_annotation: self.create_pecha_layer(
                    self.target_text, target_annotation
                ),
            }
        }

        source_pecha = Pecha(  # noqa
            source_pecha_id, source_base_files, source_layers, self.metadata["source"]
        )
        target_pecha = Pecha(  # noqa
            target_pecha_id, target_base_files, target_layers, self.metadata["target"]
        )
        return source_pecha, target_pecha

        # TODO:

        # 2. create a segment pairs [((source_pecha_id,source_segment_id), (target_pecha_id, target_segment_id)), ...]
        # 3. Create AlignmentMetadata

        """
        alignment = Alignment.from_segment_pairs(segment_pairs, metadata)
        alignment.save(path)
        """
        pass
