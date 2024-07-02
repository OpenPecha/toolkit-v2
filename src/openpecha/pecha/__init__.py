from typing import Dict

from stam import AnnotationStore, Offset, Selector

from openpecha.ids import get_uuid
from openpecha.pecha.annotation import Annotation


class Pecha:
    def __init__(
        self, pecha_id: str, segments: Dict[str, str], metadata: Dict[str, str]
    ) -> None:
        self.pecha_id = pecha_id
        self.segments = segments
        self.metadata = metadata
        self.base_text = "".join(segments.values())
        self.annotations = self.set_annotations()
        self.write_annotations()

    @classmethod
    def from_path(cls, path: str):
        pass

    @classmethod
    def from_id(cls, pecha_id: str):
        pass

    def set_annotations(self):
        char_count = 0
        for segment_id, segment in self.segments.items():
            annotation = Annotation(
                id_=segment_id,
                segment=segment,
                start=char_count,
                end=char_count + len(segment),
            )
            char_count += len(segment)
            yield annotation

    def write_annotations(self):
        """write annotations in stam data model"""
        self.annotation_store = AnnotationStore(id="PechaAnnotationStore")
        self.resource = self.annotation_store.add_resource(
            id=self.pecha_id, filename="random file path"
        )  # in case of having layers, resource_id will be pecha_id_layer_id
        self.dataset = self.annotation_store.add_dataset(id="PechaDataSet")
        self.dataset.add_key(self.metadata["annotation_category"])
        for annotation in self.annotations:
            target = Selector.textselector(
                self.resource,
                Offset.simple(annotation.start, annotation.end),
            )
            data = [
                {
                    "id": annotation.id_,
                    "key": self.metadata["annotation_category"],
                    "value": self.metadata["annotation_label"],
                    "set": self.dataset.id(),
                }
            ]
            self.annotation_store.add_annotation(
                id=annotation.id_,
                target=target,
                data=data,
            )
