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

    def to_formatted_text(self):
        formatted_text = (
            f"ID: {self.id_}\n"
            f"Title: {', '.join(self.title)}\n"
            f"Author: {', '.join(self.author)}\n"
            f"Created At: {self.created_at.isoformat()}\n"
            f"Source: {self.source}\n"
            # f"Source Metadata: {json.dumps(self.source_metadata, indent=4)}"
        )
        return formatted_text
