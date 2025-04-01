from typing import Any, Dict, List

from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.config import get_logger
from openpecha.exceptions import MetaDataValidationError
from openpecha.pecha import Pecha
from openpecha.pecha.metadata import PechaMetaData
from openpecha.pecha.serializers.pecha_db.utils import (
    get_metadata_for_pecha_org,
    get_pecha_title,
)
from openpecha.utils import chunk_strings

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

    def format_category(self, pecha: Pecha, category: Dict[str, List[Dict[str, str]]]):
        """
        Add Commentary section ie "འགྲེལ་བ།" or "Commentary text" to category
        Add pecha title to category
        """

        category["bo"].append(self.bo_commentary_category)
        category["en"].append(self.en_commentary_category)

        bo_title = get_pecha_title(pecha, "bo")
        en_title = get_pecha_title(pecha, "en")

        category["bo"].append({"name": bo_title, "heDesc": "", "heShortDesc": ""})
        category["en"].append({"name": en_title, "enDesc": "", "enShortDesc": ""})

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
        src_metadata = get_metadata_for_pecha_org(commentary_pecha)
        tgt_metadata = get_metadata_for_pecha_org(commentary_pecha, "bo")

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
