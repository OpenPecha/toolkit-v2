from typing import Any, Dict, List, Union

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer


class Serializer:
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

    def get_root_title(self, metadatas: List[Dict]):
        root_title = metadatas[0].get("title", {}).get("en")
        return root_title

    def serialize(
        self,
        pecha: Pecha,
        alignment_data: Dict,
        metadatas: List[Dict[str, Any]],
        root_pecha: Union[Pecha, None] = None,
    ) -> Dict[str, Any]:

        is_commentary = self.is_commentary_pecha(metadatas)
        if is_commentary:
            root_title = self.get_root_title(metadatas)
            return SimpleCommentarySerializer().serialize(
                pecha, alignment_data, root_title, root_pecha
            )
        else:
            return TranslationSerializer().serialize(pecha, alignment_data, root_pecha)
