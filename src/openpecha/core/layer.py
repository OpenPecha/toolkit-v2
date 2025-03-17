import json
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from openpecha.core.annotations import *
from openpecha.ids import get_uuid
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import PechaMetaData


def _get_annotation_class(layer_name: LayerEnum):
    """Maps LayerEnum to Annotation class"""
    if layer_name == LayerEnum.book_title:
        return BaseAnnotation
    elif layer_name == LayerEnum.sub_title:
        return BaseAnnotation
    elif layer_name == LayerEnum.book_number:
        return BaseAnnotation
    elif layer_name == LayerEnum.poti_title:
        return BaseAnnotation
    elif layer_name == LayerEnum.author:
        return BaseAnnotation
    elif layer_name == LayerEnum.chapter:
        return BaseAnnotation
    elif layer_name == LayerEnum.topic:
        return BaseAnnotation
    elif layer_name == LayerEnum.sub_topic:
        return BaseAnnotation
    elif layer_name == LayerEnum.pagination:
        return Pagination
    elif layer_name == LayerEnum.language:
        return Lang
    elif layer_name == LayerEnum.citation:
        return Citation
    elif layer_name == LayerEnum.correction:
        return Correction
    elif layer_name == LayerEnum.error_candidate:
        return ErrorCandidate
    elif layer_name == LayerEnum.peydurma:
        return Pedurma
    elif layer_name == LayerEnum.sapche:
        return Sapche
    elif layer_name == LayerEnum.tsawa:
        return Tsawa
    elif layer_name == LayerEnum.yigchung:
        return Yigchung
    elif layer_name == LayerEnum.archaic:
        return Archaic
    elif layer_name == LayerEnum.durchen:
        return Durchen
    elif layer_name == LayerEnum.footnote:
        return Footnote
    elif layer_name == LayerEnum.segment:
        return Segment
    elif layer_name == LayerEnum.ocr_confidence:
        return OCRConfidence
    elif layer_name == LayerEnum.transcription_time_span:
        return TranscriptionTimeSpan
    else:
        return BaseAnnotation


class Layer(BaseModel):
    id: str = Field(default=None)
    annotation_type: LayerEnum
    revision: str = Field(default="00001")
    annotations: Dict = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    def set_id(cls, values):
        values["id"] = values.get("id") or get_uuid()
        return values

    @field_validator("revision")
    def revision_must_int_parsible(cls, v):
        assert v.isdigit(), "must integer parsible like `00002`"
        return v

    def bump_revision(self):
        self.revision = f"{int(self.revision)+1:05}"

    def reset(self):
        self.revision = "00001"
        self.annotations = {}

    def get_annotations(self):
        """Yield Annotation Objects"""
        for ann_id, ann_dict in self.annotations.items():
            ann_class = _get_annotation_class(self.annotation_type)
            ann = ann_class.model_validate(ann_dict)
            yield ann_id, ann

    def get_annotation(self, annotation_id: str) -> Optional[BaseAnnotation]:
        """Retrieve annotation of id `annotation_id`"""
        ann_dict = self.annotations.get(annotation_id)
        if not ann_dict:
            return
        ann_class = _get_annotation_class(self.annotation_type)
        ann = ann_class.model_validate(ann_dict)
        return ann

    def set_annotation(self, ann: BaseAnnotation, ann_id=None):
        """Add or Update annotation `ann` to the layer, returns the annotation id"""
        ann_id = ann_id if ann_id is not None else get_uuid()
        self.annotations[ann_id] = json.loads(ann.model_dump_json())
        return ann_id

    def remove_annotation(self, annotation_id: str):
        """Delete annotaiton of `annotation_id` from the layer"""
        if annotation_id in self.annotations:
            del self.annotations[annotation_id]


class SpanINFO(BaseModel):
    text: str
    layers: Dict[LayerEnum, List[BaseAnnotation]]
    metadata: PechaMetaData

    model_config = ConfigDict(arbitrary_types_allowed=True)


class OCRConfidenceLayer(Layer):
    confidence_threshold: float
    annotation_type: LayerEnum = Field(default=LayerEnum.ocr_confidence)


class TranscriptionTimeSpanLayer(Layer):
    media_url: str
    time_unit: str
    annotation_type: LayerEnum = Field(default=LayerEnum.transcription_time_span)

    @field_validator("time_unit")
    def time_unit_must_be_millisecond_or_microsecond(cls, v):
        if v not in ("millisecond", "microsecond"):
            raise ValueError("time_unit must be either millisecond or microsecond")
        return v
