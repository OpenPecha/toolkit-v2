import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional, Tuple

from openpecha.config import PECHAS_PATH, _mkdir
from openpecha.github_utils import clone_github_repo
from openpecha.ids import get_uuid
from openpecha.pecha.layer import Layer, LayerEnum
from openpecha.pecha.metadata import (
    InitialCreationType,
    PechaMetadata,
    to_json_serializable,
)


class Pecha:
    def __init__(
        self,
        pecha_id: str = None,
        bases: Dict[str, str] = defaultdict(str),
        layers: Dict[str, Dict[Tuple[LayerEnum, str], Layer]] = defaultdict(
            lambda: defaultdict()
        ),
        metadata: PechaMetadata = None,
    ) -> None:
        self.pecha_id = metadata.id_ if metadata else pecha_id
        self.bases = bases
        self.layers = layers
        self.metadata = metadata

    @classmethod
    def from_path(cls, pecha_path: Path):
        pecha_id = pecha_path.stem
        base_path = pecha_path / f"{pecha_id}.opf"
        with open(base_path / "metadata.json", encoding="utf-8") as f:
            metadata = json.load(f)
            metadata = json.loads(metadata)

        preprocessed_meta = preprocess_metadata(metadata)
        pecha_metadata = PechaMetadata(**preprocessed_meta)
        pecha = Pecha(metadata=pecha_metadata)
        pecha.pecha_path = pecha_path

        for base_file in (base_path / "base").rglob("*"):
            base_text = base_file.read_text(encoding="utf-8")
            pecha.set_base_file(base_text, base_file.stem)

        for layer_dir in (base_path / "layers").iterdir():
            for layer_file in layer_dir.glob("*.json"):
                layer = Layer.from_path(layer_file)
                pecha.set_layer(layer_dir.stem, layer.annotation_type, layer, layer.id_)

        return pecha

    @classmethod
    def from_id(cls, pecha_id: str):
        repo_path = clone_github_repo(pecha_id, PECHAS_PATH)
        return cls.from_path(repo_path)

    def set_base_file(self, base_text: str, base_file_name: str = None) -> str:
        base_file_name = base_file_name if base_file_name else get_uuid()[:4]
        self.bases[base_file_name] = base_text
        return base_file_name

    def set_layer(
        self,
        base_name: str,
        annotation_type: LayerEnum,
        layer: Layer,
        layer_subtype_id: str = None,
    ) -> str:

        """layer key is a tuple of layer label and layer id"""
        """ A particular volume can have multiple layers with same label but different id"""
        layer_subtype_id = get_uuid()[:4] if not layer_subtype_id else layer_subtype_id
        self.layers[base_name][(annotation_type, layer_subtype_id)] = layer
        return layer_subtype_id

    def write(self, output_path: Path = PECHAS_PATH):
        if not self.pecha_id:
            raise ValueError("pecha_id must be set before writing.")

        self.pecha_path = _mkdir(output_path / self.pecha_id)

        self.base_path = _mkdir(self.pecha_path / f"{self.pecha_id}.opf")
        """ write metadata """
        self.metadata_fn = self.base_path / "metadata.json"
        self.metadata_fn.write_text(
            json.dumps(
                to_json_serializable(self.metadata), indent=4, ensure_ascii=False
            ),
            encoding="utf-8",
        )

        """ write base file"""
        if self.bases:
            base_dir = _mkdir(self.base_path / "base")
            for base_name, base_text in self.bases.items():
                base_fn = base_dir / f"{base_name}.txt"
                base_fn.write_text(base_text, encoding="utf-8")
        if self.layers:
            layer_dir = _mkdir(self.base_path / "layers")
            """ write annotation layers"""
            for layer_name, layer_data in self.layers.items():
                for _, layer in layer_data.items():
                    _mkdir(layer_dir / layer_name)
                    layer.write(
                        base_file_path=base_dir / f"{layer_name}.txt",
                        output_path=output_path,
                    )


def preprocess_metadata(metadata: Dict) -> Dict:
    # Replace null values with default values
    processed_metadata = {
        "id_": metadata.get("id_", ""),
        "title": metadata.get("title", []) if metadata.get("title") is not None else [],
        "author": metadata.get("author", [])
        if metadata.get("author") is not None
        else [],
        "source": metadata.get("source", "")
        if metadata.get("source") is not None
        else "",
        "language": metadata.get("language", "")
        if metadata.get("language") is not None
        else "",
        "initial_creation_type": InitialCreationType(metadata["initial_creation_type"])
        if "initial_creation_type" in metadata
        else None,
        "created_at": metadata.get("created_at"),
        "source_metadata": metadata.get("source_metadata", {})
        if metadata.get("source_metadata") is not None
        else {},
    }
    return processed_metadata
