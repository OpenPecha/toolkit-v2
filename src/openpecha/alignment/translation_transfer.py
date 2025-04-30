from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha

logger = get_logger(__name__)


class TranslationAlignmentTransfer:
    def get_display_layer_path(self, pecha: Pecha) -> Path:
        """
        Return the path to the first segmentation layer JSON file in the pecha.
        """
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
        mapping: Dict[int, List[int]] = {}

        src_anns = self.extract_root_anns(src_layer)
        tgt_anns = self.extract_root_anns(tgt_layer)

        for src_idx, src_span in src_anns.items():
            src_start, src_end = src_span["Span"]["start"], src_span["Span"]["end"]
            mapping[src_idx] = []
            for tgt_idx, tgt_span in tgt_anns.items():
                tgt_start, tgt_end = tgt_span["Span"]["start"], tgt_span["Span"]["end"]
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
        display_layer = AnnotationStore(file=str(display_layer_path))
        transfer_layer = AnnotationStore(
            file=str(root_pecha.layer_path / root_alignment_id)
        )
        return self.map_layer_to_layer(transfer_layer, display_layer)

    def get_translation_pechas_mapping(
        self, translation_pecha: Pecha, translation_alignment_id: str
    ) -> Dict[int, List]:
        """
        Get Segmentation mapping from translation display pecha -> translation pecha
        """
        display_layer_path = self.get_display_layer_path(translation_pecha)
        tgt_layer_path = translation_pecha.layer_path / translation_alignment_id

        display_layer = AnnotationStore(file=str(display_layer_path))
        transfer_layer = AnnotationStore(file=str(tgt_layer_path))

        map = self.map_layer_to_layer(transfer_layer, display_layer)

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
        translation_anns = self.extract_root_anns(
            AnnotationStore(file=str(translation_layer_path))
        )
        root_display_layer_path = self.get_display_layer_path(root_pecha)
        root_display_anns = self.extract_root_anns(
            AnnotationStore(file=str(root_display_layer_path))
        )

        mapped_segment: Dict[int, List[str]] = {}
        for ann in translation_anns.values():
            root_idx = ann["root_idx_mapping"]
            translation_text = ann["text"]
            if not root_map.get(root_idx):
                continue
            root_display_idx = root_map[root_idx][0]
            mapped_segment.setdefault(root_display_idx, []).append(translation_text)

        max_root_idx = max(root_display_anns.keys(), default=0)
        serialized_content = []
        for i in range(1, max_root_idx + 1):
            texts = mapped_segment.get(i, [])
            text = "\n".join(texts)
            serialized_content.append("") if is_empty(
                text
            ) else serialized_content.append(text)

        return serialized_content
