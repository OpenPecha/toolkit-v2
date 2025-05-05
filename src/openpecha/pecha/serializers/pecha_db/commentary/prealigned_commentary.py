from typing import Dict, List

from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.config import get_logger
from openpecha.pecha import Pecha
from openpecha.pecha.serializers.pecha_db.utils import (
    FormatPechaCategory,
    get_metadata_for_pecha_org,
    get_pecha_title,
)
from openpecha.utils import chunk_strings

logger = get_logger(__name__)


class PreAlignedCommentarySerializer:
    def serialize(
        self,
        root_pecha: Pecha,
        root_alignment_id: str,
        commentary_pecha: Pecha,
        commentary_alignment_id: str,
        pecha_category: List[Dict],
        commentary_segmentation_id: str | None = None,
    ):
        # Format Category
        root_title = get_pecha_title(root_pecha, "en")
        formatted_category = FormatPechaCategory().format_commentary_category(
            commentary_pecha, pecha_category, root_title
        )

        src_category, tgt_category = formatted_category["en"], formatted_category["bo"]
        logger.info(f"Category is extracted successfully for {commentary_pecha.id}.")

        # Get metadata
        src_metadata = get_metadata_for_pecha_org(commentary_pecha)
        tgt_metadata = get_metadata_for_pecha_org(commentary_pecha, "bo")

        # Get content
        src_content: List[List[str]] = []
        if commentary_segmentation_id:
            tgt_content = (
                CommentaryAlignmentTransfer().get_serialized_commentary_segmentation(
                    root_pecha,
                    root_alignment_id,
                    commentary_pecha,
                    commentary_alignment_id,
                    commentary_segmentation_id,
                )
            )
        else:
            tgt_content = CommentaryAlignmentTransfer().get_serialized_commentary(
                root_pecha, root_alignment_id, commentary_pecha, commentary_alignment_id
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
