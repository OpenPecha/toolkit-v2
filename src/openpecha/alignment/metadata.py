from enum import Enum
from typing import Dict

from pydantic import BaseModel


class AlignmentRelationEnum(Enum):
    source = "Source"
    target = "Target"


class AlignmentTypeEnum(Enum):
    translation = "Translation"
    root_commentory = "Root_Commentary"


class LanguageEnum(Enum):
    tibetan = "tibetan"
    english = "english"
    chinese = "chinese"
    sanskrit = "sanskrit"


class SegmentMetaData(BaseModel):
    type: AlignmentTypeEnum
    relation: AlignmentRelationEnum
    lang: LanguageEnum
    base: str


class AlignmentMetaData(BaseModel):
    segments_metadata: Dict[str, SegmentMetaData]
