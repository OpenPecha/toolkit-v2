from typing import Any, Dict, List, Union

from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError
from openpecha.pecha import Pecha, get_anns
from openpecha.utils import (
    chunk_strings,
    get_chapter_num_from_segment_num,
    get_text_direction_with_lang,
    process_segment_num_for_chapter,
)

logger = get_logger(__name__)


class SimpleCommentarySerializer:
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
        pecha: Pecha,
        pecha_category: Dict[str, List[Dict]],
        root_title: str,
        translation_pecha: Union[Pecha, None] = None,
    ):
        src_book, tgt_book = [], []

        if translation_pecha:

            src_metadata = self.get_metadata_for_pecha_org(translation_pecha)
            tgt_metadata = self.get_metadata_for_pecha_org(pecha, "bo")

            translation_path = translation_pecha.get_segmentation_layer_path()
            commentary_path = pecha.get_segmentation_layer_path()
            src_content = self.get_content(translation_pecha, translation_path)
            tgt_content = self.get_content(pecha, commentary_path)
        else:
            layer_path = pecha.get_segmentation_layer_path()
            content = self.get_content(pecha, layer_path)
            if pecha.metadata.language.value == "bo":
                src_metadata = self.get_metadata_for_pecha_org(pecha, "en")
                tgt_metadata = self.get_metadata_for_pecha_org(pecha, "bo")

                src_content = []
                tgt_content = content
            else:
                src_metadata = self.get_metadata_for_pecha_org(pecha)
                tgt_metadata = self.get_metadata_for_pecha_org(pecha, "bo")

                tgt_content = []
                src_content = content

        src_book.append(src_metadata)
        tgt_book.append(tgt_metadata)

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

        src_book[0]["content"] = src_content
        tgt_book[0]["content"] = tgt_content

        formatted_category = self.format_category(pecha, pecha_category)
        formatted_category = self.add_root_reference_to_category(
            formatted_category, root_title
        )
        src_category, tgt_category = formatted_category["en"], formatted_category["bo"]

        serialized_json = {
            "source": {"categories": src_category, "books": src_book},
            "target": {"categories": tgt_category, "books": tgt_book},
        }
        logger.info(f"Pecha {pecha.id} is serialized successfully.")
        return serialized_json
