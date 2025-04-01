from typing import Any, Dict, List

from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError, MetaDataValidationError
from openpecha.pecha import Pecha
from openpecha.pecha.metadata import PechaMetaData
from openpecha.utils import chunk_strings, get_text_direction_with_lang

logger = get_logger(__name__)


class PreAlignedCommentarySerializer:
    def __init__(self):
        self.bo_commentary_category = {
            "name": "འགྲེལ་བ།",
            "heDesc": "",
            "heShortDesc": "",
        }
        self.en_commentary_category = {
            "name": "Commentary text",
            "enDesc": "",
            "enShortDesc": "",
        }

    def extract_metadata(self, pecha: Pecha):
        """
        Extract neccessary metadata from opf for serialization to json
        """
        metadata: PechaMetaData = pecha.metadata

        if not isinstance(metadata.title, dict):
            logger.error(f"Title is not available in the Commentary Pecha {pecha.id}.")
            raise MetaDataValidationError(
                f"[Error] Commentary Pecha {pecha.id} has no English or Tibetan Title."
            )

        pecha_lang = pecha.metadata.language.value
        src_lang = "en" if pecha_lang == "bo" else pecha_lang
        source_title = metadata.title.get(src_lang.lower()) or metadata.title.get(
            src_lang.upper()
        )
        source_title = (
            source_title if src_lang == "en" else f"{source_title}[{src_lang}]"
        )
        target_lang = "bo"
        target_title = metadata.title.get(target_lang.lower()) or metadata.title.get(
            target_lang.upper()
        )

        src_metadata = {
            "title": source_title,
            "language": src_lang,
            "versionSource": metadata.source if metadata.source else "",
            "direction": get_text_direction_with_lang("en"),
            "completestatus": "done",
        }

        tgt_metadata = {
            "title": target_title,
            "language": target_lang,
            "versionSource": metadata.source if metadata.source else "",
            "direction": get_text_direction_with_lang("bo"),
            "completestatus": "done",
        }

        return src_metadata, tgt_metadata

    def add_root_reference_to_category(self, category: Dict[str, Any], root_title: str):
        """
        Modify the category format to the required format for pecha.org commentary
        """
        for lang in ["bo", "en"]:
            last_category = category[lang][-1]
            last_category.update(
                {
                    "base_text_titles": [root_title],
                    "base_text_mapping": "many_to_one",
                    "link": "Commentary",
                }
            )
        return category

    def get_pecha_en_title(self, pecha: Pecha):
        metadata: PechaMetaData = pecha.metadata

        if not isinstance(metadata.title, dict):
            logger.error(
                f"Title data type is not dictionary in the Root Pecha {pecha.id}."
            )
            raise MetaDataValidationError(
                f"[Error] Root Pecha {pecha.id} title data type is not dictionary."
            )

        if "en" not in metadata.title and "EN" not in metadata.title:
            logger.error(
                f"English title is not available in the Root Pecha {pecha.id}."
            )
            raise MetaDataValidationError(
                f"[Error] Root Pecha {pecha.id} has no English Title."
            )

        root_en_title = metadata.title.get("en") or metadata.title.get("EN")
        return root_en_title

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
        Add Commentary section ie "འགྲེལ་བ།" or "Commentary text" to category
        Add pecha title to category
        """

        category["bo"].append(self.bo_commentary_category)
        category["en"].append(self.en_commentary_category)

        bo_title = self.get_pecha_title(pecha, "bo")
        en_title = self.get_pecha_title(pecha, "en")

        category["bo"].append({"name": bo_title, "heDesc": "", "heShortDesc": ""})
        category["en"].append({"name": en_title, "enDesc": "", "enShortDesc": ""})

        return category

    def serialize(
        self,
        root_display_pecha: Pecha,
        root_pecha: Pecha,
        commentary_pecha: Pecha,
        pecha_category: Dict[str, List[Dict[str, str]]],
    ):
        # Format Category
        formatted_category = self.format_category(commentary_pecha, pecha_category)

        root_en_title = self.get_pecha_en_title(root_display_pecha)
        category = self.add_root_reference_to_category(
            formatted_category, root_en_title
        )
        src_category, tgt_category = category["en"], category["bo"]
        logger.info(f"Category is extracted successfully for {commentary_pecha.id}.")

        # Get metadata
        src_metadata, tgt_metadata = self.extract_metadata(commentary_pecha)

        # Get content
        src_content: List[List[str]] = []
        tgt_content = CommentaryAlignmentTransfer().get_serialized_commentary(
            root_display_pecha, root_pecha, commentary_pecha
        )
        # Preprocess newlines in content
        tgt_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in tgt_content
        ]

        # Chapterize content
        chapterized_tgt_content = chunk_strings(tgt_content)
        logger.info(
            f"Alignment transfered content is extracted successfully for {commentary_pecha.id}."
        )

        serialized_json = {
            "source": {
                "categories": src_category,
                "books": [{**src_metadata, "content": src_content}],
            },
            "target": {
                "categories": tgt_category,
                "books": [{**tgt_metadata, "content": chapterized_tgt_content}],
            },
        }
        logger.info(f"Pecha {commentary_pecha.id} is serialized successfully.")
        return serialized_json
