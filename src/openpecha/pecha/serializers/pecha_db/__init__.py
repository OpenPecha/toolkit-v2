from typing import Any, Dict, List, Union

from openpecha.config import get_logger
from openpecha.exceptions import (
    AlignmentDataMissingError,
    MetaDataMissingError,
    MetaDataValidationError,
)
from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.translation import TranslationSerializer

logger = get_logger(__name__)


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

    def get_root_en_title(self, metadatas: List[Dict], pechas: List[Pecha]) -> str:
        """
        Commentary Pecha serialized JSON should have the root English title.
        """
        root_metadata = self.get_root_metadata(metadatas)
        root_pecha = self.get_root_pecha(pechas)

        title = root_metadata.get("title")

        if not isinstance(title, dict):
            logger.error(f"Title should be a dictionary in Root Pecha {root_pecha.id}.")
            raise MetaDataValidationError(
                f"Title should be a dictionary in Root Pecha {root_pecha.id}."
            )

        en_title = next((title[key] for key in title if key.lower() == "en"), None)

        if not en_title:
            logger.error(f"English title is missing in Root Pecha {root_pecha.id}.")
            raise MetaDataMissingError(
                f"English title is missing in Root Pecha {root_pecha.id}."
            )

        return en_title

    def get_pecha_for_serialization(self, pechas: List[Pecha]) -> Pecha:
        return pechas[0]

    def get_root_pecha(self, pechas: List[Pecha]) -> Pecha:
        return pechas[-1]

    def get_root_metadata(self, metadatas: List[Dict]) -> Dict:
        return metadatas[-1]

    def serialize(
        self,
        pechas: List[Pecha],
        metadatas: List[Dict[str, Any]],
        alignment_data: Union[Dict, None],
    ) -> Dict[str, Any]:
        """
        Serialize a Pecha based on its type.
        """
        pecha = self.get_pecha_for_serialization(pechas)
        is_commentary = self.is_commentary_pecha(metadatas)
        is_translation = self.is_translation_pecha(metadatas)

        # Commentary Pecha or Translation of Commentary Pecha
        if is_commentary:
            if not alignment_data:
                logger.error(
                    "Alignment data is missing for Commentary Pecha Serialization."
                )
                raise AlignmentDataMissingError(
                    "Alignment data is missing for Commentary Pecha Serialization."
                )
            commentary_serializer = SimpleCommentarySerializer()
            root_en_title = self.get_root_en_title(metadatas, pechas)
            commentary_pecha = pechas[1]
            if is_translation:
                return commentary_serializer.serialize(
                    pecha, alignment_data, root_en_title, commentary_pecha
                )
            return commentary_serializer.serialize(pecha, alignment_data, root_en_title)

        # Root Pecha or Translation of Root Pecha
        root_serializer = TranslationSerializer()
        root_pecha = self.get_root_pecha(pechas) if is_translation else None
        return root_serializer.serialize(pecha, alignment_data, root_pecha)
