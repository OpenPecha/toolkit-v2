from typing import Dict, List, Any
from openpecha.pecha import Pecha
from openpecha.pecha.pecha_types import PechaType, get_pecha_type
from openpecha.pecha.serializers.json import JsonSerializer
from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.alignment.translation_transfer import TranslationAlignmentTransfer
from openpecha.config import get_logger

logger = get_logger(__name__)


class SerializerLogicHandler:
    """Handles serialization logic for different types of pecha alignment scenarios."""
    
    def serialize(
        self,
        target: Dict[str, Any],
        source: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Serialize pecha data based on alignment structure.
        
        Args:
            to: Dictionary containing target pecha and its annotations
                Format: {
                    'pecha': Pecha object,
                    'annotations': [{'id': str, 'type': str}]
                }
            from_: Dictionary containing source pecha and its annotations (optional)
                Format: {
                    'pecha': Pecha object,
                    'annotations': [{'id': str, 'type': str, 'aligned_to': str}]
                }
        
        Returns:
            Serialized data structure
        """
        target_pecha = target['pecha']
        target_annotations = target['annotations']
        
        
        if source == None:
            # Simple serialization of target pecha only
            return JsonSerializer().serialize_single_pecha(target_pecha, target_annotations)
        else:
            # Alignment-based serialization
            source_pecha = source['pecha']
            source_annotations = source['annotations']
        
            return self._serialize_aligned_pechas(
                target_pecha, target_annotations,
                source_pecha, source_annotations
            )
    

    def _serialize_aligned_pechas(
        self,
        target_pecha: Pecha, target_annotations: List[dict],
        source_pecha: Pecha, source_annotations: List[dict]
    ) -> Dict[str, Any]:
        """
        Serialize aligned pechas using alignment transfer logic.

        This handles the case where we have source and target pechas with alignment relationships.
        """
        # Find alignment annotations
        target_base = JsonSerializer().get_base_from_pecha(target_pecha, target_annotations)
        source_base = JsonSerializer().get_base_from_pecha(source_pecha, source_annotations)
        
        
        json_without_transformations = JsonSerializer().serialize_aligned_pechas( source_pecha, source_annotations, target_pecha, target_annotations)
        json_with_transformations = JsonSerializer().serialize_algined_pechas_with_annotations_transfered(target_pecha, target_annotations, source_pecha, source_annotations)
        
        return {
            "target": {
                "base": target_base
            },
            "source": {
                "base": source_base
            },
            "json_without_transformations": json_without_transformations,
            "json_with_transformations": json_with_transformations
        }
    
    