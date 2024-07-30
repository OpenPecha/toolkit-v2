from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, model_validator


class PechaMetaData(BaseModel):
    id_: str
    title: List[str]
    author: List[str]
    created_at: datetime
    source: str
    source_metadata: Dict[str, str]
    type: str
    language: str

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    def set_created_at(cls, values):
        if "created_at" not in values or values["created_at"] is None:
            values["created_at"] = datetime.now()
        return values
