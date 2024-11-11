from pathlib import Path

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH
from openpecha.pecha import Pecha


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
            "language": root_pecha.metadata.language,
            "versionSource": root_pecha.metadata.source,
            "content": [],
            "direction": "ltr",  # To be updated dynamically
        }
        self.root_json_format["books"].append(required_root_pecha_metadatas)

        translation_pecha = Pecha.from_path(translation_opf_path)
        required_translation_pecha_metadatas = {
            "title": translation_pecha.metadata.title,
            "language": translation_pecha.metadata.language,
            "versionSource": translation_pecha.metadata.source,
            "content": [],
            "direction": "ltr",  # To be updated dynamically
        }

        self.translation_json_format["books"].append(
            required_translation_pecha_metadatas
        )

    def fill_segments_to_json(self, root_opf_path: Path, translation_opf_path: Path):
        pass

    def serialize(
        self,
        root_opf: Path,
        translation_opf: Path,
        output_path: Path = SERIALIZED_ALIGNMENT_JSON_PATH,
    ):
        self.set_metadata_to_json(root_opf, translation_opf)
        pass
