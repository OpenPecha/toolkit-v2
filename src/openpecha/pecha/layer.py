import json
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from openpecha.ids import get_uuid
from openpecha.pecha.annotations import (
    BaseAnnotation,
    Citation,
    Lang,
    OCRConfidence,
    Pagination,
)
from openpecha.pecha.metadata import PechaMetaData


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    structure_annotation = "Structure_Annotation"
    variation_annotation = "Variation_Annotation"
    ocr_annotation = "Ocr_Annotation"
    language_annotation = "language_Annotation"
    segmentation_annotation = "Segmentation_Annotation"


class LayerEnum(Enum):
    segmentation = "Segmentation"
    alignment = "Alignment"

    chapter = "Chapter"
    pagination = "Pagination"
    durchen = "Durchen"
    sapche = "Sapche"

    ocr_confidence = "OCRConfidence"
    language = "Language"
    citation = "Citation"
    book_title = "BookTitle"


class LayerGroupEnum(Enum):
    structure_type = "Structure_Type"
    spelling_variation = "Spelling_Variation"
    ocr_confidence_type = "Ocr_Type"
    language_type = "Language_Type"
    segmentation_type = "Segmentation_Type"


def get_layer_group(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""

    if layer_type in [LayerEnum.segmentation, LayerEnum.alignment]:
        return LayerGroupEnum.segmentation_type

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.pagination,
    ]:
        return LayerGroupEnum.structure_type

    if layer_type == LayerEnum.language:
        return LayerGroupEnum.language_type

    if layer_type == LayerEnum.ocr_confidence:
        return LayerGroupEnum.ocr_confidence_type

    if layer_type == LayerEnum.durchen:
        return LayerGroupEnum.spelling_variation

    raise ValueError(f"Layer type {layer_type} has no defined LayerGroupEnum")


def get_layer_collection(layer_type: LayerEnum) -> LayerCollectionEnum:
    """return the annotation category where annotation type falls in"""

    if layer_type in [LayerEnum.segmentation, LayerEnum.alignment]:
        return LayerCollectionEnum.segmentation_annotation

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.pagination,
    ]:
        return LayerCollectionEnum.structure_annotation

    if layer_type == LayerEnum.language:
        return LayerCollectionEnum.language_annotation

    if layer_type == LayerEnum.ocr_confidence:
        return LayerCollectionEnum.ocr_annotation

    if layer_type == LayerEnum.durchen:
        return LayerCollectionEnum.variation_annotation

    raise ValueError(f"Layer type {layer_type} has no defined LayerCollectionEnum")


def _get_annotation_class(layer_name: LayerEnum):
    """Maps LayerEnum to Annotation class"""

    if layer_name == LayerEnum.pagination:
        return Pagination
    elif layer_name == LayerEnum.language:
        return Lang
    elif layer_name == LayerEnum.citation:
        return Citation
    elif layer_name == LayerEnum.ocr_confidence:
        return OCRConfidence
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
        self.revision = f"{int(self.revision)+1:05}"  # noqa

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
            return None
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
