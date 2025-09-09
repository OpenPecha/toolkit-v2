from openpecha.pecha.annotations import BaseAnnotation
from openpecha.pecha.blupdate import DiffMatchPatch
from typing import List

from openpecha.config import get_logger

logger = get_logger(__name__)


def update_coords(
    anns: List[BaseAnnotation],
    old_base: str,
    new_base: str,
):
    """
    Update the start/end coordinates of the annotations from old base to new base
    """
    diff_update = DiffMatchPatch(old_base, new_base)
    for ann in anns:
        start = ann.span.start
        end = ann.span.end

        ann.span.start = diff_update.get_updated_coord(start)
        ann.span.end = diff_update.get_updated_coord(end)

    return anns
