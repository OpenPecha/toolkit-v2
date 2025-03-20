"""Module contains all the Annotations classes
"""

from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Span(BaseModel):
    start: int = Field(..., ge=0)
    end: int = Field(..., ge=0)
    errors: Optional[Dict] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("start", "end")
    @classmethod
    def span_must_not_be_neg(cls, v: int) -> int:
        if v < 0:
            raise ValueError("span shouldn't be negative")
        return v

    @model_validator(mode="after")
    def end_must_not_be_less_than_start(self) -> "Span":
        if self.end < self.start:
            raise ValueError("Span end must not be less than start")
        return self


class AnnBase(BaseModel):
    span: Span
    metadata: Optional[Dict] = Field(default=None)

    model_config = ConfigDict(extra="forbid")


class Page(AnnBase):
    page_info: Optional[str] = Field(default=None, description="page payload")
    imgnum: Optional[int] = Field(
        default=None,
        description="image sequence no. from bdrc api, http://iiifpres.bdrc.io/il/v:bdr:I0888",
    )
    reference: Optional[str] = Field(
        default=None, description="image filename from bdrc"
    )


class BaseAnnotation(BaseModel):
    span: Span
    metadata: Optional[Dict] = None

    model_config = ConfigDict(extra="forbid")


class Pagination(BaseAnnotation):
    page_info: Optional[str] = Field(default=None, description="page payload")
    imgnum: Optional[int] = Field(default=None, description="image sequence number")
    order: Optional[int] = Field(default=None, description="order of the page")
    reference: Optional[str] = Field(
        default=None, description="can be url or just string indentifier of source page"
    )


class Lang(BaseAnnotation):
    language: Optional[str] = Field(
        default=None, description="BCP-47 tag of the language"
    )


class OCRConfidence(BaseAnnotation):
    confidence: float
    nb_below_threshold: Optional[int] = None


class Citation(BaseAnnotation):
    pass
