from enum import Enum
from typing import Any, Dict, List

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError, MetaDataValidationError
from openpecha.pecha import Pecha, get_first_layer_file
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.root import RootSerializer

logger = get_logger(__name__)


class PechaType(Enum):
    """
    Pecha Type for Serializer to determine the type of Pecha.
    """

    root_pecha = "root_pecha"
    root_translation_pecha = "root_translation_pecha"

    commentary_pecha = "commentary_pecha"
    commentary_translation_pecha = "commentary_translation_pecha"

    prealigned_commentary_pecha = "prealigned_commentary_pecha"
    prealigned_commentary_translation_pecha = "prealigned_commentary_translation_pecha"


def get_pecha_type(metadatas: List[Dict]) -> PechaType:
    is_commentary = is_commentary_pecha(metadatas)
    is_translation = is_translation_pecha(metadatas)

    if is_commentary:
        if is_translation:
            if has_version_of(metadatas):
                return PechaType.prealigned_commentary_translation_pecha
            return PechaType.commentary_translation_pecha
        if has_version_of(metadatas):
            return PechaType.prealigned_commentary_pecha

        return PechaType.commentary_pecha
    else:
        if is_translation:
            return PechaType.root_translation_pecha
        return PechaType.root_pecha


def is_commentary_pecha(metadatas: List[Dict]) -> bool:
    """
    Pecha can be i) Root Pecha ii) Commentary Pecha
    Output: True if Commentary Pecha, False otherwise
    """
    for metadata in metadatas:
        if "commentary_of" in metadata and metadata["commentary_of"]:
            return True
    return False


def is_translation_pecha(metadatas: List[Dict]) -> bool:
    """
    Return
        True if i) Translation of Root Pecha ii) Translation of Commentary Pecha
        False otherwise
    """
    if "translation_of" in metadatas[0] and metadatas[0]["translation_of"]:
        return True
    return False


def has_version_of(metadatas: List[Dict]) -> bool:
    """
    Return
        True: if the any pecha has a 'version_of' metadata chain
        False: otherwise
    """
    for metadata in metadatas:
        if "version_of" in metadata and metadata["version_of"]:
            return True
    return False


class Serializer:
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

    def serialize(self, pechas: List[Pecha], metadatas: List[Dict[str, Any]]):
        """
        Serialize a Pecha based on its type.
        """
        pecha = self.get_pecha_for_serialization(pechas)

        pecha_type = get_pecha_type(metadatas)

        if pecha_type == PechaType.commentary_pecha:
            root_en_title = self.get_root_en_title(metadatas, pechas)
            return SimpleCommentarySerializer().serialize(pecha, root_en_title)

        elif pecha_type == PechaType.commentary_translation_pecha:
            root_en_title = self.get_root_en_title(metadatas, pechas)
            commentary_pecha = pechas[1]
            return SimpleCommentarySerializer().serialize(
                pecha, root_en_title, commentary_pecha
            )

        elif pecha_type == PechaType.root_pecha:
            return RootSerializer().serialize(pecha)

        elif pecha_type == PechaType.root_translation_pecha:
            root_pecha = self.get_root_pecha(pechas)
            return RootSerializer().serialize(pecha, root_pecha)
