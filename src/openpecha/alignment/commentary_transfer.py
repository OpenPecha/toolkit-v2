from pathlib import Path
from typing import Any, Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns, load_layer
from openpecha.utils import get_chapter_for_segment, process_segment_num_for_chapter

logger = get_logger(__name__)


def is_empty(text: str) -> bool:
    """
    Return True if text is empty or contains only newlines.
    """
    return not text.strip().replace("\n", "")


def parse_root_mapping(mapping: str) -> List[int]:
    """
    Parse root_idx_mapping string like '1,2-4' into a sorted list of ints.
    """
    res = []
    for part in mapping.strip().split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            res.extend(list(range(int(start), int(end) + 1)))
        else:
            res.append(int(part))
    res.sort()
    return res


class CommentaryAlignmentTransfer:
    def get_segmentation_ann_path(self, pecha: Pecha) -> Path:
        """
        Return the path to the first segmentation layer JSON file in the pecha.
        """
        return next(pecha.layer_path.rglob("segmentation-*.json"))

    def index_annotations_by_root(
        self, anns: List[Dict[str, Any]]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Return a dict mapping root_idx_mapping to the annotation dict.
        """
        return {int(ann["root_idx_mapping"]): ann for ann in anns}

    def map_layer_to_layer(
        self, src_layer: AnnotationStore, tgt_layer: AnnotationStore
    ) -> Dict[int, List[int]]:
        """
        Map annotations from src_layer to tgt_layer based on span overlap or containment.
        """
        mapping: Dict[int, List[int]] = {}
        src_anns = get_anns(src_layer, include_span=True)
        tgt_anns = get_anns(tgt_layer, include_span=True)
        for src_ann in src_anns:
            src_start, src_end = src_ann["Span"]["start"], src_ann["Span"]["end"]
            src_idx = int(src_ann["root_idx_mapping"])
            mapping[src_idx] = []
            for tgt_ann in tgt_anns:
                tgt_start, tgt_end = tgt_ann["Span"]["start"], tgt_ann["Span"]["end"]
                tgt_idx = int(tgt_ann["root_idx_mapping"])

                is_overlap = (
                    src_start <= tgt_start < src_end or src_start < tgt_end <= src_end
                )
                is_contained = tgt_start < src_start and tgt_end > src_end
                is_edge_overlap = tgt_start == src_end or tgt_end == src_start
                if (is_overlap or is_contained) and not is_edge_overlap:
                    mapping[src_idx].append(tgt_idx)
        return dict(sorted(mapping.items()))

    def get_root_pechas_mapping(
        self, pecha: Pecha, alignment_id: str
    ) -> Dict[int, List[int]]:
        """
        Get mapping from pecha's alignment layer to segmentation layer.
        """
        segmentation_ann_path = self.get_segmentation_ann_path(pecha)
        segmentation_layer = load_layer(segmentation_ann_path)
        alignment_layer = load_layer(pecha.layer_path / alignment_id)
        return self.map_layer_to_layer(alignment_layer, segmentation_layer)

    def get_serialized_commentary(
        self,
        root_pecha: Pecha,
        root_alignment_id: str,
        commentary_pecha: Pecha,
        commentary_alignment_id: str,
    ) -> List[str]:
        """
        Serialize commentary annotations with root/segmentation mapping and formatting.
        """
        root_map = self.get_root_pechas_mapping(root_pecha, root_alignment_id)
        root_segmentation_path = self.get_segmentation_ann_path(root_pecha)
        root_segmentation_anns = self.index_annotations_by_root(
            get_anns(load_layer(root_segmentation_path))
        )
        root_anns = self.index_annotations_by_root(
            get_anns(load_layer(root_pecha.layer_path / root_alignment_id))
        )
        commentary_anns = get_anns(
            load_layer(commentary_pecha.layer_path / commentary_alignment_id)
        )

        res: List[str] = []
        for ann in commentary_anns:
            commentary_text = ann["text"]

            if is_empty(commentary_text):
                continue

            root_indices = parse_root_mapping(ann["root_idx_mapping"])
            root_idx = root_indices[0]

            if root_idx not in root_anns or is_empty(root_anns[root_idx]["text"]):
                res.append(commentary_text)
                continue

            root_display_idx = root_map[root_idx][0]
            if root_display_idx not in root_segmentation_anns or is_empty(
                root_segmentation_anns[root_display_idx]["text"]
            ):
                res.append(commentary_text)
                continue

            chapter_num = get_chapter_for_segment(root_display_idx)
            processed_root_display_idx = process_segment_num_for_chapter(
                root_display_idx
            )
            res.append(
                f"<{chapter_num}><{processed_root_display_idx}>{commentary_text}"
            )
        return res
