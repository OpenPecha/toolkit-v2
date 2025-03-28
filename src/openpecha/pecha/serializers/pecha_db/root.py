from typing import Dict, List, Union

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import (
    FileNotFoundError,
    RootPechaNotFoundError,
    StamAnnotationStoreLoadError,
)
from openpecha.pecha import Pecha, get_first_layer_file
from openpecha.pecha.metadata import Language
from openpecha.utils import chunk_strings, get_text_direction_with_lang

logger = get_logger(__name__)


class RootSerializer:
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
        pecha: Pecha,
        pecha_category: Dict[str, List[Dict[str, str]]],
        root_pecha: Union[Pecha, None] = None,
    ) -> Dict:
        """
        Root Pecha can be i) Root Pecha ii) Translation of Root Pecha
        if Root Pecha,
            pecha: Root Pecha
            root_pecha: None

        if Translation of Root Pecha,
            pecha: Translation of Root Pecha
            root_pecha: Root Pecha

        Output: JSON format for pecha_org
        """

        if root_pecha:
            if not root_pecha or not isinstance(root_pecha, Pecha):
                logger.error(
                    "Root pecha is not passed during Root Translation Serialization."
                )
                raise RootPechaNotFoundError(
                    "Root pecha is not passed during Root Translation Serialization."
                )

            root_layer_path = get_first_layer_file(root_pecha)
            root_content = self.get_root_content(root_pecha, root_layer_path)

            translation_pecha = pecha
            translation_layer_path = get_first_layer_file(translation_pecha)
            translation_content = self.get_translation_content(
                translation_pecha, translation_layer_path
            )
        else:
            root_pecha = pecha
            translation_pecha = None
            root_layer_path = get_first_layer_file(root_pecha)
            root_content = self.get_root_content(root_pecha, root_layer_path)
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

        bo_category, en_category = pecha_category["bo"], pecha_category["en"]

        root_json: Dict[str, List] = {
            "categories": bo_category,
            "books": [
                {**self.get_metadata_for_pecha_org(root_pecha), "content": root_content}
            ],
        }
        if translation_pecha:
            translation_metadata = self.get_metadata_for_pecha_org(translation_pecha)
        else:
            translation_metadata = self.get_metadata_for_pecha_org(
                root_pecha, lang=Language.english.value
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
