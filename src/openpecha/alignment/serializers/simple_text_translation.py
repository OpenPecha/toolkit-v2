from pathlib import Path

from stam import AnnotationStore

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH, _mkdir_if_not
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
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

    def set_root_content(self, root_opf_path: Path):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """
        root_pecha = Pecha.from_path(root_opf_path)
        root_base_name = next(iter(root_pecha.bases))
        root_segment_layer = root_pecha.layers[root_base_name][
            LayerEnum.meaning_segment
        ][0]
        root_segment_texts = self.get_texts_from_layer(root_segment_layer)
        self.root_json["books"][0]["content"] = [root_segment_texts]  # type: ignore

    def set_translation_content(self, translation_opf_path: Path):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """
        translation_pecha = Pecha.from_path(translation_opf_path)
        translation_base_name = next(iter(translation_pecha.bases))
        translation_segment_layer = translation_pecha.layers[translation_base_name][
            LayerEnum.meaning_segment
        ][0]
        translation_segment_texts = self.get_texts_from_layer(translation_segment_layer)
        self.translation_json["books"][0]["content"] = [  # type: ignore
            translation_segment_texts
        ]

    def serialize(
        self,
        root_opf: Path,
        translation_opf: Path,
        output_path: Path = SERIALIZED_ALIGNMENT_JSON_PATH,
    ) -> Path:
        self.set_root_metadata(root_opf)
        self.set_translation_metadata(translation_opf)

        self.set_root_content(root_opf)
        self.set_translation_content(translation_opf)

        # Write json to file
        json_output_path = output_path / "alignment.json"
        _mkdir_if_not(output_path)
        json_output = {
            "source": self.translation_json,
            "target": self.root_json,
        }

        write_json(json_output_path, json_output)
        return json_output_path
