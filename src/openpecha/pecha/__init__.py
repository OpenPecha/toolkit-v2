import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional, Tuple

from openpecha.config import PECHAS_PATH, _mkdir
from openpecha.ids import get_uuid
from openpecha.pecha.layer import Layer, LayerEnum


class Pecha:
    def __init__(
        self,
        pecha_id: str,
        bases: Dict[str, str] = defaultdict(),
        layers: Dict[str, Dict[Tuple[LayerEnum, str], Layer]] = None,
        metadata: Dict[str, str] = None,
    ) -> None:
        self.pecha_id = pecha_id
        self.bases = bases
        self.layers = layers
        self.metadata = metadata

    @classmethod
    def from_path(cls, path: str):
        pass

    @classmethod
    def from_id(cls, pecha_id: str):
        pass

    def set_base_file(self, base_text: str) -> str:
        base_file_name = get_uuid()
        self.bases[base_file_name] = base_text
        return base_file_name

    def set_layer(
        self, layer_dir: str, layer_key: Tuple[LayerEnum, Optional[str]], layer: Layer
    ):
        """Note layer dir should be same as its corresponding base file name"""
        if not self.layers:
            self.layers = {}
        if layer_dir not in self.layers:
            self.layers[layer_dir] = {}

        """ layer key is a tuple of layer label and layer id"""
        """ A particular volume can have multiple layers with same label but different id"""
        layer_label, layer_id = layer_key
        layer_id = layer_id if layer_id else get_uuid()
        self.layers[layer_dir][(layer_label, layer_id)] = layer

    def set_metadata(self, metadata: Dict[str, str]):
        if not self.metadata:
            self.metadata = {}
        for key, value in metadata.items():
            self.metadata[key] = value

    def write(self, output_path: Path = PECHAS_PATH):

        pecha_dir = _mkdir(output_path / self.pecha_id)
        self.base_path = _mkdir(pecha_dir / f"{self.pecha_id}.opf")
        """ write metadata """
        self.metadata_fn = self.base_path / "metadata.json"
        self.metadata_fn.write_text(
            json.dumps(self.metadata, indent=4, ensure_ascii=False), encoding="utf-8"
        )

        """ write base file"""
        if self.bases:
            base_dir = _mkdir(self.base_path / "base")
            for base_fname, base_text in self.bases.items():
                base_fn = base_dir / f"{base_fname}.txt"
                base_fn.write_text(base_text, encoding="utf-8")
        if self.layers:
            layer_dir = _mkdir(self.base_path / "layers")
            """ write annotation layers"""
            for layer_fname, layer_data in self.layers.items():
                for _, layer in layer_data.items():
                    _mkdir(layer_dir / layer_fname)
                    layer.write(
                        base_file_path=base_dir / f"{layer_fname}.txt",
                        output_path=output_path,
                    )
