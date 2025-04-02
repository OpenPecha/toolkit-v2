from typing import Dict, List, Union

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import FileNotFoundError, StamAnnotationStoreLoadError
from openpecha.pecha import Pecha
from openpecha.pecha.metadata import Language
from openpecha.pecha.serializers.pecha_db.utils import (
    get_metadata_for_pecha_org,
    get_pecha_title,
)
from openpecha.utils import chunk_strings

logger = get_logger(__name__)


class RootSerializer:
    def __init__(self):
        self.bo_root_category = {
            "name": "རྩ་བ།",
            "heDesc": "",
            "heShortDesc": "",
        }
        self.en_root_category = {
            "name": "Root text",
            "enDesc": "",
            "enShortDesc": "",
        }

    def format_category(self, pecha: Pecha, category: Dict[str, List[Dict[str, str]]]):
        """
        1.Add Root section ie "རྩ་བ།" or "Root text" to category
        2.Add pecha title to category
        """
        bo_category, en_category = category["bo"], category["en"]
        bo_category.append(self.bo_root_category)
        en_category.append(self.en_root_category)

        bo_title = get_pecha_title(pecha, "bo")
        en_title = get_pecha_title(pecha, "en")

        bo_category.append({"name": bo_title, "heDesc": "", "heShortDesc": ""})
        en_category.append({"name": en_title, "enDesc": "", "enShortDesc": ""})

        return {"bo": bo_category, "en": en_category}

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
        pecha: Pecha,
        pecha_category: Dict[str, List[Dict[str, str]]],
        translation_pecha: Union[Pecha, None] = None,
    ) -> Dict:

        # Format Category
        formatted_category = self.format_category(pecha, pecha_category)
        root_category, translation_category = (
            formatted_category["bo"],
            formatted_category["en"],
        )
        # Get the metadata for root and translation pecha
        root_metadata = get_metadata_for_pecha_org(pecha)

        if translation_pecha:
            translation_metadata = get_metadata_for_pecha_org(translation_pecha)
        else:
            translation_metadata = get_metadata_for_pecha_org(
                pecha, lang=Language.english.value
            )

        # Get content from root and translation pecha
        root_content = self.get_root_content(pecha, pecha.get_segmentation_layer_path())
        if translation_pecha:
            translation_content = self.get_translation_content(
                translation_pecha, translation_pecha.get_segmentation_layer_path()
            )
        else:
            translation_content = []

        # Preprocess newlines in content
        root_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in root_content
        ]
        translation_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>")
            for line in translation_content
        ]

        # Chapterize content
        root_content = chunk_strings(root_content)
        translation_content = chunk_strings(translation_content)

        root_json: Dict[str, List] = {
            "categories": root_category,
            "books": [{**root_metadata, "content": root_content}],
        }

        translation_json = {
            "categories": translation_category,
            "books": [{**translation_metadata, "content": translation_content}],
        }

        # Set the content for source and target and set it to JSON
        serialized_json = {
            "source": translation_json,
            "target": root_json,
        }
        logger.info(f"Pecha {pecha.id} is serialized successfully.")
        return serialized_json
