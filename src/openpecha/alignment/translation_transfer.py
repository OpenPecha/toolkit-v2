from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns, load_layer

logger = get_logger(__name__)


class TranslationAlignmentTransfer:
    def get_display_layer_path(self, pecha: Pecha) -> Path:
        """
        Return the path to the first segmentation layer JSON file in the pecha.
        """
        return next(pecha.layer_path.rglob("segmentation-*.json"))

    def map_layer_to_layer(
        self, src_layer: AnnotationStore, tgt_layer: AnnotationStore
    ) -> Dict[int, List[int]]:
        """
        Map annotations from src_layer to tgt_layer based on span overlap or containment.
        Returns a mapping from source indices to lists of target indices.
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
        self, root_pecha: Pecha, root_alignment_id: str
    ) -> Dict[int, List[int]]:
        """
        Get mapping from root_pecha's alignment layer to its display segmentation layer.
        """
        display_layer_path = self.get_display_layer_path(root_pecha)
        display_layer = load_layer(display_layer_path)
        alignment_layer = load_layer(root_pecha.layer_path / root_alignment_id)
        return self.map_layer_to_layer(alignment_layer, display_layer)

    def get_translation_pechas_mapping(
        self, translation_pecha: Pecha, translation_alignment_id: str
    ) -> Dict[int, List]:
        """
        Get Segmentation mapping from translation display pecha -> translation pecha
        """
        display_layer_path = self.get_display_layer_path(translation_pecha)
        alignment_layer_path = translation_pecha.layer_path / translation_alignment_id

        display_layer = load_layer(display_layer_path)
        alignment_layer = load_layer(alignment_layer_path)

        map = self.map_layer_to_layer(display_layer, alignment_layer)

        return map

    def get_serialized_translation(
        self,
        root_pecha: Pecha,
        root_alignment_id: str,
        root_translation_pecha: Pecha,
        translation_alignment_id: str,
    ) -> List[str]:
        """
        Serialize translation segments so that each segment aligns with the display layer of the root pecha.
        """

        def is_empty(text: str) -> bool:
            return not text.strip().replace("\n", "")

        root_map = self.get_root_pechas_mapping(root_pecha, root_alignment_id)
        translation_layer_path = (
            root_translation_pecha.layer_path / translation_alignment_id
        )
        translation_anns = get_anns(
            load_layer(translation_layer_path), include_span=True
        )

        mapped_segment: Dict[int, List[str]] = {}
        for ann in translation_anns:
            root_idx = int(ann["root_idx_mapping"])
            translation_text = ann["text"]
            if not root_map.get(root_idx):
                continue
            root_display_idx = root_map[root_idx][0]
            mapped_segment.setdefault(root_display_idx, []).append(translation_text)

        max_root_idx = max(mapped_segment.keys(), default=0)
        serialized_content = []
        for i in range(1, max_root_idx + 1):
            texts = mapped_segment.get(i, [])
            text = "\n".join(texts)
            serialized_content.append("") if is_empty(
                text
            ) else serialized_content.append(text)

        return serialized_content

    def get_serialized_translation_display(
        self,
        root_pecha: Pecha,
        root_alignment_id: str,
        translation_pecha: Pecha,
        translation_alignment_id: str,
        translation_display_id: str,
    ):
        """
        Input: map from transfer_layer -> display_layer (One to Many)
        Structure in a way such as : <chapter number><display idx>translation text
        Note: From many relation in display layer, take first idx (Sefaria map limitation)
        """
        root_map = self.get_root_pechas_mapping(root_pecha, root_alignment_id)
        translation_map = self.get_translation_pechas_mapping(
            translation_pecha, translation_alignment_id
        )

        layer_path = translation_pecha.layer_path / translation_display_id
        anns = get_anns(load_layer(layer_path), include_span=True)

        segments = []
        mapped_segments = {}
        for src_idx, tgt_map in translation_map.items():
            translation_text = next(
                (
                    ann["text"]
                    for ann in anns
                    if int(ann["root_idx_mapping"]) == src_idx
                ),
                "",
            )
            tgt_idx = tgt_map[0]
            root_idx = root_map[tgt_idx][0]
            mapped_segments[root_idx] = translation_text

        max_root_idx = max(mapped_segments.keys(), default=0)
        for i in range(1, max_root_idx + 1):
            text = mapped_segments.get(i, "")
            segments.append(text)
        return segments
