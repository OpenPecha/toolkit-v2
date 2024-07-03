from enum import Enum

from pydantic import BaseModel, Field

from openpecha.ids import get_uuid


class LayerEnum(Enum):
    segment = "Segment"
    commentaries = "Commentaries"


class Layer(BaseModel):
    id: str = Field(default_factory=get_uuid)
    annotation_type: LayerEnum
    annotations: dict = Field(default_factory=dict)
