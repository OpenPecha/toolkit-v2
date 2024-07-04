from pathlib import Path
from typing import List

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

    def create_pecha_layer(self, segments: List[str], annotation_label: LayerEnum):
        """ """
        layer = Layer(annotation_label=annotation_label, annotations={})
        char_count = 0
        for segment in segments:
            annotation = Annotation(
                segment=segment,
                start=char_count,
                end=char_count + len(segment),
            )
            layer.set_annotation(annotation)
            char_count += len(segment)

        return layer

    def parse(self):
        source_pecha_id, target_pecha_id = (
            get_initial_pecha_id(),
            get_initial_pecha_id(),
        )
        source_pecha = Pecha(source_pecha_id)
        target_pecha = Pecha(target_pecha_id)

        source_base_fname, target_base_fname = get_uuid(), get_uuid()
        source_pecha.set_base_file(source_base_fname, self.source_text)
        target_pecha.set_base_file(target_base_fname, self.target_text)

        source_annotation = LayerEnum(self.metadata["source"]["annotation_label"])
        target_annotation = LayerEnum(self.metadata["target"]["annotation_label"])

        source_pecha.set_layer(
            source_base_fname,
            (source_annotation, None),
            self.create_pecha_layer(self.source_text.split("\n"), source_annotation),
        )
        target_pecha.set_layer(
            target_base_fname,
            (target_annotation, None),
            self.create_pecha_layer(self.target_text.split("\n"), target_annotation),
        )

        source_pecha.set_metadata(self.metadata["source"])
        target_pecha.set_metadata(self.metadata["target"])

        return source_pecha, target_pecha

        # TODO:

        # 2. create a segment pairs [((source_pecha_id,source_segment_id), (target_pecha_id, target_segment_id)), ...]
        # 3. Create AlignmentMetadata

        """
        alignment = Alignment.from_segment_pairs(segment_pairs, metadata)
        alignment.save(path)
        """
        pass
