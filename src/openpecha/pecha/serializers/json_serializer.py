from stam import AnnotationStore

from openpecha.exceptions import AnnotationLayerIsNotSegmentationOrAlignment
from openpecha.pecha import Pecha
from openpecha.pecha.layer import AnnotationType, get_annotation_type


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
            curr_ann = {"id": ann.id(), **ann_data}
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

    def map_layers(
        self,
        src_pecha: Pecha,
        src_layer_name: str,
        tgt_pecha: Pecha,
        tgt_layer_name: str,
    ):
        """
        Create a mapping from source annotation layer to target annotation layer.
        """

        src_ann_type = get_annotation_type(
            src_layer_name.split("/")[1]
        )  # src_layer_name contains base_name/layer_name
        tgt_ann_type = get_annotation_type(tgt_layer_name.split("/")[1])

        if src_ann_type not in [AnnotationType.SEGMENTATION, AnnotationType.ALIGNMENT]:
            raise AnnotationLayerIsNotSegmentationOrAlignment(
                f"Pecha {src_pecha.id} and its layer {src_layer_name} is not segmentation or alignment layer to map with other layer."
            )

        if tgt_ann_type not in [AnnotationType.SEGMENTATION, AnnotationType.ALIGNMENT]:
            raise AnnotationLayerIsNotSegmentationOrAlignment(
                f"Pecha {src_pecha.id} and its layer {src_layer_name} is not segmentation or alignment layer to map with other layer."
            )

        src_annotations = self.get_annotations(src_pecha, src_layer_name)  # noqa
        tgt_annotations = self.get_annotations(tgt_pecha, tgt_layer_name)  # noqa


if __name__ == "__main__":
    ann_type = AnnotationType("segmentation")
    print(ann_type)
