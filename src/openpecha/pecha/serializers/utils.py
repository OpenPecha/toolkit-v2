from typing import Any, Dict, List, Optional, Tuple

from openpecha.pecha.annotations import AnnotationModel


def find_related_pecha_id(
    annotations: Dict[str, List[AnnotationModel]], annotation_path: str
) -> Optional[str]:
    """
    Find the related pecha id by comparing with annotation_path
    """
    for pecha_id, anns in annotations.items():
        for ann in anns:
            if ann.path == annotation_path:
                return pecha_id

    return None


def get_metadatachain_from_metadatatree(
    metadatatree: List[Tuple[str, Any]], pecha_id: str
) -> List[Tuple[str, Any]]:
    """
    MetadataTree contains metadata of all pecha related to it.
    Metadatachain is chain from pecha to root pecha.
    """
    metadatachain = []

    flag = True
    while flag:
        for metadata_pecha_id, metadata in metadatatree:
            if metadata_pecha_id == pecha_id:
                if metadata.commentary_of:
                    metadatachain.append((metadata_pecha_id, metadata))
                    pecha_id = metadata.commentary_of
                    break

                if metadata.translation_of:
                    metadatachain.append((metadata_pecha_id, metadata))
                    pecha_id = metadata.translation_of
                    break

                flag = False
                metadatachain.append((metadata_pecha_id, metadata))
                break

    return metadatachain
