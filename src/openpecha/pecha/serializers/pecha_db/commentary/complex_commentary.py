from typing import Any, Dict, List

from pecha_org_tools.translation import (
    get_bo_content_translation,
    get_en_content_translation,
)

from openpecha.exceptions import MetaDataValidationError
from openpecha.pecha import Pecha
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.metadata import Language, PechaMetaData
from openpecha.utils import get_text_direction_with_lang


class ComplexCommentarySerializer:
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
            "language": metadata.language.value if metadata.language else "bo",
            "versionSource": metadata.source if metadata.source else "",
            "direction": get_text_direction_with_lang(metadata.language),
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

    def get_sapche_anns(self, pecha: Pecha):
        """
        Get the sapche annotations from the sapche layer,
        """
        sapche_anns = []
        basename = next(pecha.base_path.rglob("*.txt")).stem
        sapche_layer, _ = pecha.get_layer_by_ann_type(basename, AnnotationType.SAPCHE)
        for ann in sapche_layer:
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            # Get metadata of the annotation
            ann_metadata = {}
            for data in ann:
                ann_metadata[data.key().id()] = str(data.value())
            sapche_anns.append(
                {
                    "Span": {"start": start, "end": end},
                    "text": str(ann),
                    "sapche_number": ann_metadata["sapche_number"],
                }
            )

        return sapche_anns

    def get_meaning_segment_anns(self, pecha: Pecha):
        """
        Get the meaning segment annotations from the meaning segment layer,
        """
        meaning_segment_anns = []
        basename = next(pecha.base_path.rglob("*.txt")).stem
        meaning_segment_layer, _ = pecha.get_layer_by_ann_type(
            basename, AnnotationType.ALIGNMENT
        )
        for ann in meaning_segment_layer:
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            # Get metadata of the annotation
            ann_metadata = {}
            for data in ann:
                ann_metadata[data.key().id()] = str(data.value())

            curr_ann = {
                "Span": {"start": start, "end": end},
                "text": str(ann),
            }

            if "root_idx_mapping" in ann_metadata:
                curr_ann["root_idx_mapping"] = ann_metadata["root_idx_mapping"]

            meaning_segment_anns.append(curr_ann)

        return meaning_segment_anns

    def get_content(self, pecha: Pecha):
        """
        Prepare content in the sapche annotations to the required format(Tree like structure)
        """

        def format_tree(tree):
            """
            Format sapche ann which is in tree like structure to desired format
            """
            formatted_tree = {}

            # Iterate over each key in the tree dictionary
            for key, value in tree.items():
                # Create a new dictionary for the current node with 'title' and 'data'
                formatted_tree[value["title"]] = {
                    "data": value["data"],
                }

                # If there are children, process each child and add them as separate keys
                for child_key, child_value in value["children"].items():
                    child_formatted = format_tree(
                        {child_key: child_value}
                    )  # Recursively format the child
                    formatted_tree[value["title"]].update(child_formatted)

            return formatted_tree

        sapche_anns = self.get_sapche_anns(pecha)
        self.get_text_related_to_sapche(pecha, sapche_anns)

        formatted_sapche_anns: Dict[str, Any] = {}

        for sapche_ann in sapche_anns:
            keys = sapche_ann["sapche_number"].strip(".").split(".")
            current = formatted_sapche_anns
            for key in keys:
                if key not in current:
                    current[key] = {
                        "children": {},
                        "title": sapche_ann["text"],
                        "data": sapche_ann["meaning_segments"],
                    }
                current = current[key]["children"]

        return format_tree(formatted_sapche_anns)

    @staticmethod
    def format_commentary_segment_ann(ann: Dict[str, Any], chapter_num: int = 1) -> str:
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

    def get_text_related_to_sapche(self, pecha: Pecha, sapche_anns: List[Dict]):
        """
        Get the text related to the sapche annotations from meaning segment layer,
        and add to 'meaning_segments' key of sapche annotations
        """
        meaning_segment_anns = self.get_meaning_segment_anns(pecha)

        num_of_sapches = len(sapche_anns)
        for idx, sapche_ann in enumerate(sapche_anns):
            start = sapche_ann["Span"]["start"]
            end = sapche_ann["Span"]["end"]

            sapche_ann["meaning_segments"] = []

            # Determine the boundary for the next sapche annotation, if applicable
            next_start = (
                sapche_anns[idx + 1]["Span"]["start"]
                if idx < num_of_sapches - 1
                else None
            )

            for meaning_segment_ann in meaning_segment_anns:
                meaning_segment_start = meaning_segment_ann["Span"]["start"]
                meaning_segment_end = meaning_segment_ann["Span"]["end"]

                # Check if it's the last sapche annotation and include all meaning segments after it
                if next_start is None and meaning_segment_end >= end:
                    formatted_meaning_segment_ann = self.format_commentary_segment_ann(
                        meaning_segment_ann
                    )
                    sapche_ann["meaning_segments"].append(formatted_meaning_segment_ann)

                if next_start is None:
                    continue

                # Otherwise, include meaning segments between the current sapche and the next one
                if meaning_segment_start >= start and meaning_segment_end <= next_start:
                    formatted_meaning_segment_ann = self.format_commentary_segment_ann(
                        meaning_segment_ann
                    )
                    sapche_ann["meaning_segments"].append(formatted_meaning_segment_ann)

    def get_json_content(self, pecha: Pecha):
        """
        Fill the source and target content to the json format
        """
        content = self.get_content(pecha)

        bo_title = pecha.metadata.title.get("bo") or pecha.metadata.title.get("BO")

        pecha_lang = pecha.metadata.language

        if pecha_lang == Language.tibetan:
            pecha_lang = Language.english

        pecha_lang_lowercase = pecha_lang.value.lower()
        pecha_lang_uppercase = pecha_lang.value.upper()

        other_title = pecha.metadata.title.get(
            pecha_lang_lowercase
        ) or pecha.metadata.title.get(pecha_lang_uppercase)

        if pecha.metadata.language == Language.tibetan:
            src_content = {
                other_title: {
                    "data": [],
                    **get_en_content_translation(content),
                }
            }
            tgt_content = {bo_title: {"data": [], **content}}

        else:
            src_content = {other_title: {"data": [], **content}}
            tgt_content = {
                bo_title: {
                    "data": [],
                    **get_bo_content_translation(content),
                }
            }
        return (src_content, tgt_content)

    def serialize(
        self, pecha: Pecha, pecha_category: Dict[str, List[Dict]], root_title: str
    ):
        """
        Serialize the commentary pecha to json format
        """

        src_book, tgt_book = [], []
        src_metadata, tgt_metadata = self.extract_metadata(pecha)
        src_book.append(src_metadata)
        tgt_book.append(tgt_metadata)

        category = self.add_root_reference_to_category(pecha_category, root_title)
        src_category, tgt_category = category["en"], category["bo"]

        src_content, tgt_content = self.get_json_content(pecha)
        src_book[0]["content"] = src_content
        tgt_book[0]["content"] = tgt_content

        serialized_json = {
            "source": {"categories": src_category, "books": src_book},
            "target": {"categories": tgt_category, "books": tgt_book},
        }
        return serialized_json
