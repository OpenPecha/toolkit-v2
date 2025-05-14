from typing import Any, Dict, List, Optional

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


def get_metadatachain_from_metadatatree(metadatatree: List[Any], pecha_id: str):
    """
    MetadataTree contains metadata of all pecha related to it.
    Metadatachain is chain from pecha to root pecha.
    """
    metadatachain = []

    flag = True
    while flag:
        for metadata in metadatatree:
            if metadata.id == pecha_id:
                if metadata.commentary_of:
                    metadatachain.append(metadata)
                    pecha_id = metadata.commentary_of
                    break

                if metadata.translation_of:
                    metadatachain.append(metadata)
                    pecha_id = metadata.translation_of
                    break

                flag = False
                metadatachain.append(metadata)
                break

    return metadatachain
