from pathlib import Path
from typing import Dict, List

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH, _mkdir_if_not
from openpecha.pecha import Pecha
from openpecha.utils import get_text_direction_with_lang, write_json


class SimpleTextTranslationSerializer(BaseAlignmentSerializer):
    def __init__(self):
        self.root_json: Dict[str, List] = {
            "categories": [],
            "books": [],
        }
        self.translation_json: Dict[str, List] = {
            "categories": [],
            "books": [],
        }

    def set_pecha_category(self, category: str):
        """
        Set pecha category both in english and tibetan in the JSON output.
        """
        category_extractor = CategoryExtractor()
        categories = category_extractor.get_category(category)
        self.root_json["categories"] = categories["bo"]
        self.translation_json["categories"] = categories["en"]

    def extract_metadata(self, pecha: Pecha):
        """
        Extract required metadata from opf
        """
        lang = pecha.metadata.language.value
        direction = get_text_direction_with_lang(lang)
        title = pecha.metadata.title
        if isinstance(title, dict):
            title = title.get(lang.lower()) or title.get(lang.upper())
        title = title if lang in ["bo", "en"] else f"{title}[{lang}]"
        source = pecha.metadata.source if pecha.metadata.source else ""

        return {
            "title": title,
            "language": lang,
            "versionSource": source,
            "direction": direction,
            "completestatus": "done",
        }

    def set_root_metadata(self, root_opf_path: Path):
        """
        Set tibetan text metadata to root json
        """
        root_pecha = Pecha.from_path(root_opf_path)
        self.root_json["books"].append(self.extract_metadata(root_pecha))

    def set_translation_metadata(self, translation_opf_path: Path):
        """
        Set English, Chinese, etc. text metadata to translation json
        """
        translation_pecha = Pecha.from_path(translation_opf_path)
        self.translation_json["books"].append(self.extract_metadata(translation_pecha))

    @staticmethod
    def get_texts_from_layer(layer: AnnotationStore):
        """
        Extract texts from layer
        1.If text is a newline, replace it with empty string
        2.Replace newline with <br>
        """
        return [
            "" if str(ann) == "\n" else str(ann).replace("\n", "<br>") for ann in layer
        ]

    def set_root_content(self, root_opf_path: Path, base_name: str, layer_name: str):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """
        pecha = Pecha.from_path(root_opf_path)
        segment_layer = AnnotationStore(
            file=pecha.layer_path.joinpath(base_name, layer_name).as_posix()
        )
        segment_texts = self.get_texts_from_layer(segment_layer)
        self.root_json["books"][0]["content"] = [segment_texts]

    def set_translation_content(
        self, translation_opf_path: Path, base_name: str, layer_name: str
    ):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """
        pecha = Pecha.from_path(translation_opf_path)
        segment_layer = AnnotationStore(
            file=pecha.layer_path.joinpath(base_name, layer_name).as_posix()
        )
        segment_texts = self.get_texts_from_layer(segment_layer)
        self.translation_json["books"][0]["content"] = [segment_texts]

    def get_pecha_display_aligment(self, translation_opf: Path):
        """
        Get the source and target layer from the translation opf
        """
        pecha = Pecha.from_path(translation_opf)
        pecha_display_alignment = pecha.metadata.source_metadata[
            "pecha_display_segment_alignments"
        ][0]
        root_layer_path = pecha_display_alignment["pecha_display"]
        translation_layer_path = pecha_display_alignment["translation"]

        root_basename = root_layer_path.split("/")[-2]
        translation_basename = translation_layer_path.split("/")[-2]

        root_layername = root_layer_path.split("/")[-1]
        translation_layername = translation_layer_path.split("/")[-1]

        return (root_basename, root_layername), (
            translation_basename,
            translation_layername,
        )

    def get_pecha_title(self, pecha_path: Path):
        pecha = Pecha.from_path(pecha_path)
        lang = pecha.metadata.language.value
        title = pecha.metadata.title
        if isinstance(title, dict):
            title = title.get(lang.lower()) or title.get(lang.upper())

        return title

    def serialize(
        self,
        root_opf: Path,
        translation_opf: Path,
        output_path: Path = SERIALIZED_ALIGNMENT_JSON_PATH,
    ) -> Path:
        self.set_root_metadata(root_opf)
        self.set_translation_metadata(translation_opf)

        pecha_title = self.get_pecha_title(root_opf)
        self.set_pecha_category(pecha_title)

        # Get the root and translation layer to serialize the layer(STAM) to JSON
        (root_basename, root_layername), (
            translation_basename,
            translation_layername,
        ) = self.get_pecha_display_aligment(translation_opf)

        self.set_root_content(root_opf, root_basename, root_layername)
        self.set_translation_content(
            translation_opf, translation_basename, translation_layername
        )

        # Write json to file
        json_output_path = output_path / "alignment.json"
        _mkdir_if_not(output_path)
        json_output = {
            "source": self.translation_json,
            "target": self.root_json,
        }

        write_json(json_output_path, json_output)
        return json_output_path
