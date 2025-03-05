from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns

logger = get_logger(__name__)


class PreAlignedCommentarySerializer:
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
                if (
                    src_start
                    <= tgt_start
                    < src_end  # Target annotation starts within source
                    or src_start
                    < tgt_end
                    <= src_end  # Target annotation ends within source
                    or (
                        tgt_start < src_start and tgt_end > src_end
                    )  # Target fully contains source
                ) and not (
                    tgt_start == src_end or tgt_end == src_start
                ):  # No exact edge overlap
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

        root_display_layer_path = next(root_display_pecha.layer_path.rglob("*.json"))
        root_display_anns = self.extract_root_anns(
            AnnotationStore(file=str(root_display_layer_path))
        )

        root_layer_path = next(root_pecha.layer_path.rglob("*.json"))
        root_anns = self.extract_root_anns(AnnotationStore(file=str(root_layer_path)))

        commentary_layer_path = next(commentary_pecha.layer_path.rglob("*.json"))
        commentary_anns = get_anns(AnnotationStore(file=str(commentary_layer_path)))
        segments = []
        for ann in commentary_anns:
            root_indices = parse_root_mapping(ann["root_idx_mapping"])
            first_idx = root_indices[0]
            commentary_text = ann["text"]

            # # If the commentary text is empty, skip
            if is_empty(commentary_text):
                curr_segment = commentary_text

            # If aligned root does not have text, dont add any mapping
            elif not root_map.get(first_idx):
                curr_segment = commentary_text

            # If the root text is empty, dont add any mapping
            elif is_empty(root_anns[first_idx]["text"]):
                curr_segment = commentary_text
            else:
                display_idx = root_map[first_idx][0]
                if display_idx in root_display_anns and not is_empty(
                    root_display_anns[display_idx]["text"]
                ):
                    curr_segment = f"<1><{display_idx}>{commentary_text}"
                # If root display is empty, dont add any mapping
                else:
                    curr_segment = commentary_text
            segments.append(curr_segment)
        return segments


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
