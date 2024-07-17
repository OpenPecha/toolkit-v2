from pathlib import Path

from stam import AnnotationStore

from openpecha.pecha.layer import LayerEnum


class Pecha:
    def __init__(self, pecha_id: str, annotation_path: Path) -> None:
        self.id_ = pecha_id
        self.ann_path = annotation_path

    @classmethod
    def from_path(cls, pecha_path: Path) -> "Pecha":
        pecha_id = pecha_path.stem
        annotation_path = pecha_path / "layers"
        return cls(pecha_id, annotation_path)

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
