from pathlib import Path

from stam import AnnotationStore

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH, _mkdir_if_not
from openpecha.pecha import Pecha
from openpecha.utils import get_text_direction_with_lang, write_json


class SimpleTextTranslationSerializer(BaseAlignmentSerializer):
    def __init__(self):
        self.root_json = {
            "categories": [
                {
                    "name": "བོད་སྐད་ལ་ཕབ་བསྒྱུར་བྱེད་པའི་ཚོད་ལྟ།",
                    "heDesc": "",
                    "heShortDesc": "",
                }
            ],
            "books": [],
        }
        self.translation_json = {
            "categories": [
                {"name": "Test Translation", "enDesc": "", "enShortDesc": ""}
            ],
            "books": [],
        }

    def extract_metadata(self, pecha: Pecha):
        """
        Extract required metadata from opf
        """
        text_lang = pecha.metadata.language.value
        text_direction = get_text_direction_with_lang(text_lang)
        text_title = pecha.metadata.title
        text_title = (
            text_title if text_lang in ["bo", "en"] else f"{text_title}[{text_lang}]"
        )
        text_source = pecha.metadata.source if pecha.metadata.source else ""

        return {
            "title": text_title,
            "language": text_lang,
            "versionSource": text_source,
            "direction": text_direction,
            "completestatus": "done",
        }

    def set_root_metadata(self, root_opf_path: Path):
        root_pecha = Pecha.from_path(root_opf_path)
        self.root_json["books"].append(self.extract_metadata(root_pecha))

    def set_translation_metadata(self, translation_opf_path: Path):
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
        self.root_json["books"][0]["content"] = [segment_texts]  # type: ignore

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
        self.root_json["books"][0]["content"] = [segment_texts]  # type: ignore

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

    def serialize(
        self,
        root_opf: Path,
        translation_opf: Path,
        output_path: Path = SERIALIZED_ALIGNMENT_JSON_PATH,
    ) -> Path:
        self.set_root_metadata(root_opf)
        self.set_translation_metadata(translation_opf)

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
