import json
from pathlib import Path
from typing import List, Optional

from openpecha.alignment import Alignment, AlignmentMetaData
from openpecha.alignment.metadata import AlignmentRelationEnum, SegmentMetaData
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import PechaMetaData
from openpecha.pecha.parsers import DummyParser


class PlainTextLineAlignedParser:
    """
    Class to parse plain text lines and create aligned annotations.
    """

    def __init__(self, source_text: str, target_text: str, metadata: dict):
        self.source_text = source_text
        self.target_text = target_text
        self.metadata = metadata

    @classmethod
    def from_files(
        cls, source_path: Path, target_path: Path, metadata_path: Path
    ) -> "PlainTextLineAlignedParser":
        """
        Create a parser instance from file paths.
        """
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        with open(metadata_path) as f:
            metadata = json.load(f)
        return cls(source_text, target_text, metadata)

    def parse(self, output_path: Path) -> Optional[Alignment]:
        """
        Parse the source and target texts, create annotations, and save to files.
        """
        (source_layer, source_layer_name), (
            target_layer,
            target_layer_name,
        ) = self.parse_pechas(output_path)
        self.source_layer = source_layer
        self.target_layer = target_layer

        alignment = self.create_alignment(source_layer_name, target_layer_name)
        if alignment:
            alignment.write(output_path)
        return alignment

    def create_alignment(
        self, source_layer_name: str, target_layer_name: str
    ) -> Optional[Alignment]:
        if not self.source_layer or not self.target_layer:
            return None

        """ building alignment metadata """
        source_resource_id = next(self.source_layer.resources()).id()
        source_metadata = {
            "type": LayerEnum.root_segment.value,
            "relation": AlignmentRelationEnum.source.value,
            "lang": self.metadata["source"]["language"],
            "base": source_resource_id,
            "layer": source_layer_name,
        }
        source_metadata = SegmentMetaData(**source_metadata)

        target_resource_id = next(self.target_layer.resources()).id()
        target_metadata = {
            "type": LayerEnum.commentary_segment.value,
            "relation": AlignmentRelationEnum.target.value,
            "lang": self.metadata["target"]["language"],
            "base": target_resource_id,
            "layer": target_layer_name,
        }
        target_metadata = SegmentMetaData(**target_metadata)

        source_id = self.source_layer.id()
        target_id = self.target_layer.id()
        alignment_metadata = {
            "segments_metadata": {
                source_id: source_metadata,
                target_id: target_metadata,
            },
            "source_metadata": {},
        }

        alignment_metadata = AlignmentMetaData(**alignment_metadata)
        segment_pairs = [
            ((source_id, source_ann.id()), (target_id, target_ann.id()))
            for source_ann, target_ann in zip(
                self.source_layer.annotations(), self.target_layer.annotations()
            )
        ]

        alignment = Alignment.from_segment_pairs(segment_pairs, alignment_metadata)
        return alignment

    def parse_pechas(self, output_path: Path):

        source_metadata = PechaMetaData(
            parser=DummyParser().name, **self.metadata["source"]
        )
        target_metadata = PechaMetaData(
            parser=DummyParser().name, **self.metadata["target"]
        )

        source_layer, source_layer_name = create_pecha_stam(
            self.source_text, source_metadata, LayerEnum.root_segment, output_path
        )
        target_layer, target_layer_name = create_pecha_stam(
            self.target_text, target_metadata, LayerEnum.commentary_segment, output_path
        )

        return (source_layer, source_layer_name), (target_layer, target_layer_name)


def create_pecha_stam(
    base_text: str, metadata: PechaMetaData, ann_type: LayerEnum, output_path: Path
):

    pecha = Pecha.create(output_path)
    base_name = pecha.set_base(base_text)

    pecha.set_metadata(metadata)

    layer, layer_path = pecha.add_layer(base_name, ann_type)

    """ create annotation for each line in new annotation store"""
    lines = split_text_into_lines(base_text)
    char_count = 0
    for line in lines:
        annotation = {
            ann_type.value: {
                "start": char_count,
                "end": char_count + len(line),
            }
        }
        pecha.add_annotation(layer, annotation, ann_type)
        char_count += len(line)

    layer.save()
    return (layer, layer_path.name)


def split_text_into_lines(text: str) -> List[str]:
    """
    Split text into lines and ensure each line ends with a newline character.
    """
    lines = text.split("\n")
    return [line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)]
