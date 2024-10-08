import json
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


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

    def to_dict(self):
        ann_data = {}
        for ann_metadata, ann_metadata_value in self.model_dump().items():
            if isinstance(ann_metadata_value, list):
                for v in ann_metadata_value:
                    ann_data[ann_metadata] = v

            elif isinstance(ann_metadata_value, dict):
                for k, v in ann_metadata_value.items():
                    ann_data[k] = v

            elif isinstance(ann_metadata_value, str):
                ann_data[ann_metadata] = ann_metadata_value

            elif isinstance(ann_metadata_value, datetime):
                ann_data[ann_metadata] = ann_metadata_value.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            else:
                raise ValueError(
                    "Metadata value should be either a string, list or dictionary."
                )

        return ann_data


class KungsangMonlamMetaData(BaseModel):
    author: Optional[Dict[str, str]] = Field(default_factory=dict)
    composition_date: Optional[Dict[str, str]] = Field(default_factory=dict)
    source: Optional[Dict[str, str]] = Field(default_factory=dict)
    presentation: Optional[Dict[str, str]] = Field(default_factory=dict)
    usage_title: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_short: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_long_clean: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_alt_1: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_alt_2: Optional[Dict[str, str]] = Field(default_factory=dict)
    is_commentary_of: Optional[Dict[str, str]] = Field(default_factory=dict)
    is_version_of: Optional[Dict[str, str]] = Field(default_factory=dict)
    lang: Optional[str] = None

    model_config = ConfigDict(extra="allow")

    def to_pecha_metadata(self, id_: str) -> PechaMetaData:
        """
        Extract relevant fields from KunsangMonlamMetaData and map them to PechaMetaData fields
        """
        title = (
            [json.dumps(self.title_short, ensure_ascii=False)]
            if self.title_short
            else []
        )
        author = [json.dumps(self.author, ensure_ascii=False)] if self.author else []
        source = json.dumps(self.source, ensure_ascii=False) if self.source else ""
        type = "kunsang_monlam"
        language = self.lang if self.lang else ""

        extra_metadata = {
            k: v
            for k, v in self.model_dump().items()
            if k not in ["author", "source", "source", "lang"]
        }

        return PechaMetaData(
            id_=id_,
            title=title,
            author=author,
            source=source,
            source_metadata={},
            type=type,
            language=language,
            **extra_metadata
        )
