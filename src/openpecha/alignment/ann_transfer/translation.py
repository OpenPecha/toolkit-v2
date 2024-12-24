import os
from pathlib import Path
from typing import Dict, Union

from openpecha.alignment.ann_transfer import AlignmentAnnTransfer
from openpecha.pecha import Pecha, StamPecha
from openpecha.pecha.layer import LayerEnum


class TranslationAlignmentAnnTransfer(AlignmentAnnTransfer):
    def __init__(self, source: Dict, target: Dict, translation: Dict):
        super().__init__(source, target)

        self.translation_pecha_path: Path = translation["translation_pecha_path"]
        self.translation_base_name = translation["translation_base_name"]

        self.translation_pecha_id: str = self.translation_pecha_path.name
        self.translation_layer_name: Union[str, None] = None

    def normalise_coordinate(self):
        """
        Normalises the coordinate of the translation layer based on the display layer.
        """
        display_layer_ann = self.get_display_layer_anns()
        transfered_layer_ann = self.get_transfered_layer_anns()
        transfered_to_display_map = self.map_display_to_transfer(
            display_layer_ann, transfered_layer_ann
        )
        self.create_display_translation_alignment_layer(transfered_to_display_map)
        self.write_layer()

    def create_display_translation_alignment_layer(self, transfered_to_display):
        """
        Creates a dictionary of display and translation alignment layer annotations.
        """
        curr_ann = {}
        translation_layer_ann = {}
        translation_pecha = StamPecha(self.translation_pecha_path)
        self.translation_layer = translation_pecha.get_layers(
            self.translation_base_name
        )
        for layer in self.translation_layer:
            for ann in layer[1]:
                start, end = ann.offset().begin().value(), ann.offset().end().value()
                ann_metadata = {}
                for data in ann:
                    ann_metadata[data.key().id()] = str(data.value())
                curr_ann[int(ann_metadata["root_idx_mapping"])] = {
                    "Span": {"start": start, "end": end},
                }
                translation_layer_ann.update(curr_ann)
                curr_ann = {}

        for alignment_key, display_info in transfered_to_display.items():
            start, end = (
                translation_layer_ann[alignment_key]["Span"]["start"],
                translation_layer_ann[alignment_key]["Span"]["end"],
            )
            curr_ann[alignment_key] = {
                "Span": {"start": start, "end": end},
                "alignment_mapping": display_info,
            }
            self.alignment_data.update(curr_ann)
            curr_ann = {}

    def write_layer(self):
        """
        Writes the alignment data to the translation pecha layer.
        """
        pecha = Pecha(
            pecha_id=self.translation_pecha_id, pecha_path=self.translation_pecha_path
        )
        segment, segment_path = pecha.add_layer(
            self.translation_base_name, LayerEnum.pecha_display_alignment_segment
        )
        for root_id, info in self.alignment_data.items():
            alignment_info = info["alignment_mapping"]
            segment_ann = {
                LayerEnum.pecha_display_alignment_segment.value: info["Span"],
                "root_idx_mapping": root_id,
                "alignment_mapping": alignment_info,
            }
            pecha.add_annotation(
                segment, segment_ann, LayerEnum.pecha_display_alignment_segment
            )
        segment.save()

        self.update_metadata(
            pecha_path=self.translation_pecha_path,
            new_metadata={
                "pecha_display_segment_alignments": [
                    {
                        "pecha_display": os.path.relpath(
                            f"{self.target_pecha_id}/layers/{self.target_base_name}/{self.target_layer_name}"
                        ),
                        "translation": os.path.relpath(segment_path.as_posix()),
                    }
                ]
            },
        )
