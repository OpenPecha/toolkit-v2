from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


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
