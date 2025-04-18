from typing import Any, Dict, List

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError, MetaDataValidationError
from openpecha.pecha import Pecha
from openpecha.pecha.pecha_types import PechaType, get_pecha_type
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
        pecha_category: List[Dict[str, Dict[str, str]]],
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
                return RootSerializer().serialize(
                    root_pecha, pecha_category, pecha
                )

            case PechaType.commentary_pecha:
                root_en_title = self.get_root_en_title(metadatas, pechas)
                return SimpleCommentarySerializer().serialize(
                    pecha, pecha_category, root_en_title
                )

            case PechaType.commentary_translation_pecha:
                root_en_title = self.get_root_en_title(metadatas, pechas)
                commentary_pecha = pechas[1]
                return SimpleCommentarySerializer().serialize(
                    commentary_pecha, pecha_category, root_en_title, pecha
                )

            case PechaType.prealigned_commentary_pecha:
                root_display_pecha = pechas[2]
                root_pecha = pechas[1]
                commentary_pecha = pechas[0]
                return PreAlignedCommentarySerializer().serialize(
                    root_display_pecha,
                    root_pecha,
                    commentary_pecha,
                    pecha_category,
                )

            case PechaType.prealigned_root_translation_pecha:
                root_display_pecha = pechas[2]
                root_pecha = pechas[1]
                translation_pecha = pechas[0]
                return PreAlignedRootTranslationSerializer().serialize(
                    root_display_pecha,
                    root_pecha,
                    translation_pecha,
                    pecha_category,
                )

            case PechaType.prealigned_commentary_translation_pecha:
                root_display_pecha = pechas[3]
                root_pecha = pechas[2]
                commentary_pecha = pechas[1]
                translation_pecha = pechas[0]
                return PreAlignedCommentarySerializer().serialize(
                    root_display_pecha,
                    root_pecha,
                    commentary_pecha,
                    pecha_category,
                )

            case _:
                raise ValueError(f"Unsupported pecha type: {pecha_type}")
