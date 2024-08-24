from stam import AnnotationStore

from openpecha.alignment.alignment import Alignment
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum


class JSONSerializer:
    def __init__(self, alignment: Alignment):
        self.alignment = alignment

    def load_pechas(self, source_pecha: Pecha, target_pecha: Pecha):
        self.source_pecha = source_pecha
        self.target_pecha = target_pecha

        root_segment_file = next(
            self.source_pecha.ann_path.rglob(f"{LayerEnum.root_segment.value}*.json")
        )

        commentary_segment_file = next(
            self.target_pecha.ann_path.rglob(
                f"{LayerEnum.commentary_segment.value}*.json"
            )
        )

        source_ann_store = AnnotationStore(file=root_segment_file.as_posix())
        target_ann_store = AnnotationStore(file=commentary_segment_file.as_posix())

        return source_ann_store, target_ann_store

    # def serialize(self, output_path: Path):
