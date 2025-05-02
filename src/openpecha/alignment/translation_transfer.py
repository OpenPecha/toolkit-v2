from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns, load_layer

logger = get_logger(__name__)


class TranslationAlignmentTransfer:
    @staticmethod
    def is_empty(text: str) -> bool:
        return not text.strip().replace("\n", "")

    def get_segmentation_ann_path(self, pecha: Pecha) -> Path:
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

    def get_translation_pechas_mapping(
        self,
        pecha: Pecha,
        alignment_id: str,
        segmentation_id: str,
    ) -> Dict[int, List]:
        """
        Get Segmentation mapping from segmentation to alignment layer.
        """
        segmentation_ann_path = pecha.layer_path / segmentation_id
        segmentation_layer = load_layer(segmentation_ann_path)
        alignment_layer = load_layer(pecha.layer_path / alignment_id)
        return self.map_layer_to_layer(segmentation_layer, alignment_layer)

    def mapping_to_text_list(self, mapping: Dict[int, List[str]]) -> List[str]:
        """
        Flatten the mapping from Translation to Root Text
        """
        max_root_idx = max(mapping.keys(), default=0)
        res = []
        for i in range(1, max_root_idx + 1):
            texts = mapping.get(i, [])
            text = "\n".join(texts)
            res.append("") if self.is_empty(text) else res.append(text)
        return res

    def get_serialized_translation_alignment(
        self,
        root_pecha: Pecha,
        root_alignment_id: str,
        root_translation_pecha: Pecha,
        translation_alignment_id: str,
    ) -> List[str]:
        """
        Serialize with Root Translation Alignment Text mapped to Root Segmentation Text
        """
        root_map = self.get_root_pechas_mapping(root_pecha, root_alignment_id)

        layer = load_layer(root_translation_pecha.layer_path / translation_alignment_id)
        anns = get_anns(layer, include_span=True)

        # Root segmentation idx and Root Translation Alignment Text mapping
        map: Dict[int, List[str]] = {}
        for ann in anns:
            aligned_idx = int(ann["root_idx_mapping"])
            text = ann["text"]
            if not root_map.get(aligned_idx):
                continue
            root_segmentation_idx = root_map[aligned_idx][0]
            map.setdefault(root_segmentation_idx, []).append(text)

        return self.mapping_to_text_list(map)

    def get_serialized_translation_segmentation(
        self,
        root_pecha: Pecha,
        root_alignment_id: str,
        translation_pecha: Pecha,
        translation_alignment_id: str,
        translation_segmentation_id: str,
    ):
        """
        Serialize with Root Translation Segmentation Text mapped to Root Segmentation Text
        """
        root_map = self.get_root_pechas_mapping(root_pecha, root_alignment_id)
        translation_map = self.get_translation_pechas_mapping(
            translation_pecha, translation_alignment_id, translation_segmentation_id
        )

        layer = load_layer(translation_pecha.layer_path / translation_segmentation_id)
        anns = get_anns(layer, include_span=True)

        # Root segmentation idx and Root Translation Segmentation Text mapping
        map: Dict[int, List[str]] = {}
        for ann in anns:
            text = ann["text"]
            idx = int(ann["root_idx_mapping"])

            aligned_idx = translation_map[idx][0]
            root_segmentation_idx = root_map[aligned_idx][0]
            map.setdefault(root_segmentation_idx, []).append(text)

        return self.mapping_to_text_list(map)
