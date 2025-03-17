import json
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from openpecha.ids import get_uuid
from openpecha.pecha.metadata import PechaMetaData

from openpecha.pecha.annotations import *


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    translation = "Translation"
    root_commentory = "Root_Commentary"
    metadata = "Meta_Data"
    structure_annotation = "Structure_Annotation"
    variation_annotation = "Variation_Annotation"
    ocr_annotation = "Ocr_Annotation"
    language_annotation = "language_Annotation"


class LayerEnum(Enum):
    # Existing v2 segments
    meaning_segment = "Meaning_Segment"
    root_segment = "Root_Segment"
    commentary_segment = "Commentary_Segment"
    tibetan_segment = "Tibetan_Segment"
    english_segment = "English_Segment"
    chinese_segment = "Chinese_Segment"
    sanskrit_segment = "Sanskrit_Segment"
    italian_segment = "Italian_Segment"
    russian_segment = "Russian_Segment"
    pecha_display_alignment_segment = "Pecha_Display_Alignment_Segment"

    # Common attributes (keeping v2 naming)
    chapter = "Chapter"
    sapche = "Sapche"  # Note: v1 had "Sabche"
    metadata = "Meta_Data"
    tsawa = "Tsawa"
    pagination = "Pagination"
    durchen = "Durchen"
    ocr_confidence = "OCRConfidence"
    language = "Language"

    # Additional attributes from v1
    index = "index"
    book_title = "BookTitle"
    sub_title = "SubTitle"
    book_number = "BookNumber"
    poti_title = "PotiTitle"
    author = "Author"
    topic = "Text"
    sub_topic = "SubText"
    citation = "Citation"
    correction = "Correction"
    error_candidate = "ErrorCandidate"
    peydurma = "Peydurma"
    pedurma_note = "PedurmaNote"
    yigchung = "Yigchung"
    archaic = "Archaic"
    footnote = "Footnote"
    segment = "Segment"
    transcription_time_span = "TranscriptionTimeSpan"


class LayerGroupEnum(Enum):
    structure_type = "Structure_Type"
    translation_segment = "Translation_Segment"
    associated_alignment = "Associated_Alignment"
    spelling_variation = "Spelling_Variation"
    ocr_confidence_type = "Ocr_Type"
    language_type = "Language_Type"


def get_layer_group(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type in [
        LayerEnum.tibetan_segment,
        LayerEnum.english_segment,
        LayerEnum.chinese_segment,
        LayerEnum.sanskrit_segment,
        LayerEnum.italian_segment,
        LayerEnum.russian_segment,
        LayerEnum.pecha_display_alignment_segment,
    ]:
        return LayerGroupEnum.translation_segment

    if layer_type in [LayerEnum.root_segment, LayerEnum.commentary_segment]:
        return LayerGroupEnum.associated_alignment

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.tsawa,
        LayerEnum.meaning_segment,
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
    if layer_type in [
        LayerEnum.tibetan_segment,
        LayerEnum.english_segment,
        LayerEnum.chinese_segment,
        LayerEnum.sanskrit_segment,
        LayerEnum.italian_segment,
        LayerEnum.russian_segment,
        LayerEnum.pecha_display_alignment_segment,
    ]:
        return LayerCollectionEnum.translation

    if layer_type == LayerEnum.metadata:
        return LayerCollectionEnum.metadata

    if layer_type in [LayerEnum.root_segment, LayerEnum.commentary_segment]:
        return LayerCollectionEnum.root_commentory

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.tsawa,
        LayerEnum.meaning_segment,
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
