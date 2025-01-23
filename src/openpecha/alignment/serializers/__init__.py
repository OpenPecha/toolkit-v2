from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

from openpecha.pecha import Pecha


class BaseAlignmentSerializer(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def serialize(
        self,
        root_pecha: Pecha,
        translation_pecha: Pecha,
    ) -> Dict:
        pass
