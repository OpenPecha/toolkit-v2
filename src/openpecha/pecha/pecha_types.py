from enum import Enum
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel


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


def get_aligned_id(ann_models: List[AnnotationModel], annotation_path: str):
    """
    Get the alignment id from List of AnnotationModel
    """
    for ann_model in ann_models:
        if annotation_path == ann_model.path:
            aligned_to = ann_model.aligned_to
            if aligned_to and aligned_to.alignment_id:
                return aligned_to.alignment_id
    return None


def get_pecha_type(
    pechas: List[Pecha],
    metadatas: List[Dict],
    annotations: Dict[str, List[AnnotationModel]],
    annotation_path: str,
) -> PechaType:
    is_commentary = is_commentary_pecha(metadatas)
    is_translation = is_translation_pecha(metadatas)

    if is_commentary:
        if is_translation:
            if has_version_of(pechas, annotations, annotation_path):
                return PechaType.prealigned_commentary_translation_pecha
            return PechaType.commentary_translation_pecha
        if has_version_of(pechas, annotations, annotation_path):
            return PechaType.prealigned_commentary_pecha

        return PechaType.commentary_pecha
    else:
        if is_translation:
            if has_version_of(pechas, annotations, annotation_path):
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


def has_version_of(
    pechas: List[Pecha],
    annotations: Dict[str, List[AnnotationModel]],
    annotation_path: str,
) -> bool:
    """
    Return
        True: If the pecha points to an alignment annotation layer of Root Pecha
        False: otherwise
    """
    root_pecha = pechas[-1]
    parent_pecha = pechas[-2]

    if len(annotations.keys()) == 3:
        annotation_path = get_aligned_id(annotations[pechas[0].id], annotation_path)

    aligned_root_id = get_aligned_id(annotations[parent_pecha.id], annotation_path)

    if aligned_root_id != annotations[root_pecha.id][0].path:
        return True
    return False


def is_root_related_pecha(metadatas: List[Dict]) -> bool:
    """
    Returns True if the pecha type is root-related.
    """
    for metadata in metadatas:
        if metadata["commentary_of"]:
            return False
    return True
