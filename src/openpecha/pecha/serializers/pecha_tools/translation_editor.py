from typing import Any, Dict, List, Optional

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import (
    FileNotFoundError,
    MetaDataMissingError,
    StamAnnotationStoreLoadError,
)
from openpecha.pecha import Pecha, get_annotations_data
from openpecha.pecha.serializers.pecha_tools.utils import get_base_text

logger = get_logger(__name__)


def get_layer_name(metadatas: List[Dict[str, Any]]) -> str:
    """
    Get the layer name from the metadata.
    """
    for metadata in metadatas:
        if "annotations" in metadata:
            return metadata["annotations"][0]["layer_name"]
    raise MetaDataMissingError("Layer name is missing in the metadata.")


class TranslationSerializer:
    def get_annotations_from_layer(self, pecha: Pecha, layer_path: str):
        ann_store_path = pecha.pecha_path.parent.joinpath(layer_path)
        if not ann_store_path.exists():
            logger.error(f"The layer path {str(ann_store_path)} does not exist.")
            raise FileNotFoundError(
                f"[Error] The layer path '{str(ann_store_path)}' does not exist."
            )
        else:
            try:
                annotation_store = AnnotationStore(file=ann_store_path.as_posix())
                annotations = get_annotations_data(annotation_store)
                return annotations
            except Exception as e:
                logger.error(
                    f"Unable to load annotation store from layer path: {ann_store_path}. {str(e)}"
                )
                raise StamAnnotationStoreLoadError(
                    f"[Error] Error loading annotation store from layer path: {layer_path}. {str(e)}"
                )

    def serialize(
        self,
        pechas: List[Pecha],
        metadatas: List[Dict[str, Any]],
        pecha_category: List[Dict[str, object]],
        layer_name: Optional[str] = None,
    ) -> Dict:
        # Get content from root and translation pecha
        pecha = pechas[0]
        metadata = metadatas[0]
        if layer_name is None:
            layer_name = get_layer_name(metadatas)

        layer_path = pecha.get_segmentation_layer_path()
        base_text = get_base_text(pecha, layer_path)
        annotations = self.get_annotations_from_layer(pecha, layer_path)

        serialized_json = {
            "base_text": base_text,
            "annotations": annotations,
            "metadata": metadata,
            "pecha_category": pecha_category,
        }
        logger.info(f"Pecha {pecha.id} is serialized successfully.")
        return serialized_json
