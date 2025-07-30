import shutil
import tempfile
from pathlib import Path

from stam import AnnotationStore

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import VersionVariantOperations
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

            if operation == VersionVariantOperations.INSERTION:
                edition_base += text
            elif operation == VersionVariantOperations.DELETION:
                pass  # Skip deleted text
            else:
                raise ValueError(
                    f"Invalid operation: {operation}. Expected 'insertion' or 'deletion'."
                )

            cursor = end

        return edition_base

    def get_layer_paths(self, pecha: Pecha, annotations: list[dict]):
    
        def get_annotation_names(annotations: list[dict]):
            annotation_filenames = []
            for annotation in annotations:
                filename = annotation['type'] + "-" + annotation["name"]
                annotation_filenames.append(filename)
            return annotation_filenames
        
        layer_paths = []
        annotation_names = get_annotation_names(annotations)
        for base_name in pecha.bases.keys():
            for path in Path(pecha.layer_path/base_name).iterdir():
                if path.stem in annotation_names:
                    layer_paths.append("/".join(path._tail[-2:]))
        return layer_paths

    def serialize(self, pecha: Pecha, manifestation_info: dict = None):
        """
        Get annotations for a single or list of layer paths.
        Each layer_path is a string like: "B5FE/segmentation-4FD1.json"
        """
        
        layer_paths = self.get_layer_paths(pecha, manifestation_info["annotations"])

        annotations = {}
        for layer_path in layer_paths:
            ann_store = AnnotationStore(file=str(pecha.layer_path / layer_path))
            ann_type = self._get_ann_type(layer_path)
            anns = self.to_dict(ann_store, ann_type)
            annotations[ann_type.value] = anns

        base = self.get_base(pecha)
        return {"base": base, "annotations": annotations}

    def serialize_edition_annotations(
        self, pecha: Pecha, edition_layer_path: str, layer_path: str
    ):
        """
        Get annotations for a single or list of edition layer paths.
        Edition annotations are annotations done on top of edition base rather than the base.
        """
        edition_base = self.get_edition_base(pecha, edition_layer_path)
        edition_basename = Path(edition_layer_path).stem
        output_path = str(Path(tempfile.mkdtemp()) / pecha.id)

        shutil.copytree(pecha.pecha_path.as_posix(), output_path)
        Path(f"{output_path}/base/{edition_basename}.txt").write_text(
            edition_base, encoding="utf-8"
        )
        temp_pecha = pecha.from_path(Path(output_path))

        serialized = self.serialize(temp_pecha, layer_path)
        return serialized
