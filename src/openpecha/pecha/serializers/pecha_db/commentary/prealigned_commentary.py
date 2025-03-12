from typing import Any, Dict, List

from pecha_org_tools.extract import CategoryExtractor

from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.config import get_logger
from openpecha.exceptions import MetaDataValidationError, PechaCategoryNotFoundError
from openpecha.pecha import Pecha
from openpecha.pecha.metadata import PechaMetaData
from openpecha.utils import chunk_strings, get_text_direction_with_lang

logger = get_logger(__name__)


class PreAlignedCommentarySerializer:
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

    def get_category(self, category_name: str):
        """
        Input: title: Title of the pecha commentary which will be used to get the category format
        Process: Get the category format from the pecha.org categorizer package
        """

        try:
            categorizer = CategoryExtractor()
            category = categorizer.get_category(category_name)
        except Exception as e:
            logger.error(
                f"Category not found for pecha title: {category_name}. {str(e)}"
            )
            raise PechaCategoryNotFoundError(
                f"Category not found for pecha title: {category_name}. {str(e)}"
            )
        return category

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

    def get_categories(self, pecha: Pecha, root_title: str):
        """
        Set the category format to self.category attribute
        """

        title = pecha.metadata.title.get("bo") or pecha.metadata.title.get("BO")
        category = self.get_category(title)
        category = self.add_root_reference_to_category(category, root_title)

        return (category["en"], category["bo"])  # source and target category

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

    def serialize(
        self, root_display_pecha: Pecha, root_pecha: Pecha, commentary_pecha: Pecha
    ):
        src_book, tgt_book = [], []
        src_metadata, tgt_metadata = self.extract_metadata(commentary_pecha)
        src_book.append(src_metadata)
        tgt_book.append(tgt_metadata)

        root_en_title = self.get_pecha_en_title(root_display_pecha)
        src_category, tgt_category = self.get_categories(
            commentary_pecha, root_en_title
        )
        logger.info(f"Category is extracted successfully for {commentary_pecha.id}.")

        src_content: List[List[str]] = []
        tgt_content = CommentaryAlignmentTransfer().get_serialized_commentary(
            root_display_pecha, root_pecha, commentary_pecha
        )

        # Chapterize content
        chapterized_tgt_content = chunk_strings(tgt_content)
        logger.info(
            f"Alignment transfered content is extracted successfully for {commentary_pecha.id}."
        )

        src_book[0]["content"] = src_content
        tgt_book[0]["content"] = chapterized_tgt_content

        serialized_json = {
            "source": {"categories": src_category, "books": src_book},
            "target": {"categories": tgt_category, "books": tgt_book},
        }
        logger.info(f"Pecha {commentary_pecha.id} is serialized successfully.")
        return serialized_json
