from pathlib import Path

from stam import AnnotationStore

from openpecha.config import PECHAS_PATH
from openpecha.github_utils import git_clone
from openpecha.pecha.layer import LayerEnum


class Pecha:
    def __init__(self, pecha_id: str, base_path: Path) -> None:
        self.id_ = pecha_id
        self.base_path = base_path

    @classmethod
    def from_id(cls, pecha_id: str):
        pecha_path = git_clone(pecha_id, PECHAS_PATH)
        return Pecha.from_path(pecha_path)

    @classmethod
    def from_path(cls, pecha_path: Path) -> "Pecha":
        pecha_id = pecha_path.stem
        return cls(pecha_id, pecha_path)

    @property
    def ann_path(self):
        return self.base_path / "layers"

    def get_annotation_store(self, annotation_type: LayerEnum):
        annotation_type_file_paths = list(
            self.ann_path.glob(f"{annotation_type.value}*.json")
        )
        annotation_stores = [
            AnnotationStore(file=str(annotation_file))
            for annotation_file in annotation_type_file_paths
        ]

        if len(annotation_stores) == 1:
            return annotation_stores[0]

        return annotation_stores
