from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import FileNotFoundError, StamAnnotationStoreLoadError
from openpecha.pecha import Pecha

logger = get_logger(__name__)


def get_base_text(pecha: Pecha, layer_path: str):
    ann_store_path = pecha.pecha_path.parent.joinpath(layer_path)
    if ann_store_path.exists():
        try:
            ann_store = AnnotationStore(file=ann_store_path.as_posix())
            base_text = next(ann_store.resources()).text()
            return base_text
        except Exception as e:
            logger.error(
                f"Unable to load annotation store from layer path: {ann_store_path}. {str(e)}"
            )
            raise StamAnnotationStoreLoadError(
                f"[Error] Error loading annotation store from layer path: {layer_path}. {str(e)}"
            )
    else:
        logger.error(f"The layer path {str(ann_store_path)} does not exist.")
        raise FileNotFoundError(
            f"[Error] The layer path '{str(ann_store_path)}' does not exist."
        )
