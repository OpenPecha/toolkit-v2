from typing import Any, Dict, List, Union

from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer


class Serializer:
    def is_commentary_pecha(self, metadatas: List[Dict]) -> bool:
        """
        Pecha can be i) Root Pecha ii) Commentary Pecha
        Output: True if Commentary Pecha, False otherwise
        """
        for metadata in metadatas:
            if "commentary_of" in metadata and metadata["commentary_of"]:
                return True
        return False

    def is_translation_pecha(self, metadatas: List[Dict]) -> bool:
        """
        Return
            True if i) Translation of Root Pecha ii) Translation of Commentary Pecha
            False otherwise
        """
        if "translation_of" in metadatas[0] and metadatas[0]["translation_of"]:
            return True
        return False

    def get_root_en_title(self, metadatas: List[Dict]):
        """
        Commentary Pecha serialized JSON should have the root english title
        """
        root_title = metadatas[-1].get("title", {}).get("en")
        return root_title

    def get_pecha_for_serialization(self, pechas: List[Pecha]) -> Pecha:
        return pechas[0]

    def get_root_pecha(self, pechas: List[Pecha]) -> Pecha:
        return pechas[-1]

    def serialize(
        self,
        pechas: List[Pecha],
        metadatas: List[Dict[str, Any]],
        alignment_data: Union[Dict, None],
    ) -> Dict[str, Any]:

        pecha = self.get_pecha_for_serialization(pechas)
        is_commentary = self.is_commentary_pecha(metadatas)
        is_translation = self.is_translation_pecha(metadatas)
        if is_commentary:
            if is_translation:
                root_pecha = self.get_root_pecha(pechas)
                root_title = self.get_root_en_title(metadatas)
                return SimpleCommentarySerializer().serialize(
                    pecha, alignment_data, root_title, root_pecha  # type: ignore
                )
            else:
                return SimpleCommentarySerializer().serialize(pecha, alignment_data)  # type: ignore
        else:
            if is_translation:
                root_pecha = self.get_root_pecha(pechas)
                return TranslationSerializer().serialize(
                    pecha, alignment_data, root_pecha
                )
            else:
                return TranslationSerializer().serialize(pecha, alignment_data)
