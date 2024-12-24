import os
from pathlib import Path
from typing import Dict, Generator, Union

from stam import AnnotationStore

from openpecha.pecha import Pecha, StamPecha
from openpecha.pecha.layer import LayerEnum


class AlignmentAnnTransfer:
    def __init__(self, source: Dict, target: Dict):
        self.source_pecha_path: Path = source["source_pecha_path"]
        self.target_pecha_path: Path = target["target_pecha_path"]
        self.source_base_name: str = source["source_base_name"]
        self.target_base_name: str = target["target_base_name"]

        self.source_pecha_id: str = self.source_pecha_path.name
        self.target_pecha_id: str = self.target_pecha_path.name

        self.target_layer: Union[Generator, None] = None
        self.source_layer: Union[Generator, None] = None
        self.target_layer_name: Union[str, None] = None
        self.source_layer_name: Union[str, None] = None

        self.alignment_data: Dict = {}
        self.transfer_layer()

    def update_metadata(self, pecha_path: Path, new_metadata: Dict):
        """
        Updates the source metadata of the pecha with the given data.
        """
        pecha = Pecha.from_path(pecha_path)
        pecha_metadata = pecha.metadata
        field_name = list(new_metadata.keys())[0]
        if field_name in pecha_metadata.source_metadata:
            pecha_metadata.source_metadata[field_name].append(new_metadata[field_name])
        else:
            pecha_metadata.source_metadata[field_name] = new_metadata[field_name]
        pecha.set_metadata(pecha_metadata=pecha_metadata)

        pecha.publish()

    def transfer_layer(self):
        """
        Transfer the annotation layer from source to target pecha with give basename.
        """
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
            new_metadata={
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
        """
        Get layer name from source and target pecha and translation pecha.
        """
        if self.source_layer:
            self.source_layer_name = next(self.source_layer)[0]
        if self.target_layer:
            self.target_layer_name = next(self.target_layer)[0]

    @staticmethod
    def get_root_anns(layer: AnnotationStore):
        """
        Get the root annotation from the given root layer(STAM)
        """
        anns = {}
        for ann in layer:
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            ann_metadata = {}
            for data in ann:
                ann_metadata[data.key().id()] = str(data.value())
            anns[int(ann_metadata["root_idx_mapping"])] = {
                "Span": {"start": start, "end": end},
                "text": str(ann),
            }
        return anns

    def get_transfered_layer_anns(self):
        """
        Get the annotations of the transfered layer from the target Pecha.
        """
        assert self.target_layer is not None, "Target layer is not set."

        target_pecha = StamPecha(self.target_pecha_path)
        self.target_layer = target_pecha.get_layers(self.target_base_name)
        tranfered_layer = next(
            (
                layer
                for layer in self.target_layer
                if layer[0] == self.source_layer_name
            ),
            None,
        )
        assert tranfered_layer, "tranfered layer not found in the target pecha."

        return self.get_root_anns(tranfered_layer[1])

    def get_display_layer_anns(self):
        """
        Get the annotations of the display layer from the target Pecha.
        """
        assert self.target_layer is not None, "Target layer is not set."
        target_pecha = StamPecha(self.target_pecha_path)
        self.target_layer = target_pecha.get_layers(self.target_base_name)
        display_layer = next(
            (
                layer
                for layer in self.target_layer
                if layer[0] != self.source_layer_name
            ),
            None,
        )
        assert display_layer, "Display layer not found in the target pecha."

        return self.get_root_anns(display_layer[1])

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
