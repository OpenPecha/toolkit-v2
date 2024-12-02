from pathlib import Path
from typing import Any, Dict, Union

from pecha_org_tools.enums import TextType
from pecha_org_tools.extract import CategoryExtractor

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.utils import get_text_direction_with_lang


class CommentarySerializer:
    def __init__(self):
        self.source_category = {}
        self.target_category = {}
        self.source_book = []
        self.target_book = []

        self.sapche_anns = []
        self.meaning_segment_anns = []
        self.formatted_sapche_anns = {}

        self.bo_root_title: Union[str, None] = None
        self.en_root_title: Union[str, None] = None
        self.pecha_path: Union[Path, None] = None
        self.pecha: Union[Pecha, None] = None

    def extract_metadata(self):
        """
        Extract neccessary metadata from opf for serialization to json
        """
        assert self.pecha is not None, "Pecha object is not set"
        pecha_metadata = self.pecha.metadata
        source_title = pecha_metadata.title["en"]
        target_title = pecha_metadata.title["bo"]

        source_metadata = {
            "title": source_title,
            "language": "en",
            "versionSource": pecha_metadata.source if pecha_metadata.source else "",
            "direction": get_text_direction_with_lang("en"),
            "completestatus": "done",
        }

        target_metadata = {
            "title": target_title,
            "language": pecha_metadata.language.value,
            "versionSource": pecha_metadata.source if pecha_metadata.source else "",
            "direction": get_text_direction_with_lang(pecha_metadata.language),
            "completestatus": "done",
        }

        return source_metadata, target_metadata

    def set_metadata_to_json(self):
        """
        Set extracted metadata to json format
        """
        source_metadata, target_metadata = self.extract_metadata()
        self.source_book.append(source_metadata)
        self.target_book.append(target_metadata)

    def get_category(self, category_name: str):
        """
        Input: title: Title of the pecha commentary which will be used to get the category format
        Process: Get the category format from the pecha.org categorizer package
        """
        assert self.pecha is not None, "Pecha object is not set"

        if isinstance(self.pecha.metadata.title, dict):
            bo_title = self.pecha.metadata.title.get("bo", "")
            en_title = self.pecha.metadata.title.get("en", "")

        elif isinstance(self.pecha.metadata.title, list):
            bo_title = self.pecha.metadata.title[0]
            en_title = self.pecha.metadata.title[1]

        else:
            bo_title = self.pecha.metadata.title
            en_title = self.pecha.metadata.title

        heDesc = self.pecha.metadata.source_metadata.get("heDesc", "")
        heShortDesc = self.pecha.metadata.source_metadata.get("heShortDesc", "")

        enDesc = self.pecha.metadata.source_metadata.get("enDesc", "")
        enShortDesc = self.pecha.metadata.source_metadata.get("enShortDesc", "")

        pecha_metadata = {
            "bo": {
                "title": bo_title,
                "heDesc": heDesc,
                "heShortDesc": heShortDesc,
            },
            "en": {
                "title": en_title,
                "enDesc": enDesc,
                "enShortDesc": enShortDesc,
            },
        }

        categorizer = CategoryExtractor()
        category_json = categorizer.get_category(
            category_name, pecha_metadata, TextType.COMMENTARY
        )
        return category_json

    def modify_category(self, category_json: Dict[str, Any]):
        """
        Modify the category format to the required format for pecha.org commentary
        """
        last_bo_category = category_json["bo"][-1]
        last_en_category = category_json["en"][-1]

        last_bo_category["base_text_titles"] = [self.bo_root_title]
        last_en_category["base_text_titles"] = [self.en_root_title]

        last_bo_category["base_text_mapping"] = "many_to_one"
        last_en_category["base_text_mapping"] = "many_to_one"

        last_bo_category["link"] = "Commentary"
        last_en_category["link"] = "Commentary"

        category_json["bo"][-1] = last_bo_category
        category_json["en"][-1] = last_en_category

        return category_json

    def set_category_to_json(self, category_name: str):
        """
        Set the category format to self.category attribute
        """
        category_json = self.get_category(category_name)
        category_json = self.modify_category(category_json)

        self.source_category = category_json["en"]
        self.target_category = category_json["bo"]

    def get_sapche_anns(self):
        """
        Get the sapche annotations from the sapche layer,
        and store it in self.sapche_anns attribute
        """
        assert self.pecha is not None, "Pecha object is not set"
        basename = next(self.pecha.base_path.rglob("*.txt")).stem
        sapche_layer, _ = self.pecha.get_layer(basename, LayerEnum.sapche)
        for ann in sapche_layer:
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            # Get metadata of the annotation
            ann_metadata = {}
            for data in ann:
                ann_metadata[data.key().id()] = str(data.value())
            self.sapche_anns.append(
                {
                    "Span": {"start": start, "end": end},
                    "text": str(ann),
                    "sapche_number": ann_metadata["sapche_number"],
                }
            )

        return self.sapche_anns

    def get_meaning_segment_anns(self):
        """
        Get the meaning segment annotations from the meaning segment layer,
        and store it in self.meaning_segment_anns attribute
        """
        assert self.pecha is not None, "Pecha object is not set"
        basename = next(self.pecha.base_path.rglob("*.txt")).stem
        meaning_segment_layer, _ = self.pecha.get_layer(
            basename, LayerEnum.meaning_segment
        )
        for ann in meaning_segment_layer:
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            # Get metadata of the annotation
            ann_metadata = {}
            for data in ann:
                ann_metadata[data.key().id()] = str(data.value())

            curr_meaining_segment_ann = {
                "Span": {"start": start, "end": end},
                "text": str(ann),
            }

            if "root_idx_mapping" in ann_metadata:
                curr_meaining_segment_ann["root_idx_mapping"] = ann_metadata[
                    "root_idx_mapping"
                ]

            self.meaning_segment_anns.append(curr_meaining_segment_ann)

        return self.meaning_segment_anns

    def format_sapche_anns(self):
        """
        Format the sapche annotations to the required format(Tree like structure)
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

        self.get_sapche_anns()
        self.get_text_related_to_sapche()

        formatted_sapche_anns: Dict[str, Any] = {}

        for sapche_ann in self.sapche_anns:
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

        self.formatted_sapche_anns = format_tree(formatted_sapche_anns)
        return self.formatted_sapche_anns

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

    def get_text_related_to_sapche(self):
        """
        Get the text related to the sapche annotations from meaning segment layer,
        and add to 'meaning_segments' key of sapche annotations
        """
        self.get_meaning_segment_anns()

        num_of_sapches = len(self.sapche_anns)
        for idx, sapche_ann in enumerate(self.sapche_anns):
            start = sapche_ann["Span"]["start"]
            end = sapche_ann["Span"]["end"]

            sapche_ann["meaning_segments"] = []

            # Determine the boundary for the next sapche annotation, if applicable
            next_start = (
                self.sapche_anns[idx + 1]["Span"]["start"]
                if idx < num_of_sapches - 1
                else None
            )

            for meaning_segment_ann in self.meaning_segment_anns:
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

    def serialize(
        self,
        pecha_path: Path,
        category_name: str,
        bo_root_title: str,
        en_root_title: str,
    ):
        """
        Serialize the commentary pecha to json format
        """
        self.bo_root_title = bo_root_title
        self.en_root_title = en_root_title

        self.pecha_path = pecha_path
        self.pecha = Pecha.from_path(pecha_path)

        self.set_metadata_to_json()
        self.set_category_to_json(category_name)
        formatted_sapche_ann = self.format_sapche_anns()

        self.source_book[0]["content"] = {}
        self.target_book[0]["content"] = formatted_sapche_ann

        serialized_json = {
            "source": {"categories": self.source_category, "book": self.source_book},
            "target": {"categories": self.target_category, "book": self.target_book},
        }
        return serialized_json
