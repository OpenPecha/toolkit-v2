from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union

from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH
from openpecha.pecha import Pecha


class BaseAlignmentSerializer(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def serialize(
        self,
        root_opf: Path,
        translation_opf: Path,
    ) -> Dict:
        pass
