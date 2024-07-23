import json
import re
from datetime import datetime
from typing import Dict, List, Optional

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
            f"Source Metadata: {json.dumps(self.source_metadata, indent=4)}"
        )
        return formatted_text


def parse_metadata_from_text(text: str) -> Optional[MetaData]:
    """
    Parse metadata from a given formatted text string and create a MetaData instance.

    Parameters:
    text (str): The formatted text string containing metadata.

    Returns:
    Optional[MetaData]: An instance of the MetaData class or None if parsing fails.
    """
    id_match = re.search(r"ID: (.+)", text)
    title_match = re.search(r"Title: ([^/\n]+)", text)
    author_match = re.search(r"Author: (.+)", text)
    created_at_match = re.search(r"Created At: ([^\n]+)\n", text)
    source_match = re.search(r"Source: (.+)", text)
    source_metadata_match = re.search(r"Source Metadata: (.+)", text)

    if not (
        id_match
        and title_match
        and author_match
        and created_at_match
        and source_match
        and source_metadata_match
    ):
        return None  # Return None if any of the required metadata is missing

    id_ = id_match.group(1)
    title = title_match.group(1).split(", ")
    author = author_match.group(1).split(", ")
    created_at_str = created_at_match.group(1)
    created_at = datetime.fromisoformat(created_at_str)
    source = source_match.group(1)
    source_metadata_str = source_metadata_match.group(1)
    source_metadata = json.loads(source_metadata_str)

    metadata = MetaData(
        id_=id_,
        title=title,
        author=author,
        created_at=created_at,
        source=source,
        source_metadata=source_metadata,
    )
    return metadata
