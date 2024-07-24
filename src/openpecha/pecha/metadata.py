import json
import re
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator


class PechaMetaData(BaseModel):
    id_: str
    title: List[str]
    author: List[str]
    created_at: datetime
    source: str
    source_metadata: Dict[str, str]
    type: str
    language: str

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
            f"Source Metadata: {json.dumps(self.source_metadata, indent=4)}\n"
            f"Type: {self.type}\n"
            f"Language: {self.language}"
        )
        return formatted_text

    @classmethod
    def from_text(cls, text: str) -> Optional["PechaMetaData"]:
        """
        Parse metadata from a given formatted text string and create a PechaMetaData instance.

        Parameters:
        text (str): The formatted text string containing metadata.

        Returns:
        Optional[PechaMetaData]: An instance of the PechaMetaData class or None if parsing fails.
        """
        id_match = re.search(r"ID: (.+)", text)
        title_match = re.search(r"Title: ([^/\n]+)", text)
        author_match = re.search(r"Author: (.+)", text)
        created_at_match = re.search(r"Created At: ([^\n]+)\n", text)
        source_match = re.search(r"Source: (.+)", text)
        source_metadata_match = re.search(r"Source Metadata: (.+)", text)
        type_match = re.search(r"Type: (.+)", text)
        language_match = re.search(r"Language: (.+)", text)

        if not (
            id_match
            and title_match
            and author_match
            and created_at_match
            and source_match
            and source_metadata_match
            and type_match
            and language_match
        ):
            return None

        id_ = id_match.group(1)
        title = title_match.group(1).split(", ")
        author = author_match.group(1).split(", ")
        created_at_str = created_at_match.group(1)
        created_at = datetime.fromisoformat(created_at_str)
        source = source_match.group(1)
        source_metadata_str = source_metadata_match.group(1)
        source_metadata = json.loads(source_metadata_str)
        type_ = type_match.group(1)
        language = language_match.group(1)

        return cls(
            id_=id_,
            title=title,
            author=author,
            created_at=created_at,
            source=source,
            source_metadata=source_metadata,
            type=type_,
            language=language,
        )
