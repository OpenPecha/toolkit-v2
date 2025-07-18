from stam import AnnotationStore

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import SpellingVariantOperations
from openpecha.pecha.layer import (
    AnnotationType,
    get_annotation_group_type,
    get_annotation_type,
)


class JsonSerializer:
    def get_base(self, pecha: Pecha):
        basename = list(pecha.bases.keys())[0]
        base = pecha.get_base(basename)
        return base

    @staticmethod
    def to_dict(ann_store: AnnotationStore, ann_type: AnnotationType):
        ann_group = get_annotation_group_type(ann_type)
        anns = []
        for ann in ann_store:
            ann_data = {}
            for data in ann:
                k, v = data.key().id(), data.value().get()
                if k != ann_group.value:
                    ann_data[k] = v
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

    def get_edition_base(self, pecha: Pecha, edition_layer_path: str) -> str:
        """
        1.Get base from Pecha.
        2.Read Spelling Variant Annotations from Edition Layer path
        3.Form a new base for Edition
        """
        ann_store = AnnotationStore(file=str(pecha.layer_path / edition_layer_path))
        ann_type = self._get_ann_type(edition_layer_path)
        anns = self.to_dict(ann_store, ann_type)

        old_base = self.get_base(pecha)
        edition_base = ""

        cursor = 0
        for ann in anns:
            start, end = ann["Span"]["start"], ann["Span"]["end"]
            operation, text = ann["operation"], ann["text"]

            edition_base += old_base[cursor:start]

            if operation == SpellingVariantOperations.INSERTION:
                edition_base += text
            elif operation == SpellingVariantOperations.DELETION:
                pass  # Skip deleted text
            else:
                raise ValueError(
                    f"Invalid operation: {operation}. Expected 'insertion' or 'deletion'."
                )

            cursor = end

        return edition_base

    def serialize(self, pecha: Pecha, layer_paths: str | list[str]):
        """
        Get annotations for a single or list of layer paths.
        Each layer_path is a string like: "B5FE/segmentation-4FD1.json"
        """
        if isinstance(layer_paths, str):
            layer_paths = [layer_paths]

        annotations = {}
        for layer_path in layer_paths:
            ann_store = AnnotationStore(file=str(pecha.layer_path / layer_path))
            ann_type = self._get_ann_type(layer_path)
            anns = self.to_dict(ann_store, ann_type)
            annotations[ann_type.value] = anns

        base = self.get_base(pecha)
        return {"base": base, "annotations": annotations}
