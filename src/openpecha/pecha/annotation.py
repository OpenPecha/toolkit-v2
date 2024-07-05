from pydantic import BaseModel, Field, ValidationInfo, field_validator


class Annotation(BaseModel):
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    metadata: dict = Field(default_factory=dict)

    @field_validator("end")
    @classmethod
    def end_must_not_be_less_than_start(cls, v: int, values: ValidationInfo) -> int:
        if "start" in values.data and v < values.data["start"]:
            raise ValueError("Span end must not be less than start")
        return v
