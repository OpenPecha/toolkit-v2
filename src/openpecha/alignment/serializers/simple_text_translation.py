from pathlib import Path

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH


class SimpleTextTranslationSerializer(BaseAlignmentSerializer):
    def __init__(self):
        self.json_output_format = {
            "categories": [
                {"name": "Dummy Source Category", "enDesc": "", "enShortDesc": ""}
            ],
            "books": [],
        }

    def serialize(
        self,
        root_opf: Path,
        translation_opf: Path,
        output_path: Path = SERIALIZED_ALIGNMENT_JSON_PATH,
    ):
        pass
