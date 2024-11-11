from pathlib import Path

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH, _mkdir_if_not
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.utils import write_json


class SimpleTextTranslationSerializer(BaseAlignmentSerializer):
    def __init__(self):
        self.root_json_format = {
            "categories": [
                {"name": "Dummy Source Category", "enDesc": "", "enShortDesc": ""}
            ],
            "books": [],
        }
        self.translation_json_format = {
            "categories": [
                {"name": "Dummy Source Category", "enDesc": "", "enShortDesc": ""}
            ],
            "books": [],
        }

    def set_metadata_to_json(self, root_opf_path: Path, translation_opf_path: Path):
        root_pecha = Pecha.from_path(root_opf_path)
        required_root_pecha_metadatas = {
            "title": root_pecha.metadata.title,
            "language": root_pecha.metadata.language.value,
            "versionSource": root_pecha.metadata.source,
            "direction": "ltr",  # To be updated dynamically
        }
        self.root_json_format["books"].append(required_root_pecha_metadatas)

        translation_pecha = Pecha.from_path(translation_opf_path)
        required_translation_pecha_metadatas = {
            "title": translation_pecha.metadata.title,
            "language": translation_pecha.metadata.language.value,
            "versionSource": translation_pecha.metadata.source,
            "direction": "ltr",  # To be updated dynamically
        }

        self.translation_json_format["books"].append(
            required_translation_pecha_metadatas
        )

    def fill_segments_to_json(self, root_opf_path: Path, translation_opf_path: Path):
        root_pecha = Pecha.from_path(root_opf_path)
        translation_pecha = Pecha.from_path(translation_opf_path)

        # Get one txt file from root and translation opf
        root_base_name = list(root_pecha.bases.keys())[0]
        translation_base_name = list(translation_pecha.bases.keys())[0]

        # Read meaning segments from root and translation opf
        root_segment_layer = root_pecha.layers[root_base_name][
            LayerEnum.meaning_segment
        ][0]
        root_segment_texts = []
        for root_segment_ann in root_segment_layer:
            root_segment_text = str(root_segment_ann)
            root_segment_text = "" if root_segment_text == "\n" else root_segment_text
            root_segment_texts.append(root_segment_text)

        translation_segment_layer = translation_pecha.layers[translation_base_name][
            LayerEnum.meaning_segment
        ][0]
        translation_segment_texts = []
        for translation_segment_ann in translation_segment_layer:
            translation_segment_text = str(translation_segment_ann)
            translation_segment_text = (
                "" if translation_segment_text == "\n" else translation_segment_text
            )
            translation_segment_texts.append(translation_segment_text)

        # Fill segments to json

        self.root_json_format["books"][0]["content"] = [root_segment_texts]  # type: ignore
        self.translation_json_format["books"][0]["content"] = [  # type: ignore
            translation_segment_texts
        ]

    def serialize(
        self,
        root_opf: Path,
        translation_opf: Path,
        output_path: Path = SERIALIZED_ALIGNMENT_JSON_PATH,
    ):
        self.set_metadata_to_json(root_opf, translation_opf)
        self.fill_segments_to_json(root_opf, translation_opf)

        # Write json to file
        json_output_path = output_path / "alignment.json"
        _mkdir_if_not(output_path)
        json_output = {
            "source": self.translation_json_format,
            "target": self.root_json_format,
        }

        write_json(json_output_path, json_output)
