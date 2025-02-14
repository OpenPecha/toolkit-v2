from pathlib import Path
from typing import Any, Dict

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.exceptions import MetaDataValidationError
from openpecha.pecha import Pecha, get_pecha_with_id
from openpecha.pecha.metadata import PechaMetaData
from openpecha.utils import get_text_direction_with_lang


class SimpleCommentarySerializer:
    def extract_metadata(self, pecha: Pecha):
        """
        Extract neccessary metadata from opf for serialization to json
        """
        metadata: PechaMetaData = pecha.metadata

        if not isinstance(metadata.title, dict):
            raise MetaDataValidationError(
                f"[Error] Commentary Pecha {pecha.id} has no English or Tibetan Title."
            )

        source_title = metadata.title.get("en") or metadata.title.get("EN")
        target_title = metadata.title.get("bo") or metadata.title.get("BO")

        src_metadata = {
            "title": source_title,
            "language": "en",
            "versionSource": metadata.source if metadata.source else "",
            "direction": get_text_direction_with_lang("en"),
            "completestatus": "done",
        }

        tgt_metadata = {
            "title": target_title,
            "language": metadata.language.value,
            "versionSource": metadata.source if metadata.source else "",
            "direction": get_text_direction_with_lang(metadata.language),
            "completestatus": "done",
        }

        return src_metadata, tgt_metadata

    def get_category(self, category_name: str):
        """
        Input: title: Title of the pecha commentary which will be used to get the category format
        Process: Get the category format from the pecha.org categorizer package
        """

        categorizer = CategoryExtractor()
        category = categorizer.get_category(category_name)
        return category

    def add_root_reference_to_category(self, category: Dict[str, Any], root_title: str):
        """
        Modify the category format to the required format for pecha.org commentary
        """
        last_bo_category = category["bo"][-1]
        last_en_category = category["en"][-1]

        last_bo_category["base_text_titles"] = [root_title]
        last_en_category["base_text_titles"] = [root_title]

        last_bo_category["base_text_mapping"] = "many_to_one"
        last_en_category["base_text_mapping"] = "many_to_one"

        last_bo_category["link"] = "Commentary"
        last_en_category["link"] = "Commentary"

        category["bo"][-1] = last_bo_category
        category["en"][-1] = last_en_category

        return category

    def get_categories(self, pecha: Pecha, root_title: str):
        """
        Set the category format to self.category attribute
        """

        title = pecha.metadata.title.get("bo") or pecha.metadata.title.get("BO")
        category = self.get_category(title)
        category = self.add_root_reference_to_category(category, root_title)

        return (category["en"], category["bo"])  # source and target category

    def get_content(self, pecha: Pecha):
        """
        Prepare content in the sapche annotations to the required format(Tree like structure)
        """

        segment_layer = AnnotationStore(
            file=str(next(pecha.layer_path.rglob("*.json")))
        )
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
        if "root_idx_mapping" in ann:
            return f"<{chapter_num}><{ann['root_idx_mapping']}>{ann['text'].strip()}"
        return ann["text"].strip()

    def serialize(self, pecha_path: Path, root_title: str):
        """
        Serialize the commentary pecha to json format
        """

        pecha = Pecha.from_path(pecha_path)

        src_book, tgt_book = [], []
        src_metadata, tgt_metadata = self.extract_metadata(pecha)
        src_book.append(src_metadata)
        tgt_book.append(tgt_metadata)

        src_category, tgt_category = self.get_categories(pecha, root_title)

        if "translation_of" in pecha.metadata.source_metadata:
            src_content = self.get_content(pecha)
            root_pecha = get_pecha_with_id(
                pecha.metadata.source_metadata["translation_of"]
            )
            tgt_content = self.get_content(root_pecha)
        else:

            src_content = []
            tgt_content = self.get_content(pecha)
        src_book[0]["content"] = src_content
        tgt_book[0]["content"] = tgt_content

        serialized_json = {
            "source": {"categories": src_category, "book": src_book},
            "target": {"categories": tgt_category, "book": tgt_book},
        }
        return serialized_json


def get_anns(ann_store: AnnotationStore):
    anns = []
    for ann in ann_store:
        ann_data = {}
        for data in ann:
            ann_data[data.key().id()] = data.value().get()
        curr_ann = {**ann_data, "text": str(ann)}
        anns.append(curr_ann)
    return anns
