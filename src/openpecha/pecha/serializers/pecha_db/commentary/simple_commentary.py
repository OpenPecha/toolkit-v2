from typing import Any, Dict, Union

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import (
    MetaDataValidationError,
    PechaCategoryNotFoundError,
    RootPechaNotFoundError,
)
from openpecha.pecha import Pecha, get_anns, get_first_layer_file
from openpecha.pecha.metadata import PechaMetaData
from openpecha.utils import (
    chunk_strings,
    get_chapter_num_from_segment_num,
    get_text_direction_with_lang,
    process_segment_num_for_chapter,
)

logger = get_logger(__name__)


class SimpleCommentarySerializer:
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
        chapter_num = get_chapter_num_from_segment_num(root_map)

        processed_root_map = process_segment_num_for_chapter(root_map)
        if "root_idx_mapping" in ann:
            return f"<{chapter_num}><{processed_root_map}>{ann['text'].strip()}"
        return ann["text"].strip()

    def serialize(
        self,
        pecha: Pecha,
        root_title: str,
        commentary_pecha: Union[Pecha, None] = None,
    ):
        """
        Commentary Pecha can be i) Commentary Pecha ii) Translation of Commentary Pecha
        if Commentary Pecha,
            pecha: Commentary Pecha
            root_title: Root Pecha title
            commentary_pecha: None

        if Translation of Commentary Pecha,
            pecha: Translation of Commentary Pecha
            root_title: Root Pecha title
            commentary_pecha: Commentary Pecha

        Output: Serialized JSON of Commentary Pecha
        """

        src_book, tgt_book = [], []
        src_metadata, tgt_metadata = self.extract_metadata(pecha)
        src_book.append(src_metadata)
        tgt_book.append(tgt_metadata)

        src_category, tgt_category = self.get_categories(pecha, root_title)

        pecha_metadata = pecha.metadata.source_metadata

        if "translation_of" in pecha_metadata and pecha_metadata["translation_of"]:
            if not commentary_pecha or not isinstance(commentary_pecha, Pecha):
                logger.error(
                    "Root pecha is not passed during Commentary Translation Serialization."
                )
                raise RootPechaNotFoundError(
                    "Root pecha is not passed during Commentary Translation Serialization."
                )
            translation_path = get_first_layer_file(pecha)
            commentary_path = get_first_layer_file(commentary_pecha)
            src_content = self.get_content(pecha, translation_path)
            tgt_content = self.get_content(commentary_pecha, commentary_path)

            # Chapterize content
            src_content = chunk_strings(src_content)
            tgt_content = chunk_strings(tgt_content)
        else:
            tgt_layer_path = get_first_layer_file(pecha)
            src_content = []
            tgt_content = self.get_content(pecha, tgt_layer_path)

            # Chapterize content
            tgt_content = chunk_strings(tgt_content)

        src_book[0]["content"] = src_content
        tgt_book[0]["content"] = tgt_content

        serialized_json = {
            "source": {"categories": src_category, "books": src_book},
            "target": {"categories": tgt_category, "books": tgt_book},
        }
        logger.info(f"Pecha {pecha.id} is serialized successfully.")
        return serialized_json
