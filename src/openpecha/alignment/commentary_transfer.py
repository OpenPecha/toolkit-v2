from typing import Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns
from openpecha.utils import (
    get_chapter_num_from_segment_num,
    process_segment_num_for_chapter,
)

logger = get_logger(__name__)


class CommentaryAlignmentTransfer:
    def get_display_layer_path(self, pecha: Pecha) -> Pecha:
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
        mapping: Dict = {}

        src_anns = self.extract_root_anns(src_layer)
        tgt_anns = self.extract_root_anns(tgt_layer)

        for src_idx, src_span in src_anns.items():
            src_start, src_end = src_span["Span"]["start"], src_span["Span"]["end"]
            mapping[src_idx] = []

            for tgt_idx, tgt_span in tgt_anns.items():
                tgt_start, tgt_end = tgt_span["Span"]["start"], tgt_span["Span"]["end"]

                # Check for mapping conditions
                is_overlap = (
                    src_start <= tgt_start < src_end or src_start < tgt_end <= src_end
                )
                is_contained = tgt_start < src_start and tgt_end > src_end
                is_edge_overlap = tgt_start == src_end or tgt_end == src_start
                if is_overlap or is_contained and not is_edge_overlap:
                    mapping[src_idx].append(tgt_idx)

        # Sort the mapping by source indices
        return dict(sorted(mapping.items()))

    def get_root_pechas_mapping(
        self, root_pecha: Pecha, root_alignment_id: str
    ) -> Dict[int, List]:
        """
        Get segmentation mapping from root_pecha -> root_display_pecha
        """
        display_layer_path = self.get_display_layer_path(root_pecha)

        display_layer = AnnotationStore(file=str(display_layer_path))
        transfer_layer = AnnotationStore(
            file=str(root_pecha.layer_path / root_alignment_id)
        )

        map = self.map_layer_to_layer(transfer_layer, display_layer)
        return map

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

        root_display_layer_path = self.get_display_layer_path(root_pecha)
        root_display_anns = self.extract_root_anns(
            AnnotationStore(file=str(root_display_layer_path))
        )

        root_anns = self.extract_root_anns(
            AnnotationStore(file=str(root_pecha.layer_path / root_alignment_id))
        )

        commentary_anns = get_anns(
            AnnotationStore(
                file=str(commentary_pecha.layer_path / commentary_alignment_id)
            )
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
