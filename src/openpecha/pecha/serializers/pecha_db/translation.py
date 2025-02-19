from typing import Dict, List, Union

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import (
    AlignmentDataKeyMissingError,
    FileNotFoundError,
    StamAnnotationStoreLoadError,
)
from openpecha.pecha import Pecha, get_pecha_with_id
from openpecha.pecha.metadata import Language
from openpecha.utils import chunk_strings, get_text_direction_with_lang

logger = get_logger(__name__)


class TranslationSerializer:
    def get_pecha_category(self, pecha: Pecha):
        """
        Set pecha category both in english and tibetan in the JSON output.
        """
        pecha_title = self.get_pecha_bo_title(pecha)
        category_extractor = CategoryExtractor()
        categories = category_extractor.get_category(pecha_title)
        return categories["bo"], categories["en"]

    def get_metadata_for_pecha_org(self, pecha: Pecha, lang: Union[str, None] = None):
        """
        Extract required metadata from opf
        """
        if not lang:
            lang = pecha.metadata.language.value
        direction = get_text_direction_with_lang(lang)
        title = pecha.metadata.title
        if isinstance(title, dict):
            title = title.get(lang.lower(), None) or title.get(  # type: ignore
                lang.upper(), None  # type: ignore
            )
        title = title if lang in ["bo", "en"] else f"{title}[{lang}]"
        source = pecha.metadata.source if pecha.metadata.source else ""

        return {
            "title": title,
            "language": lang,
            "versionSource": source,
            "direction": direction,
            "completestatus": "done",
        }

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
            return chunk_strings(segments)

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

            return chunk_strings(translation_segments)

    def get_pecha_bo_title(self, pecha: Pecha):
        """
        Get tibetan title from the Pecha metadata
        """
        title = pecha.metadata.title
        if isinstance(title, dict):
            title = title.get("bo") or title.get("BO")

        return title

    def serialize(
        self,
        pecha: Pecha,
        alignment_data: Union[Dict, None] = None,
    ) -> Dict:

        if alignment_data:
            if "source" not in alignment_data or "target" not in alignment_data:
                logger.error(
                    f"Pecha {pecha.id} alignment data must have 'source' and 'target' keys."
                )
                raise AlignmentDataKeyMissingError(
                    f"Pecha {pecha.id} alignment data must have 'source' and 'target' keys."
                )
            root_pecha = get_pecha_with_id(alignment_data["source"].split("/")[0])
            translation_pecha = pecha
            root_content = self.get_root_content(root_pecha, alignment_data["source"])
            translation_content = self.get_translation_content(
                translation_pecha, alignment_data["target"]
            )
        else:
            root_pecha = pecha
            translation_pecha = None
            root_layer_path = next(root_pecha.layer_path.rglob("*.json"))
            root_content = self.get_root_content(
                root_pecha, root_layer_path.relative_to(root_pecha.pecha_path.parent)
            )
            translation_content = []

        # Get pecha category from pecha_org_tools package and set to JSON
        bo_category, en_category = self.get_pecha_category(root_pecha)

        root_json: Dict[str, List] = {
            "categories": bo_category,
            "books": [
                {**self.get_metadata_for_pecha_org(root_pecha), "content": root_content}
            ],
        }

        translation_metadata = self.get_metadata_for_pecha_org(
            translation_pecha if translation_pecha else root_pecha,
            Language.english.value,
        )
        translation_json = {
            "categories": en_category,
            "books": [{**translation_metadata, "content": translation_content}],
        }

        # Set the content for source and target and set it to JSON
        serialized_json = {
            "source": translation_json,
            "target": root_json,
        }
        logger.info(f"Pecha {pecha.id} is serialized successfully.")
        return serialized_json
