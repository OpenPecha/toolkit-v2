from typing import Any, Dict, List, Optional

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError, MetaDataValidationError
from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel
from openpecha.pecha.pecha_types import PechaType, get_aligned_id, get_pecha_type
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary import (
    PreAlignedCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary_translation import (
    PreAlignedCommentaryTranslationSerializer,
)
from openpecha.pecha.serializers.pecha_db.commentary.simple_commentary import (
    SimpleCommentarySerializer,
)
from openpecha.pecha.serializers.pecha_db.prealigned_root_translation import (
    PreAlignedRootTranslationSerializer,
)
from openpecha.pecha.serializers.pecha_db.root import RootSerializer

logger = get_logger(__name__)


def has_segmentation_annotation(ann_models: List[AnnotationModel]) -> bool:
    for ann_model in ann_models:
        path = ann_model.path
        if path.split("/")[1].startswith("segmentation"):
            return True
    return False


def get_segmentation_id(ann_models: List[AnnotationModel]) -> Optional[str]:
    for ann_model in ann_models:
        path = ann_model.path
        if path.split("/")[1].startswith("segmentation"):
            return path
    return None


# Handler functions for each PechaType
def _serialize_root_pecha(
    pechas, metadatas, annotations, pecha_category, annotation_path
):
    return RootSerializer().serialize(pechas[0], annotation_path, pecha_category)


def _serialize_root_translation_pecha(
    pechas, metadatas, annotations, pecha_category, annotation_path
):
    root_alignment_id = get_aligned_id(annotations[pechas[0].id], annotation_path)
    logger.info(f"Root Alignment ID: {root_alignment_id}")
    return RootSerializer().serialize(
        pechas[1],
        root_alignment_id,
        pecha_category,
        pechas[0],
        annotation_path,
    )


def _serialize_commentary_pecha(
    pechas, metadatas, annotations, pecha_category, annotation_path
):
    root_title = Serializer.get_root_en_title(metadatas, pechas)
    return SimpleCommentarySerializer().serialize(
        pechas[0], annotation_path, pecha_category, root_title
    )


def _serialize_commentary_translation_pecha(
    pechas, metadatas, annotations, pecha_category, annotation_path
):
    root_title = Serializer.get_root_en_title(metadatas, pechas)

    commentary_pecha = pechas[1]
    translation_pecha = pechas[0]

    commentary_alignment_id = get_aligned_id(
        annotations[translation_pecha.id], annotation_path
    )

    return SimpleCommentarySerializer().serialize(
        commentary_pecha,
        commentary_alignment_id,
        pecha_category,
        root_title,
        translation_pecha,
        annotation_path,
    )


def _serialize_prealigned_commentary_pecha(
    pechas, metadatas, annotations, pecha_category, annotation_path
):
    root_pecha = pechas[1]
    commentary_pecha = pechas[0]

    root_alignment_id = get_aligned_id(
        annotations[commentary_pecha.id], annotation_path
    )

    commentary_ann_models = annotations[commentary_pecha.id]
    if has_segmentation_annotation(commentary_ann_models):
        commentary_segmentation_id = get_segmentation_id(commentary_ann_models)
        logger.info(
            f"Serializing PreAligned Commentary Pecha with segmentation id: {commentary_segmentation_id}"
        )
        return PreAlignedCommentarySerializer().serialize(
            root_pecha,
            root_alignment_id,
            commentary_pecha,
            annotation_path,
            pecha_category,
            commentary_segmentation_id,
        )
    else:
        return PreAlignedCommentarySerializer().serialize(
            root_pecha,
            root_alignment_id,
            commentary_pecha,
            annotation_path,
            pecha_category,
        )


def _serialize_prealigned_commentary_translation_pecha(
    pechas, metadatas, annotations, pecha_category, annotation_path
):
    root_pecha = pechas[2]
    commentary_pecha = pechas[1]
    translation_pecha = pechas[0]

    commentary_alignment_id = get_aligned_id(
        annotations[translation_pecha.id], annotation_path
    )

    root_alignment_id = get_aligned_id(
        annotations[commentary_pecha.id], commentary_alignment_id
    )

    PreAlignedCommentaryTranslationSerializer().serialize(
        root_pecha,
        root_alignment_id,
        commentary_pecha,
        commentary_alignment_id,
        translation_pecha,
        annotation_path,
        pecha_category,
    )


def _serialize_prealigned_root_translation_pecha(
    pechas, metadatas, annotations, pecha_category, annotation_path
):
    root_pecha = pechas[1]
    translation_pecha = pechas[0]
    root_alignment_id = get_aligned_id(
        annotations[translation_pecha.id], annotation_path
    )

    translation_ann_models = annotations[translation_pecha.id]
    if has_segmentation_annotation(translation_ann_models):
        translation_segmentation_id = get_segmentation_id(translation_ann_models)
        return PreAlignedRootTranslationSerializer().serialize(
            root_pecha,
            root_alignment_id,
            translation_pecha,
            annotation_path,
            pecha_category,
            translation_segmentation_id,
        )
    else:
        return PreAlignedRootTranslationSerializer().serialize(
            root_pecha,
            root_alignment_id,
            translation_pecha,
            annotation_path,
            pecha_category,
        )


# Registry mapping PechaType to handler function
PECHA_SERIALIZER_REGISTRY = {
    PechaType.root_pecha: _serialize_root_pecha,
    PechaType.root_translation_pecha: _serialize_root_translation_pecha,
    PechaType.commentary_pecha: _serialize_commentary_pecha,
    PechaType.commentary_translation_pecha: _serialize_commentary_translation_pecha,
    PechaType.prealigned_commentary_pecha: _serialize_prealigned_commentary_pecha,
    PechaType.prealigned_commentary_translation_pecha: _serialize_prealigned_commentary_translation_pecha,
    PechaType.prealigned_root_translation_pecha: _serialize_prealigned_root_translation_pecha,
}


class Serializer:
    @staticmethod
    def get_root_en_title(metadatas: List[Any], pechas: List[Pecha]) -> str:
        """
        Commentary Pecha serialized JSON should have the root English title.
        """
        logger.info(f"Metadatachain: {metadatas}")

        root_metadata = metadatas[-1]
        root_pecha = pechas[-1]

        en_title = root_metadata.title["en"]
        if not en_title:
            logger.error(f"English title is missing in Root Pecha {root_pecha.id}.")
            raise MetaDataMissingError(
                f"English title is missing in Root Pecha {root_pecha.id}."
            )
        return en_title

    def serialize(
        self,
        pechas: List[Pecha],
        metadatas: List[Any],
        annotations: Dict[str, List[AnnotationModel]],
        pecha_category: List[Dict[str, Dict[str, str]]],
        annotation_path: str,
    ):
        """
        Serialize a Pecha based on its type.
        """
        pecha = pechas[0]
        pecha_type = get_pecha_type(pechas, metadatas, annotations, annotation_path)
        logger.info(f"Serializing Pecha {pecha.id}, Type: {pecha_type}")
        handler = PECHA_SERIALIZER_REGISTRY.get(pecha_type)
        if not handler:
            raise ValueError(f"Unsupported pecha type: {pecha_type}")
        return handler(pechas, metadatas, annotations, pecha_category, annotation_path)
