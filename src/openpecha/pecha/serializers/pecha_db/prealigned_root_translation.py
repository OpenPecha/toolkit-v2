from typing import Dict, List, Union

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.alignment.translation_transfer import TranslationAlignmentTransfer
from openpecha.config import get_logger
from openpecha.exceptions import (
    FileNotFoundError,
    PechaCategoryNotFoundError,
    StamAnnotationStoreLoadError,
)
from openpecha.pecha import Pecha, get_first_layer_file
from openpecha.pecha.metadata import Language
from openpecha.utils import get_text_direction_with_lang

logger = get_logger(__name__)


class PreAlignedRootTranslationSerializer:
    def get_pecha_category(self, pecha: Pecha):
        """
        Set pecha category both in english and tibetan in the JSON output.
        """
        pecha_title = self.get_pecha_bo_title(pecha)

        try:
            category_extractor = CategoryExtractor()
            categories = category_extractor.get_category(pecha_title)
            bo_category = categories.get("bo")
            en_category = categories.get("en")

            if bo_category is None or en_category is None:
                raise KeyError(
                    f"bo or en category is missing in pecha category for title {pecha_title}."
                )

        except Exception as e:
            logger.error(
                f"Failed getting Category for pecha {pecha.id} title: {pecha_title}. {str(e)}"
            )
            raise PechaCategoryNotFoundError(
                f"Failed gettting Category for pecha {pecha.id} title: {pecha_title}. {str(e)}"
            )
        else:
            return bo_category, en_category

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
        # pecha: Pecha,
        # root_pecha: Union[Pecha, None] = None,
        root_display_pecha: Pecha,
        root_pecha: Pecha,
        translation_pecha: Pecha,
    ) -> Dict:
        # Get pecha category from pecha_org_tools package and set to JSON
        bo_category, en_category = self.get_pecha_category(root_pecha)

        src_content = TranslationAlignmentTransfer().get_serialized_translation(
            root_display_pecha, root_pecha, translation_pecha
        )

        root_layer_path = get_first_layer_file(root_display_pecha)
        tgt_content = self.get_root_content(root_display_pecha, root_layer_path)

        tgt_json: Dict[str, List] = {
            "categories": bo_category,
            "books": [
                {**self.get_metadata_for_pecha_org(root_pecha), "content": tgt_content}
            ],
        }

        translation_metadata = self.get_metadata_for_pecha_org(
            translation_pecha if translation_pecha else root_pecha,
            Language.english.value,
        )
        src_json = {
            "categories": en_category,
            "books": [{**translation_metadata, "content": src_content}],
        }

        # Set the content for source and target and set it to JSON
        serialized_json = {
            "source": src_json,
            "target": tgt_json,
        }
        logger.info(f"Pecha {translation_pecha.id} is serialized successfully.")
        return serialized_json
