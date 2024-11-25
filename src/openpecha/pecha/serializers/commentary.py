from pathlib import Path
from typing import Any, Dict

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

    def extract_metadata(self, pecha_path: Path):
        """
        Extract neccessary metadata from opf for serialization to json
        """
        pecha = Pecha.from_path(pecha_path)
        pecha_metadata = pecha.metadata
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

    def set_metadata_to_json(self, pecha_path: Path):
        """
        Set extracted metadata to json format
        """
        self.extract_metadata(pecha_path)
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

    def get_sapche_anns(self, pecha_path: Path):
        """
        Get the sapche annotations from the sapche layer
        """
        pecha = Pecha.from_path(pecha_path)
        basename = next(pecha.base_path.rglob("*.txt")).stem
        sapche_layer, _ = pecha.get_layer(basename, LayerEnum.sapche)
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

    def format_sapche_anns(self, pecha_path: Path):
        """
        Format the sapche annotations to the required format(Tree like structure)
        """
        self.get_sapche_anns(pecha_path)
        self.get_text_related_to_sapche(pecha_path)

        formatted_sapche_anns: Dict[str, Any] = {}

        for sapche_ann in self.sapche_anns:
            keys = sapche_ann["sapche_number"].strip(".").split(".")
            curr_sapche_ann = formatted_sapche_anns
            for key in keys:
                if key not in curr_sapche_ann:
                    curr_sapche_ann[key] = {"children": {}, "title": sapche_ann["text"]}
                curr_sapche_ann = curr_sapche_ann[key]["children"]

        pass

    def get_text_related_to_sapche(self, pecha_path: Path):
        """
        Get the text related to the sapche annotations from meaning segment layer
        """

        num_of_sapches = len(self.sapche_anns)
        for idx, sapche_ann in enumerate(self.sapche_anns):
            start = sapche_ann["Span"]["start"]  # noqa
            end = sapche_ann["Span"]["end"]  # noqa

            if idx == num_of_sapches - 1:
                continue

            next_start = self.sapche_anns[idx + 1]["Span"]["start"]  # noqa

        pass

    def serialize(self, pecha_path: Path, title: str):
        """
        Serialize the commentary pecha to json format
        """
        self.set_metadata_to_json(pecha_path)
        self.set_category_to_json()
        self.format_sapche_anns(pecha_path)
        # serialize to json
        pass
