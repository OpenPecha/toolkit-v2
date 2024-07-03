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
        bases: Dict[str, str] = None,
        layers: Dict[str, Dict[LayerEnum, Layer]] = None,
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
