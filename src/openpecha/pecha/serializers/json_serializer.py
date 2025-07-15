from stam import AnnotationStore

from openpecha.pecha import Pecha
from openpecha.pecha.layer import get_annotation_type


class JsonSerializer:
    def get_base(self, pecha: Pecha):
        basename = list(pecha.bases.keys())[0]
        base = pecha.get_base(basename)
        return base

    @staticmethod
    def to_dict(ann_store: AnnotationStore):
        anns = []
        for ann in ann_store:
            ann_data = {}
            for data in ann:
                ann_data[data.key().id()] = data.value().get()
            curr_ann = {
                "id": ann.id(),
                "Span": {
                    "start": ann.offset().begin().value(),
                    "end": ann.offset().end().value(),
                },
                **ann_data,
            }

            anns.append(curr_ann)
        return anns

    @staticmethod
    def _get_ann_type(layer_path: str):
        layer_name = layer_path.split("/")[1]
        ann_name = layer_name.split("-")[0]
        return get_annotation_type(ann_name)

    def get_annotations(self, pecha: Pecha, layer_path: str):
        anns = self.to_dict(
            ann_store=AnnotationStore(file=str(pecha.layer_path / layer_path))
        )
        base = self.get_base(pecha)

        ann_type = self._get_ann_type(layer_path)
        res = {"base": base, "annotations": {ann_type.value: anns}}
        return res
