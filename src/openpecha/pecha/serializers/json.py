from stam import AnnotationStore

from openpecha.pecha import Pecha


class JsonSerializer:
    def get_base(self, pecha: Pecha):
        basename = list(pecha.bases.keys())[0]
        base = pecha.get_base(basename)
        return base

    @staticmethod
    def to_dict(ann_store: AnnotationStore, include_span: bool = False):
        anns = []
        for ann in ann_store:
            ann_data = {}
            for data in ann:
                ann_data[data.key().id()] = data.value().get()
            curr_ann = {**ann_data}
            if include_span:
                curr_ann["Span"] = {
                    "start": ann.offset().begin().value(),
                    "end": ann.offset().end().value(),
                }
            anns.append(curr_ann)
        return anns

    def get_annotations(self, pecha: Pecha, layer_name: str):
        layer_path = pecha.layer_path / layer_name
        anns = self.to_dict(ann_store=AnnotationStore(file=str(layer_path)))
        return anns
