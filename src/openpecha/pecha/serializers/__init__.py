from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.translation import TextTranslationSerializer


class BaseSerializer(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def serialize(
        self,
        pecha_path: Path,
        source_type: str,
    ):
        pass


class PechaSerializer:
    def is_commentary_pecha(self, metadatas: List[Dict]) -> bool:
        """Checks if the given metadata corresponds to a commentary Pecha.

        Args:
            metadatas (List[Dict]): List of dictionaries containing metadata of the Pecha.

        Returns:
            bool: True if the Pecha is a commentary, otherwise False.
        """
        for metadata in metadatas:
            if "commentary_of" in metadata and metadata["commentary_of"]:
                return True
        return False

    def serialize(
        self, pecha: Pecha, alignment_data: Dict, metadatas: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        is_commentary = self.is_commentary_pecha(metadatas)
        if is_commentary:
            # root_title = self.get_root_title(metadatas)
            root_title = metadatas[0].get("title", {}).get("en", "Untitled")
            return SimpleCommentarySerializer().serialize(pecha, root_title)
        else:
            return TextTranslationSerializer().serialize(pecha, alignment_data)
