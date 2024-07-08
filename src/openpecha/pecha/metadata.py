from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from openpecha.ids import get_diplomatic_id, get_initial_pecha_id, get_open_pecha_id


class InitialCreationType(Enum):
    ocr = "ocr"
    ebook = "ebook"
    input = "input"
    tmx = "tmx"


class PechaMetadata(BaseModel):
    id_: str = Field(default=None, alias="id_")
    title: List[str] = Field(default=None, alias="title")
    author: List[str] = Field(default=None, alias="author")
    source: str = Field(default=None, alias="source")
    language: str = Field(default=None, alias="language")
    initial_creation_type: InitialCreationType = Field(
        None, alias="initial_creation_type"
    )
    created_at: datetime = Field(default=datetime.now, alias="created_at")
    source_metadata: Optional[Dict] = Field(
        default=defaultdict
    )  # place to dump any metadata from the source

    @field_validator("created_at", pre=True, always=True)
    def set_imported_date(cls, v):
        return v or datetime.now()


class InitialPechaMetadata(PechaMetadata):
    @field_validator("id_", pre=True, always=True)
    def set_id(cls, v):
        return v or get_initial_pecha_id()


class OpenPechaMetadata(PechaMetadata):
    @field_validator("id_", pre=True, always=True)
    def set_id(cls, v):
        return v or get_open_pecha_id()


class DiplomaticPechaMetadata(PechaMetadata):
    @field_validator("id_", pre=True, always=True)
    def set_id(cls, v):
        return v or get_diplomatic_id()
