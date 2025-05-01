from enum import Enum
from typing import Any, Dict, List, Optional

from openpecha.config import get_logger
from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnBase
from openpecha.pecha.serializers.pecha_tools.translation_editor import (
    TranslationSerializer,
)

logger = get_logger(__name__)


class EditorType(Enum):
    """
    Editor Type for Serializer to determine the type of Pecha.
    """

    TRANSLATION = "translation"
    COMMENTARY = "commentary"
    CHAPTER = "chapter"
    SEGMENTATION = "segmentation"


class TranslationEditor:
    metadata: Dict = {}
    base_text: str = ""
    annotations: Optional[AnnBase] = None


class Serializer:
    def serialize(
        self,
        pechas: List[Pecha],
        metadatas: List[Dict[str, Any]],
        pecha_category: List[Dict],
        editor_type: str,
        layer_name: Optional[str] = None,
    ):
        """
        Serialize a Pecha based on its type.
        """
        logger.info(f"Serializing Pecha {pechas[0].id}, Editor Type: {editor_type}")

        match editor_type:
            case EditorType.TRANSLATION.value:
                return TranslationSerializer().serialize(
                    pechas, metadatas, pecha_category, layer_name
                )

            case _:
                raise ValueError(f"Unsupported pecha type: {editor_type}")
