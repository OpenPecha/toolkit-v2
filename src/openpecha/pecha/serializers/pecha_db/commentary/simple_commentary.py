from typing import Any, Dict, List

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.serializers.pecha_db.utils import (
    FormatPechaCategory,
    get_metadata_for_pecha_org,
)
from openpecha.utils import (
    adjust_segment_num_for_chapter,
    chunk_strings,
    get_chapter_for_segment,
)

logger = get_logger(__name__)


class SimpleCommentarySerializer:
    def get_content(self, pecha: Pecha, layer_path: str):
        """
        Prepare content in the sapche annotations to the required format(Tree like structure)
        """
        ann_layer_path = pecha.pecha_path.parent.joinpath(layer_path)
        if not ann_layer_path.exists():
            logger.error(f"The layer path {str(ann_layer_path)} does not exist.")
            raise FileNotFoundError(
                f"[Error] The layer path '{str(ann_layer_path)}' does not exist."
            )
        segment_layer = AnnotationStore(file=str(ann_layer_path))

        anns = get_anns(segment_layer)
        contents = [self.format_commentary_ann(ann) for ann in anns]
        return contents

    @staticmethod
    def format_commentary_ann(ann: Dict[str, Any], chapter_num: int = 1) -> str:
        """
        Format the commentary meaning segment annotation to the required format
        Input: ann: meaning segment annotation
        Required Format:
        <a><b>Text, where a is chapter number, b is root mapping number,
                    and Text is the meaning segment text

                    If root mapping number is not available, then just return the text
        Output Format: string
        """
        root_map = int(ann["root_idx_mapping"])
        chapter_num = get_chapter_for_segment(root_map)

        processed_root_map = adjust_segment_num_for_chapter(root_map)
        if "root_idx_mapping" in ann:
            return f"<{chapter_num}><{processed_root_map}>{ann['text'].strip()}"
        return ann["text"].strip()

    def serialize(
        self,
        pecha: Pecha,
        annotation_path: str,
        pecha_category: List[Dict],
        root_title: str,
        translation_pecha: Pecha | None = None,
        translation_ann_path: str | None = None,
    ):
        # Format Category
        formatted_category = FormatPechaCategory().format_commentary_category(
            pecha, pecha_category, root_title
        )
        src_category, tgt_category = formatted_category["en"], formatted_category["bo"]

        # Get the metadata for Commentary and Commentary Translation pecha
        if translation_pecha:
            src_metadata = get_metadata_for_pecha_org(translation_pecha)
            tgt_metadata = get_metadata_for_pecha_org(pecha, "bo")
        else:
            if pecha.metadata.language.value == "bo":
                src_metadata = get_metadata_for_pecha_org(pecha, "en")
                tgt_metadata = get_metadata_for_pecha_org(pecha, "bo")
            else:
                src_metadata = get_metadata_for_pecha_org(pecha)
                tgt_metadata = get_metadata_for_pecha_org(pecha, "bo")

        # Get the metadata for Commentary and Commentary Translation pecha
        if translation_pecha:

            src_metadata = get_metadata_for_pecha_org(translation_pecha)
            tgt_metadata = get_metadata_for_pecha_org(pecha, "bo")

            src_content = self.get_content(
                translation_pecha, translation_pecha.layer_path / translation_ann_path
            )
            tgt_content = self.get_content(pecha, pecha.layer_path / annotation_path)
        else:
            content = self.get_content(pecha, pecha.layer_path / annotation_path)
            if pecha.metadata.language.value == "bo":
                src_content = []
                tgt_content = content
            else:
                tgt_content = []
                src_content = content

        # Preprocess newlines in content
        src_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in src_content
        ]
        tgt_content = [
            line.replace("\\n", "<br>").replace("\n", "<br>") for line in tgt_content
        ]

        # Chapterize content
        src_content = chunk_strings(src_content)
        tgt_content = chunk_strings(tgt_content)

        commentary_json = {
            "categories": tgt_category,
            "books": [{**tgt_metadata, "content": tgt_content}],
        }

        translation_json = {
            "categories": src_category,
            "books": [{**src_metadata, "content": src_content}],
        }

        serialized_json = {
            "source": translation_json,
            "target": commentary_json,
        }
        logger.info(f"Pecha {pecha.id} is serialized successfully.")
        return serialized_json
