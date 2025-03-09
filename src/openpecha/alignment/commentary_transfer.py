from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns

logger = get_logger(__name__)


class CommentaryAlignmentTransfer:
    def get_first_layer_path(self, pecha: Pecha) -> Path:
        return next(pecha.layer_path.rglob("*.json"))

    def base_update(self, src_pecha: Pecha, tgt_pecha: Pecha) -> Path:
        """
        1. Take the layer from src pecha
        2. Migrate the layer to tgt pecha using base update
        """
        src_base_name = list(src_pecha.bases.keys())[0]
        tgt_base_name = list(tgt_pecha.bases.keys())[0]
        tgt_pecha.merge_pecha(src_pecha, src_base_name, tgt_base_name)

        src_layer_name = next(src_pecha.layer_path.rglob("*.json")).name
        new_layer_path = tgt_pecha.layer_path / tgt_base_name / src_layer_name
        return new_layer_path

    def extract_root_anns(self, layer: AnnotationStore) -> Dict:
        """
        Extract annotation from layer(STAM)
        """
        anns = {}
        for ann in layer.annotations():
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            ann_metadata = {}
            for data in ann:
                ann_metadata[data.key().id()] = str(data.value())
            anns[int(ann_metadata["root_idx_mapping"])] = {
                "Span": {"start": start, "end": end},
                "text": str(ann),
                "root_idx_mapping": int(ann_metadata["root_idx_mapping"]),
            }
        return anns

    def map_layer_to_layer(
        self, src_layer: AnnotationStore, tgt_layer: AnnotationStore
    ):
        """
        1. Extract annotations from source and target layers
        2. Map the annotations from source to target layer
        src_layer -> tgt_layer (One to Many)
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
        self, root_pecha: Pecha, root_display_pecha: Pecha
    ) -> Dict[int, List]:
        """
        Get segmentation mapping from root_pecha -> root_display_pecha
        """
        display_layer_path = self.get_first_layer_path(root_display_pecha)
        new_tgt_layer = self.base_update(root_pecha, root_display_pecha)

        display_layer = AnnotationStore(file=str(display_layer_path))
        transfer_layer = AnnotationStore(file=str(new_tgt_layer))

        map = self.map_layer_to_layer(transfer_layer, display_layer)

        # Clean up the layer
        new_tgt_layer.unlink()
        return map

    def get_serialized_commentary(
        self, root_display_pecha: Pecha, root_pecha: Pecha, commentary_pecha: Pecha
    ) -> List[str]:
        def is_empty(text):
            """Check if text is empty or contains only newlines."""
            return not text.strip().replace("\n", "")

        root_map = self.get_root_pechas_mapping(root_pecha, root_display_pecha)

        root_display_layer_path = self.get_first_layer_path(root_display_pecha)
        root_display_anns = self.extract_root_anns(
            AnnotationStore(file=str(root_display_layer_path))
        )

        root_layer_path = self.get_first_layer_path(root_pecha)
        root_anns = self.extract_root_anns(AnnotationStore(file=str(root_layer_path)))

        commentary_layer_path = self.get_first_layer_path(commentary_pecha)
        commentary_anns = get_anns(AnnotationStore(file=str(commentary_layer_path)))
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

            serialized_content.append(f"<1><{root_display_idx}>{commentary_text}")
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
