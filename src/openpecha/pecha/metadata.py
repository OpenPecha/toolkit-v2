import json
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
    title: List[str] = Field(default=list, alias="title")
    author: List[str] = Field(default=list, alias="author")
    source: str = Field(default=None, alias="source")
    language: str = Field(default=None, alias="language")
    initial_creation_type: InitialCreationType = Field(
        None, alias="initial_creation_type"
    )
    created_at: Optional[datetime] = Field(default=None, alias="created_at")
    source_metadata: Optional[Dict] = Field(
        default=dict
    )  # place to dump any metadata from the source

    @field_validator("created_at", mode="before")
    def set_imported_date(cls, v):
        return v or datetime.now()

    class Config:
        json_encoders = {
            InitialCreationType: lambda v: v.value,
            defaultdict: lambda d: dict(d),
        }


def to_json_serializable(pecha_metadata: Optional[PechaMetadata]) -> str:
    if pecha_metadata is None:
        return json.dumps({}, indent=4, ensure_ascii=False)

    dict_data = pecha_metadata.model_dump()
    if dict_data["initial_creation_type"] is not None:
        dict_data["initial_creation_type"] = dict_data["initial_creation_type"].value
    for k, v in dict_data.items():
        if v is list:
            dict_data[k] = []
            continue
        if v is dict:
            dict_data[k] = {}
    return json.dumps(dict_data, indent=4, ensure_ascii=False)


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
