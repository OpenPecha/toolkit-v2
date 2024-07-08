from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from openpecha.ids import get_initial_pecha_id


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

    @field_validator("created_at", mode="before")
    def set_imported_date(cls, v):
        return v or datetime.now()


class InitialPechaMetadata(PechaMetadata):
    @model_validator(mode="before")
    @classmethod
    def set_id(cls, values):
        if "id_" not in values or values["id_"] is None:
            values["id_"] = get_initial_pecha_id()
        return values


class OpenPechaMetadata(PechaMetadata):
    @model_validator(mode="before")
    @classmethod
    def set_id(cls, values):
        if "id_" not in values or values["id_"] is None:
            values["id_"] = get_initial_pecha_id()
        return values


class DiplomaticPechaMetadata(PechaMetadata):
    @model_validator(mode="before")
    @classmethod
    def set_id(cls, values):
        if "id_" not in values or values["id_"] is None:
            values["id_"] = get_initial_pecha_id()
        return values
