from enum import Enum
from typing import Dict

from openpecha.pecha.annotation import Annotation


class LayerEnum(Enum):
    segment = "Segment"
    commentaries = "Commentaries"


class Layer:
    def __init__(self, annotation_label: LayerEnum, annotations: Dict[str, Annotation]):
        self.annotation_label = annotation_label
        self.annotations = annotations
