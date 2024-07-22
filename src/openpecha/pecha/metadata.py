from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Extra, root_validator


class MetaData(BaseModel):
    id_: str
    title: List[str]
    author: List[str]
    created_at: datetime
    source: str
    source_metadata: Dict[str, str]

    class Config:
        extra = Extra.allow

    @root_validator(pre=True)
    def set_created_at(cls, values):
        if "created_at" not in values or values["created_at"] is None:
            values["created_at"] = datetime.now()
        return values

    def to_serializable_dict(self):
        data = self.model_dump()
        if isinstance(data["created_at"], datetime):
            data["created_at"] = data["created_at"].isoformat()
        return data
