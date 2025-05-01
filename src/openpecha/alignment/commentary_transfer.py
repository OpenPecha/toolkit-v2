from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns, load_layer
from openpecha.utils import (
    get_chapter_num_from_segment_num,
    process_segment_num_for_chapter,
)

logger = get_logger(__name__)


class CommentaryAlignmentTransfer:
    def get_segmentation_ann_path(self, pecha: Pecha) -> Path:
        return next(pecha.layer_path.rglob("segmentation-*.json"))

    def extract_root_anns(self, layer: AnnotationStore) -> Dict[int, Dict]:
        """
        Extract annotations from a STAM layer into a dictionary keyed by root index mapping.
        """
        anns = {}
        for ann in layer.annotations():
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            ann_metadata = {data.key().id(): str(data.value()) for data in ann}
            root_idx = int(ann_metadata["root_idx_mapping"])
            anns[root_idx] = {
                "Span": {"start": start, "end": end},
                "text": str(ann),
                "root_idx_mapping": root_idx,
            }
        return anns

    def map_layer_to_layer(
        self, src_layer: AnnotationStore, tgt_layer: AnnotationStore
    ) -> Dict[int, List[int]]:
        """
        Map annotations from src_layer to tgt_layer based on span overlap or containment.
        Returns a mapping from source indices to lists of target indices.
        """
        map: Dict[int, List[int]] = {}

        src_anns = get_anns(src_layer, include_span=True)
        tgt_anns = get_anns(tgt_layer, include_span=True)

        for src_ann in src_anns:
            src_start, src_end = src_ann["Span"]["start"], src_ann["Span"]["end"]
            src_idx = int(src_ann["root_idx_mapping"])
            map[src_idx] = []
            for tgt_ann in tgt_anns:
                tgt_start, tgt_end = tgt_ann["Span"]["start"], tgt_ann["Span"]["end"]
                tgt_idx = int(tgt_ann["root_idx_mapping"])

                is_overlap = (
                    src_start <= tgt_start < src_end or src_start < tgt_end <= src_end
                )
                is_contained = tgt_start < src_start and tgt_end > src_end
                is_edge_overlap = tgt_start == src_end or tgt_end == src_start
                if (is_overlap or is_contained) and not is_edge_overlap:
                    map[src_idx].append(tgt_idx)

        # Sort the dictionary
        return dict(sorted(map.items()))

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
        def is_empty(text):
            """Check if text is empty or contains only newlines."""
            return not text.strip().replace("\n", "")

        root_map = self.get_root_pechas_mapping(root_pecha, root_alignment_id)

        root_display_layer_path = self.get_segmentation_ann_path(root_pecha)
        root_display_anns = self.extract_root_anns(load_layer(root_display_layer_path))

        root_anns = self.extract_root_anns(
            load_layer(root_pecha.layer_path / root_alignment_id)
        )

        commentary_anns = get_anns(
            load_layer(commentary_pecha.layer_path / commentary_alignment_id)
        )
        serialized_content = []
        for ann in commentary_anns:
            root_indices = parse_root_mapping(ann["root_idx_mapping"])
            root_idx = root_indices[0]
            commentary_text = ann["text"]

            # Skip if commentary is empty
            is_commentary_empty = is_empty(commentary_text)
            if is_commentary_empty:
                continue

            # Dont include mapping if root is empty
            idx_not_in_root = root_idx not in root_anns
            if idx_not_in_root:
                serialized_content.append(commentary_text)
                continue

            is_root_empty = is_empty(root_anns[root_idx]["text"])
            if is_root_empty:
                serialized_content.append(commentary_text)
                continue

            # Dont include mapping if root_display is empty
            root_display_idx = root_map[root_idx][0]
            idx_not_in_root_display = root_display_idx not in root_display_anns
            if idx_not_in_root_display:
                serialized_content.append(commentary_text)
                continue

            is_root_display_empty = is_empty(
                root_display_anns[root_display_idx]["text"]
            )
            if is_root_display_empty:
                serialized_content.append(commentary_text)
                continue

            chapter_num = get_chapter_num_from_segment_num(root_display_idx)
            processed_root_display_idx = process_segment_num_for_chapter(
                root_display_idx
            )
            serialized_content.append(
                f"<{chapter_num}><{processed_root_display_idx}>{commentary_text}"
            )
        return serialized_content


def parse_root_mapping(mapping: str) -> List[int]:
    res = []
    for map in mapping.strip().split(","):
        map = map.strip()
        if "-" in map:
            start, end = map.split("-")
            res.extend(list(range(int(start), int(end) + 1)))
        else:
            res.append(int(map))

    res.sort()
    return res
