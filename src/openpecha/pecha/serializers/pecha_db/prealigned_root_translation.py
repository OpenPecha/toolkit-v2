from typing import Dict, List, Union

from stam import AnnotationStore

from openpecha.alignment.translation_transfer import TranslationAlignmentTransfer
from openpecha.config import get_logger
from openpecha.exceptions import (
    FileNotFoundError,
    MetaDataMissingError,
    StamAnnotationStoreLoadError,
)
from openpecha.pecha import Pecha, get_first_layer_file
from openpecha.utils import chunk_strings, get_text_direction_with_lang

logger = get_logger(__name__)


class PreAlignedRootTranslationSerializer:
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

    def get_pecha_title(self, pecha: Pecha, lang: str):
        pecha_title = pecha.metadata.title

        if isinstance(pecha_title, dict):
            title = pecha_title.get(lang.lower()) or pecha_title.get(lang.upper())

        if title is None or title == "":
            logger.error(
                f"[Error] {lang.upper()} title not available inside metadata for {pecha.id} for Serialization."
            )
            raise MetaDataMissingError(
                f"[Error] {lang.upper()} title not available inside metadata for {pecha.id} for Serialization."
            )

        return title

    def format_category(self, pecha: Pecha, category: Dict[str, List[Dict[str, str]]]):
        """
        Add Root section ie "རྩ་བ།" or "Root text" to category
        Add pecha title to category
        """
        bo_category, en_category = category["bo"], category["en"]
        bo_category.append(self.bo_root_category)
        en_category.append(self.en_root_category)

        bo_title = self.get_pecha_title(pecha, "bo")
        en_title = self.get_pecha_title(pecha, "en")

        bo_category.append({"name": bo_title, "heDesc": "", "heShortDesc": ""})
        en_category.append({"name": en_title, "enDesc": "", "enShortDesc": ""})

        return {"bo": bo_category, "en": en_category}

    def serialize(
        self,
        root_display_pecha: Pecha,
        root_pecha: Pecha,
        translation_pecha: Pecha,
        pecha_category: Dict[str, List[Dict[str, str]]],
    ) -> Dict:

        formatted_category = self.format_category(root_display_pecha, pecha_category)
        bo_category, en_category = formatted_category["bo"], formatted_category["en"]

        src_content = TranslationAlignmentTransfer().get_serialized_translation(
            root_display_pecha, root_pecha, translation_pecha
        )

        root_layer_path = get_first_layer_file(root_display_pecha)
        tgt_content = self.get_root_content(root_display_pecha, root_layer_path)

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
                    **self.get_metadata_for_pecha_org(root_display_pecha),
                    "content": chapterized_tgt_content,
                }
            ],
        }

        translation_metadata = self.get_metadata_for_pecha_org(translation_pecha)
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
