from pathlib import Path
from typing import Any, Dict, Union

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.utils import get_text_direction_with_lang


class CommentarySerializer:
    def __init__(self):
        self.category = []
        self.book = []
        self.book_content = {}
        self.required_metadata = {}
        self.sapche_anns = []
        self.meaning_segment_anns = []

        self.pecha_path: Union[Path, None] = None
        self.pecha: Union[Pecha, None] = None

    def extract_metadata(self):
        """
        Extract neccessary metadata from opf for serialization to json
        """
        assert self.pecha is not None, "Pecha object is not set"
        pecha_metadata = self.pecha.metadata
        title = pecha_metadata.title
        lang = pecha_metadata.language
        title = title if lang in ["bo", "en"] else f"{title}[{lang}]"
        self.required_metadata = {
            "title": title,
            "language": pecha_metadata.language,
            "versionSource": pecha_metadata.source if pecha_metadata.source else "",
            "direction": get_text_direction_with_lang(pecha_metadata.language),
            "completestatus": "done",
        }
        return self.required_metadata

    def set_metadata_to_json(self):
        """
        Set extracted metadata to json format
        """
        self.extract_metadata()
        self.book.append(self.required_metadata)

    def get_category(self, title: str):
        """
        Input: title: Title of the pecha commentary which will be used to get the category format
        Process: Get the category format from the pecha.org categorizer package
        """
        pass

    def set_category_to_json(self):
        """
        Set the category format to self.category attribute
        """
        self.get_category(self.required_metadata["title"])
        pass

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
        self.get_sapche_anns()
        self.get_text_related_to_sapche()

        formatted_sapche_anns: Dict[str, Any] = {}

        for sapche_ann in self.sapche_anns:
            keys = sapche_ann["sapche_number"].strip(".").split(".")
            curr_sapche_ann = formatted_sapche_anns
            for key in keys:
                if key not in curr_sapche_ann:
                    curr_sapche_ann[key] = {"children": {}, "title": sapche_ann["text"]}
                curr_sapche_ann = curr_sapche_ann[key]["children"]

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

    def serialize(self, pecha_path: Path, title: str):
        """
        Serialize the commentary pecha to json format
        """
        self.pecha_path = pecha_path
        self.pecha = Pecha.from_path(pecha_path)

        self.set_metadata_to_json()
        self.set_category_to_json()
        self.format_sapche_anns()
        # serialize to json
        pass
