import re
from typing import Dict, List, Optional, Tuple

from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer
from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns, load_layer
from openpecha.pecha.serializers.pecha_db.utils import (
    FormatPechaCategory,
    get_metadata_for_pecha_org,
    get_pecha_title,
)
from openpecha.utils import chunk_strings

logger = get_logger(__name__)


class PreAlignedCommentaryTranslationSerializer:
    def __init__(self):
        self.map_regex = r"^<(\d+)><(\d+)>"

    def extract_mapping(self, segments: List[str]):
        """
        Get Chapter information with segment number.
        2.Loop throught chapters
        3.Get chapter number and segment number
        """
        map: List[Optional[Tuple[int, int]]] = []
        for segment in segments:
            match = re.match(self.map_regex, segment)
            if match:
                chapter = int(match.group(1))
                segment_num = int(match.group(2))
                map.append((chapter, segment_num))
            else:
                map.append(None)
        return map

    def add_mapping_to_anns(
        self, anns: List[str], map: List[Optional[Tuple[int, int]]]
    ):
        for i, (ann, mapping) in enumerate(zip(anns, map)):
            if mapping:
                anns[i] = f"<{mapping[0]}><{mapping[1]}> {ann}"
        return anns

    def serialize(
        self,
        root_pecha: Pecha,
        root_alignment_id: str,
        commentary_pecha: Pecha,
        commentary_alignment_id: str,
        translation_pecha: Pecha,
        translation_alignment_id: str,
        pecha_category: List[Dict],
    ):
        # Format Category
        root_title = get_pecha_title(root_pecha, "en")
        formatted_category = FormatPechaCategory().format_commentary_category(
            commentary_pecha, pecha_category, root_title
        )

        src_category, tgt_category = formatted_category["en"], formatted_category["bo"]
        logger.info(f"Category is extracted successfully for {commentary_pecha.id}.")

        # Get metadata
        src_metadata = get_metadata_for_pecha_org(translation_pecha)
        tgt_metadata = get_metadata_for_pecha_org(commentary_pecha, "bo")
        logger.info(
            f"Pecha {commentary_pecha.id} Metadata successfully prepared for pecha.org website."
        )

        # Get content
        tgt_content = CommentaryAlignmentTransfer().get_serialized_commentary(
            root_pecha, root_alignment_id, commentary_pecha, commentary_alignment_id
        )

        map = self.extract_mapping(tgt_content)
        translation_anns = get_anns(
            load_layer(translation_pecha.layer_path / translation_alignment_id)
        )
        src_content = [ann["text"] for ann in translation_anns]
        src_content = self.add_mapping_to_anns(src_content, map)

        logger.info(
            f"Alignment transfered content is extracted successfully for {commentary_pecha.id}."
        )
        # Preprocess newlines in content
        tgt_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in tgt_content
        ]
        src_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in src_content
        ]

        # Chapterize content
        chapterized_tgt_content = chunk_strings(tgt_content)
        chapterized_src_content = chunk_strings(src_content)

        serialized_json = {
            "source": {
                "categories": src_category,
                "books": [{**src_metadata, "content": chapterized_src_content}],
            },
            "target": {
                "categories": tgt_category,
                "books": [{**tgt_metadata, "content": chapterized_tgt_content}],
            },
        }
        logger.info(f"Pecha {commentary_pecha.id} is serialized successfully.")
        return serialized_json
