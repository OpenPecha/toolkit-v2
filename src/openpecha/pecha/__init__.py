import json
from pathlib import Path
from typing import Dict, Optional, Tuple

from openpecha.config import PECHAS_PATH, _mkdir
from openpecha.ids import get_uuid
from openpecha.pecha.layer import Layer, LayerEnum


class Pecha:
    def __init__(
        self,
        pecha_id: str,
        bases: Dict[str, str] = None,
        layers: Dict[str, Dict[Tuple[LayerEnum, str], Layer]] = None,
        metadata: Dict[str, str] = None,
    ) -> None:
        self.pecha_id = pecha_id
        self.bases = bases
        self.layers = layers
        self.metadata = metadata

    @classmethod
    def from_path(cls, base_path: Path):
        pecha_id = base_path.stem
        pecha = Pecha(pecha_id=pecha_id)

        with open(base_path / "metadata.json", encoding="utf-8") as f:
            metadata = json.load(f)
            pecha.set_metadata(metadata)

        for base_file in (base_path / "base").rglob("*.txt"):
            base_text = base_file.read_text(encoding="utf-8")
            pecha.set_base_file(base_file.stem, base_text)

        for layer_dir in (base_path / "layers").iterdir():
            for layer_file in layer_dir.glob("*.json"):
                layer = Layer.from_path(layer_file)
                layer_key = (layer.annotation_label, layer_file.stem)
                pecha.set_layer(layer_dir.stem, layer_key, layer)

        return pecha

    @classmethod
    def from_id(cls, pecha_id: str):
        pass

    def set_base_file(self, base_file_name: str, base_text: str):
        if not self.bases:
            self.bases = {}
        self.bases[base_file_name] = base_text

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

    def write(self, export_path: Path = PECHAS_PATH):

        pecha_dir = _mkdir(export_path / self.pecha_id)
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
                        export_path=export_path,
                    )
