from pathlib import Path

from stam import AnnotationStore

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.config import SERIALIZED_ALIGNMENT_JSON_PATH, _mkdir_if_not
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.utils import get_text_direction_with_lang, write_json


class SimpleTextCommentarySerializer(BaseAlignmentSerializer):
    def __init__(self):
        self.root_json_format = {
            "categories": [
                {
                    "name": "བོད་སྐད་ལ་ཕབ་བསྒྱུར་བྱེད་པའི་ཚོད་ལྟ།",
                    "heDesc": "",
                    "heShortDesc": "",
                }
            ],
            "books": [],
        }
        self.commentary_json_format = {
            "categories": [
                {"name": "Test Commentary", "enDesc": "", "enShortDesc": ""}
            ],
            "books": [],
        }

    def extract_metadata(self, pecha: Pecha):
        """
        Extract metadata from opf
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

    def set_metadata_to_json(self, root_opf_path: Path, commentary_opf_path: Path):
        """
        Extract only required metadata from root and commentary opf and set it to json format
        """
        root_pecha = Pecha.from_path(root_opf_path)
        commentary_pecha = Pecha.from_path(commentary_opf_path)

        self.root_json_format["books"].append(self.extract_metadata(root_pecha))
        self.commentary_json_format["books"].append(
            self.extract_metadata(commentary_pecha)
        )

    @staticmethod
    def get_root_texts_from_layer(layer: AnnotationStore):
        """
        Extract texts from layer
        1.If text is a newline, replace it with empty string
        2.Replace newline with <br>
        """
        text_with_mapping_ann = []
        for ann in layer:
            ann_data = {}
            for data in ann:
                ann_data[data.key().id()] = str(data.value())

            mapping_ann = f"<{ann_data['root_idx']}>" if "root_idx" in ann_data else ""

            ann_text = "" if str(ann) == "\n" else str(ann).replace("\n", "<br>")
            text_with_mapping_ann.append(f"{mapping_ann}{ann_text}")

        return text_with_mapping_ann

    @staticmethod
    def get_commentary_texts_from_layer(layer: AnnotationStore):
        """
        Extract texts from layer
        1.If text is a newline, replace it with empty string
        2.Replace newline with <br>
        """
        text_with_mapping_ann = []
        for ann in layer:
            if str(ann) == "\n":
                text_with_mapping_ann.append("")
            else:
                text_with_mapping_ann.append(str(ann).replace("\n", "<br>"))

        return text_with_mapping_ann

    def fill_segments_to_json(self, root_opf_path: Path, commentary_opf_path: Path):
        """
        Processes:
        1. Get the first txt file from root and commentary opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """
        root_pecha = Pecha.from_path(root_opf_path)
        commentary_pecha = Pecha.from_path(commentary_opf_path)

        # Get one txt file from root and commentary opf
        root_base_name = next(iter(root_pecha.bases))
        commentary_base_name = next(iter(commentary_pecha.bases))

        # Read meaning segments from root and commentary opf
        root_segment_layer = root_pecha.layers[root_base_name][
            LayerEnum.meaning_segment
        ][0]
        commentary_segment_layer = commentary_pecha.layers[commentary_base_name][
            LayerEnum.meaning_segment
        ][0]

        root_segment_texts = self.get_root_texts_from_layer(root_segment_layer)
        commentary_segment_texts = self.get_commentary_texts_from_layer(
            commentary_segment_layer
        )

        # Fill segments to json
        self.root_json_format["books"][0]["content"] = [root_segment_texts]  # type: ignore
        self.commentary_json_format["books"][0]["content"] = [  # type: ignore
            commentary_segment_texts
        ]

    def serialize(
        self,
        root_opf: Path,
        commentary_opf: Path,
        output_path: Path = SERIALIZED_ALIGNMENT_JSON_PATH,
    ) -> Path:
        self.set_metadata_to_json(root_opf, commentary_opf)
        self.fill_segments_to_json(root_opf, commentary_opf)

        # Write json to file
        json_output_path = output_path / "alignment.json"
        _mkdir_if_not(output_path)
        json_output = {
            "source": self.commentary_json_format,
            "target": self.root_json_format,
        }

        write_json(json_output_path, json_output)
        return json_output_path
