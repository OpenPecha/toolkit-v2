from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Tuple

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha, annotation_path
from openpecha.pecha.layer import AnnotationType


class DocxBaseParser(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def parse(
        self,
        input: str | Path,
        annotation_type: AnnotationType,
        metadata: Dict,
        output_path: Path = PECHAS_PATH,
    ) -> Tuple[Pecha, annotation_path]:
        raise NotImplementedError


class BaseParser(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def parse(
        self,
        input: Any,
        metadata: Dict,
        output_path: Path = PECHAS_PATH,
    ):
        raise NotImplementedError


class OCRBaseParser(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def parse(
        self,
        dataprovider: Any,
    ) -> Pecha:
        raise NotImplementedError


class DummyParser(BaseParser):
    @property
    def name(self):
        return self.__class__.__name__

    def parse(
        self,
        input: Any,
        metadata: Dict,
        output_path: Path = PECHAS_PATH,
    ) -> Pecha:
        raise NotImplementedError
