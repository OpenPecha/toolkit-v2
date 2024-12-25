import os
from pathlib import Path
from typing import Dict, Union

from openpecha.alignment.ann_transfer import AlignmentAnnTransfer
from openpecha.pecha import Pecha, StamPecha
from openpecha.pecha.layer import LayerEnum


class CommentaryAlignmentAnnTransfer(AlignmentAnnTransfer):
    def __init__(self, source: Dict, target: Dict, commentary: Dict):
        super().__init__(source, target)

        self.commentary_pecha_path: Path = commentary["commentary_pecha_path"]
        self.commentary_base_name = commentary["commentary_base_name"]

        self.commentary_pecha_id: str = self.commentary_pecha_path.name
        self.commentary_layer_name: Union[str, None] = None

    def transfer_annotation(self):
        """
        Normalises the coordinate of the commentary layer based on the display layer.
        """
        display_layer_ann = self.get_display_layer_anns()
        transfered_layer_ann = self.get_transfered_layer_anns()
        transfered_to_display_map = self.map_display_to_transfer(
            display_layer_ann, transfered_layer_ann
        )
        self.create_display_commentary_alignment_layer(transfered_to_display_map)
        self.write_layer()

    def create_display_commentary_alignment_layer(self, transfered_to_display):
        """
        Creates a dictionary of display and commentary alignment layer annotations.
        """
        curr_ann = {}
        commentary_layer_ann = {}
        commentary_pecha = StamPecha(self.commentary_pecha_path)
        self.commentary_layer = commentary_pecha.get_layers(self.commentary_base_name)
        for layer in self.commentary_layer:
            if not layer[0].startswith(LayerEnum.meaning_segment.value):
                continue

            for ann in layer[1]:
                start, end = ann.offset().begin().value(), ann.offset().end().value()
                ann_metadata = {}
                for data in ann:
                    ann_metadata[data.key().id()] = str(data.value())
                if "root_idx_mapping" in ann_metadata:

                    curr_ann[ann_metadata["root_idx_mapping"]] = {
                        "Span": {"start": start, "end": end},
                    }
                    commentary_layer_ann.update(curr_ann)
                    curr_ann = {}

        for alignment_key, display_info in transfered_to_display.items():
            if alignment_key not in commentary_layer_ann:
                continue
            start, end = (
                commentary_layer_ann[alignment_key]["Span"]["start"],
                commentary_layer_ann[alignment_key]["Span"]["end"],
            )
            curr_ann[alignment_key] = {
                "Span": {"start": start, "end": end},
                "alignment_mapping": display_info,
            }
            self.alignment_data.update(curr_ann)
            curr_ann = {}

    def write_layer(self):
        """
        Writes the alignment data to the commentary pecha layer.
        """
        pecha = Pecha.from_path(self.commentary_pecha_path)
        segment, segment_path = pecha.add_layer(
            self.commentary_base_name, LayerEnum.pecha_display_alignment_segment
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
            pecha_path=self.commentary_pecha_path,
            new_metadata={
                "pecha_display_segment_alignments": [
                    {
                        "pecha_display": os.path.relpath(
                            f"{self.target_pecha_id}/layers/{self.target_base_name}/{self.target_layer_name}"
                        ),
                        "commentary": os.path.relpath(segment_path.as_posix()),
                    }
                ]
            },
        )
