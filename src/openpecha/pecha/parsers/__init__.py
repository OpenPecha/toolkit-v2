from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field, validator

from openpecha.config import PECHAS_PATH


class BaseParser(ABC):
    def __init__(self, text: str):
        self.text = text

    @abstractmethod
    def parse(self, output_path: Path):
        pass


class Document(BaseModel):
    text: str = Field(default="")
    annotations: Dict[str, list] = Field(default_factory=dict)
    resources: Dict[str, str] = Field(default_factory=dict)
    resource_ann_mapping: List = Field(default_factory=list)

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
