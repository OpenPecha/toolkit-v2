from enum import Enum
from typing import Any, Dict, List

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError, MetaDataValidationError
from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary import (
    PreAlignedCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.prealigned_root_translation import (
    PreAlignedRootTranslationSerializer,
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

    prealigned_root_translation_pecha = "prealigned_root_translation_pecha"

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
            if has_version_of(metadatas):
                return PechaType.prealigned_root_translation_pecha
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
        root_metadata = metadatas[-1]
        root_pecha = pechas[-1]

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

    def serialize(
        self,
        pechas: List[Pecha],
        metadatas: List[Dict[str, Any]],
        pecha_category: Dict[str, List[Dict[str, str]]],
    ):
        """
        Serialize a Pecha based on its type.
        """
        pecha = pechas[0]

        pecha_type = get_pecha_type(metadatas)
        logger.info(f"Serializing Pecha {pecha.id}, Type: {pecha_type}")

        match pecha_type:
            case PechaType.root_pecha:
                return RootSerializer().serialize(pecha, pecha_category)

            case PechaType.root_translation_pecha:
                root_pecha = pechas[-1]
                return RootSerializer().serialize(pecha, pecha_category, root_pecha)

            case PechaType.commentary_pecha:
                root_en_title = self.get_root_en_title(metadatas, pechas)
                return SimpleCommentarySerializer().serialize(pecha, root_en_title)

            case PechaType.commentary_translation_pecha:
                root_en_title = self.get_root_en_title(metadatas, pechas)
                commentary_pecha = pechas[1]
                return SimpleCommentarySerializer().serialize(
                    pecha, root_en_title, commentary_pecha
                )

            case PechaType.prealigned_commentary_pecha:
                root_display_pecha = pechas[2]
                root_pecha = pechas[1]
                commentary_pecha = pechas[0]
                return PreAlignedCommentarySerializer().serialize(
                    root_display_pecha, root_pecha, commentary_pecha
                )

            case PechaType.prealigned_root_translation_pecha:
                root_display_pecha = pechas[2]
                root_pecha = pechas[1]
                translation_pecha = pechas[0]
                return PreAlignedRootTranslationSerializer().serialize(
                    root_display_pecha, root_pecha, translation_pecha
                )

            case PechaType.prealigned_commentary_translation_pecha:
                root_display_pecha = pechas[3]
                root_pecha = pechas[2]
                commentary_pecha = pechas[1]
                translation_pecha = pechas[0]
                return PreAlignedCommentarySerializer().serialize(
                    root_display_pecha, root_pecha, commentary_pecha
                )

            case _:
                raise ValueError(f"Unsupported pecha type: {pecha_type}")
