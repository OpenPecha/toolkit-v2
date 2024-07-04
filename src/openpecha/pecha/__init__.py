import json
from pathlib import Path
from shutil import rmtree
from typing import Dict

from stam import AnnotationStore, Offset, Selector

from openpecha.config import (
    PECHA_ANNOTATION_STORE_ID,
    PECHA_DATASET_ID,
    PECHAS_PATH,
    _mkdir,
)
from openpecha.ids import get_uuid
from openpecha.pecha.annotation import Annotation
from openpecha.pecha.layer import Layer, LayerEnum


class Pecha:
    def __init__(
        self,
        pecha_id: str,
        bases: Dict[str, str],
        layers: Dict[str, Dict[LayerEnum, Layer]],
        metadata: Dict[str, str],
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

    def write(self, export_path: Path = PECHAS_PATH):

        pecha_dir = _mkdir(export_path / self.pecha_id)
        self.base_path = _mkdir(pecha_dir / f"{self.pecha_id}.opf")
        """ write metadata """
        self.metadata_fn = self.base_path / "metadata.json"
        self.metadata_fn.write_text(
            json.dumps(self.metadata, indent=4, ensure_ascii=False), encoding="utf-8"
        )

        """ write base file"""
        base_dir = _mkdir(self.base_path / "base")
        for base_fname, base_text in self.bases.items():
            base_fn = base_dir / f"{base_fname}.txt"
            base_fn.write_text(base_text, encoding="utf-8")

        layer_dir = _mkdir(self.base_path / "layers")
        """ write annotation layers"""
        for layer_fname, layer_data in self.layers.items():
            for _, layer in layer_data.items():
                _mkdir(layer_dir / layer_fname)
                layer.write(
                    base_file_path=base_dir / layer_fname,
                    export_path=layer_dir / layer_fname,
                )
