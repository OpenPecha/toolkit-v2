from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field

from openpecha.ids import get_uuid
from openpecha.pecha.annotation import Annotation


class LayerEnum(Enum):
    segment = "Segment"
    commentaries = "Commentaries"


class Layer(BaseModel):
    id_: str = Field(default_factory=get_uuid)
    annotation_type: LayerEnum
    annotations: Dict[str, Annotation] = Field(default_factory=dict)
