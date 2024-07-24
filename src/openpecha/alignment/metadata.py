from enum import Enum
from typing import Dict

from pydantic import BaseModel, model_validator

from openpecha.ids import get_alignment_id
from openpecha.pecha.layer import LayerEnum


class AlignmentRelationEnum(Enum):
    source = "Source"
    target = "Target"


class AlignmentTypeEnum(Enum):
    translation = "Translation"
    root_commentory = "Root_Commentary"


class LanguageEnum(Enum):
    tibetan = "Tibetan"
    english = "English"
    chinese = "Chinese"
    sanskrit = "Sanskrit"


class SegmentMetaData(BaseModel):
    type: LayerEnum
    relation: AlignmentRelationEnum
    lang: LanguageEnum
    base: str

    def to_dict(self) -> Dict:
        """
        Convert the SegmentMetaData instance to a dictionary,
        converting enum attributes to their values.
        """
        return {
            "type": self.type.value,
            "relation": self.relation.value,
            "lang": self.lang.value,
            "base": self.base,
        }


class AlignmentMetaData(BaseModel):
    id_: str
    segments_metadata: Dict[str, SegmentMetaData]

    @classmethod
    def from_dict(cls, metadata: Dict) -> "AlignmentMetaData":
        segments_metadata: Dict[str, SegmentMetaData] = {}
        for segment_source_id, segment_metadata in metadata.items():
            type = LayerEnum(segment_metadata["type"])
            relation = AlignmentRelationEnum(segment_metadata["relation"])
            lang = LanguageEnum(segment_metadata["lang"])
            base = segment_metadata["base"]

            segments_metadata[segment_source_id] = SegmentMetaData(
                type=type, relation=relation, lang=lang, base=base
            )

        return cls(segments_metadata=segments_metadata)

    @model_validator(mode="before")
    @classmethod
    def set_id(cls, values):
        if "id_" not in values or values["id_"] is None:
            values["id_"] = get_alignment_id()
        return values

    def to_dict(self) -> Dict:
        """
        Convert the AlignmentMetaData instance to a dictionary,
        converting enum attributes to their values.
        """
        return {
            "id_": self.id_,
            "segments_metadata": {
                segment_id: segment.to_dict()
                for segment_id, segment in self.segments_metadata.items()
            },
        }
