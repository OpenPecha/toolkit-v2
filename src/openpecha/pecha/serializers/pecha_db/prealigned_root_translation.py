from typing import Dict, List

from stam import AnnotationStore

from openpecha.alignment.translation_transfer import TranslationAlignmentTransfer
from openpecha.config import get_logger
from openpecha.exceptions import FileNotFoundError, StamAnnotationStoreLoadError
from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.utils import (
    FormatPechaCategory,
    get_metadata_for_pecha_org,
)
from openpecha.utils import chunk_strings

logger = get_logger(__name__)


class PreAlignedRootTranslationSerializer:
    @staticmethod
    def get_texts_from_layer(layer: AnnotationStore):
        """
        Extract texts from layer
        1.If text is a newline, replace it with empty string
        2.Replace newline with <br>
        """
        return [
            "" if str(ann) == "\n" else str(ann).replace("\n", "<br>") for ann in layer
        ]

    def get_root_content(self, pecha: Pecha, layer_path: str):
        ann_store_path = pecha.pecha_path.parent.joinpath(layer_path)
        if not ann_store_path.exists():
            logger.error(f"The layer path {str(ann_store_path)} does not exist.")
            raise FileNotFoundError(
                f"[Error] The layer path '{str(ann_store_path)}' does not exist."
            )

        try:
            segment_layer = AnnotationStore(file=ann_store_path.as_posix())
        except Exception as e:
            logger.error(
                f"Unable to load annotation store from layer path: {ann_store_path}. {str(e)}"
            )
            raise StamAnnotationStoreLoadError(
                f"[Error] Error loading annotation store from layer path: {layer_path}. {str(e)}"
            )
        else:
            segments = self.get_texts_from_layer(segment_layer)
            return segments

    def get_translation_content(self, pecha: Pecha, layer_path: str):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """
        ann_store_path = pecha.pecha_path.parent.joinpath(layer_path)
        if not ann_store_path.exists():
            logger.error(f"The layer path {str(ann_store_path)} does not exist.")
            raise FileNotFoundError(
                f"[Error] The layer path '{str(ann_store_path)}' does not exist."
            )

        try:
            translation_segment_layer = AnnotationStore(file=ann_store_path.as_posix())
        except Exception as e:
            logger.error(
                f"Unable to load annotation store from layer path: {ann_store_path}. {str(e)}"
            )
            raise StamAnnotationStoreLoadError(
                f"[Error] Error loading annotation store from layer path: {ann_store_path}. {str(e)}"
            )
        else:
            segments: Dict[int, List[str]] = {}
            for ann in translation_segment_layer:
                ann_data = {}
                for data in ann:
                    ann_data[str(data.key().id())] = data.value().get()

                if "root_idx_mapping" in ann_data:
                    root_map = int(ann_data["root_idx_mapping"])
                    segments[root_map] = [str(ann)]

            max_root_idx = max(segments.keys())
            translation_segments = []
            for root_idx in range(1, max_root_idx + 1):
                if root_idx in segments:
                    translation_segments.append("".join(segments[root_idx]))
                else:
                    translation_segments.append("")

            return translation_segments

    def serialize(
        self,
        root_display_pecha: Pecha,
        root_pecha: Pecha,
        translation_pecha: Pecha,
        pecha_category: List[Dict],
    ) -> Dict:
        # Format Category
        formatted_category = FormatPechaCategory().format_root_category(
            root_display_pecha, pecha_category
        )
        bo_category, en_category = formatted_category["bo"], formatted_category["en"]
        # Get the metadata for root and translation pecha
        root_metadata = get_metadata_for_pecha_org(root_display_pecha)
        translation_metadata = get_metadata_for_pecha_org(translation_pecha)

        # Get content from root and translation pecha
        src_content = TranslationAlignmentTransfer().get_serialized_translation(
            root_display_pecha, root_pecha, translation_pecha
        )

        tgt_content = self.get_root_content(
            root_display_pecha, root_display_pecha.get_segmentation_layer_path()
        )

        # Preprocess newlines in content
        src_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in src_content
        ]
        tgt_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in tgt_content
        ]

        # Chapterize content
        chapterized_src_content: List[List[str]] = chunk_strings(src_content)
        chapterized_tgt_content: List[List[str]] = chunk_strings(tgt_content)

        tgt_json: Dict[str, List] = {
            "categories": bo_category,
            "books": [
                {
                    **root_metadata,
                    "content": chapterized_tgt_content,
                }
            ],
        }

        src_json = {
            "categories": en_category,
            "books": [{**translation_metadata, "content": chapterized_src_content}],
        }

        # Set the content for source and target and set it to JSON
        serialized_json = {
            "source": src_json,
            "target": tgt_json,
        }
        logger.info(f"Pecha {translation_pecha.id} is serialized successfully.")
        return serialized_json
