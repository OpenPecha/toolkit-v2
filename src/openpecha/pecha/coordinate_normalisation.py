import os
from typing import Dict

from openpecha.pecha import Pecha, StamPecha
from openpecha.pecha.layer import LayerEnum


class CoordinateNormalisation:
    def __init__(self, source=dict, target=dict, translation=dict):
        self.source_pecha_path = source.get("source_pecha_path")
        self.target_pecha_path = target.get("target_pecha_path")
        self.source_base_name = source.get("source_base_name")
        self.target_base_name = target.get("target_base_name")
        self.translation_pecha_path = translation.get("translation_pecha_path")
        self.translation_base_name = translation.get("translation_base_name")
        self.source_pecha_id = self.source_pecha_path.name
        self.target_pecha_id = self.target_pecha_path.name
        self.translation_pecha_id = self.translation_pecha_path.name
        self.target_layer = None
        self.source_layer = None
        self.target_layer_name = None
        self.source_layer_name = None
        self.translation_layer_name = None
        self.alignment_data = {}
        self.transfer_layer()

    def update_metadata(self, pecha_path, dict_data):
        """
        Updates the metadata of the pecha with the given data.
        """
        pecha = Pecha.from_path(pecha_path)
        pecha_metadata = pecha.metadata
        dict_key = dict_data.keys()
        if dict_key in pecha_metadata.source_metadata:
            pecha_metadata.source_metadata[dict_key].append(dict_data.value())
        else:
            pecha_metadata.source_metadata = dict_data
        pecha.set_metadata(pecha_metadata=pecha_metadata)

        pecha.publish()

    def transfer_layer(self):
        target_pecha = StamPecha(self.target_pecha_path)
        source_pecha = StamPecha(self.source_pecha_path)
        self.target_layer = target_pecha.get_layers(self.target_base_name)
        self.source_layer = source_pecha.get_layers(self.source_base_name)
        self.get_layer_name()
        target_pecha.merge_pecha(
            source_pecha, self.source_base_name, self.target_base_name
        )
        self.update_metadata(
            pecha_path=self.target_pecha_path,
            dict_data={
                "segmentation_transfered": [
                    {
                        "source": os.path.relpath(
                            f"{self.source_pecha_path}/layers/{self.source_base_name}/{self.source_layer_name}"
                        ),
                        "transfered": os.path.relpath(
                            f"{self.target_pecha_path}/layers/{self.target_base_name}/{self.source_layer_name}"
                        ),
                    }
                ]
            },
        )

    def get_layer_name(self):
        if self.source_layer:
            for layer in self.source_layer:
                self.source_layer_name = layer[0]
        if self.target_layer:
            for layer in self.target_layer:
                self.target_layer_name = layer[0]
        translation_pecha = StamPecha(self.translation_pecha_path)
        translation_layer = translation_pecha.get_layers(self.translation_base_name)
        for layer in translation_layer:
            self.translation_layer_name = layer[0]

    def normalise_coordinate(self):
        """
        Normalises the coordinate of the translation layer based on the display layer.
        """
        curr_ann = {}
        transfered_layer_ann = {}
        display_layer_ann = {}
        target_pecha = StamPecha(self.target_pecha_path)
        self.target_layer = target_pecha.get_layers(self.target_base_name)
        for layer in self.target_layer:
            for ann in layer[1]:
                start, end = ann.offset().begin().value(), ann.offset().end().value()
                ann_metadata = {}
                for data in ann:
                    ann_metadata[data.key().id()] = str(data.value())
                curr_ann[int(ann_metadata["root_idx_mapping"])] = {
                    "Span": {"start": start, "end": end},
                    "text": str(ann),
                }
                if layer[0] == self.source_layer_name:
                    transfered_layer_ann.update(curr_ann)
                else:
                    display_layer_ann.update(curr_ann)
                curr_ann = {}
        transfered_to_display_map = self.map_display_to_transfer(
            display_layer_ann, transfered_layer_ann
        )
        self.create_display_translation_alignment_layer(transfered_to_display_map)
        self.write_layer()

    def map_display_to_transfer(self, display_layer_ann, transfer_layer_ann):
        """
        Maps display layer annotations to transfer layer annotations based on span overlap.

        Args:
            display_layer_ann: A dictionary of display layer annotations.
            transfer_layer_ann: A dictionary of transfer layer annotations.

        Returns:
            A dictionary mapping display keys to transfer keys.
        """
        transfered_to_display_map: Dict = {}
        for transfer_key, transfer_span in transfer_layer_ann.items():
            t_start, t_end = (
                transfer_span["Span"]["start"],
                transfer_span["Span"]["end"],
            )
            transfered_to_display_map[transfer_key] = []
            for display_key, display_span in display_layer_ann.items():
                d_start, d_end = (
                    display_span["Span"]["start"],
                    display_span["Span"]["end"],
                )
                if t_start <= d_start <= t_end or t_start <= d_end <= t_end:
                    transfered_to_display_map[transfer_key].append(
                        [display_key, [d_start, d_end]]
                    )
        sorted_mapping = dict(sorted(transfered_to_display_map.items()))
        return sorted_mapping

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
            dict_data={
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
