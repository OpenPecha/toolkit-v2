from enum import Enum
from typing import Dict, List


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
    root_metadata = metadatas[-1]
    parent_metadata = metadatas[-2]

    aligned_root_id = parent_metadata["annotations"][0].aligned_to.alignment_id

    if root_metadata["annotations"][0].id == aligned_root_id:
        return False
    return True


def is_root_related_pecha(pecha_type: PechaType) -> bool:
    """
    Returns True if the pecha type is root-related.
    """
    return pecha_type in [
        PechaType.root_pecha,
        PechaType.root_translation_pecha,
        PechaType.prealigned_root_translation_pecha,
    ]


def is_commentary_related_pecha(pecha_type: PechaType) -> bool:
    """
    Returns True if the pecha type is commentary-related.
    """
    return pecha_type in [
        PechaType.commentary_pecha,
        PechaType.commentary_translation_pecha,
        PechaType.prealigned_commentary_pecha,
        PechaType.prealigned_commentary_translation_pecha,
    ]
