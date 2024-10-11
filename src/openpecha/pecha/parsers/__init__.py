from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union

from openpecha.config import PECHAS_PATH


class BaseParser(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def parse(
        self,
        input: Any,
        metadata: Union[Dict, Path],
        output_path: Path = PECHAS_PATH,
    ):
        pass
