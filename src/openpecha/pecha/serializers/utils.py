from typing import Dict, List, Optional

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
