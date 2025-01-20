from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.utils import get_text_direction_with_lang


class SimpleTextCommentarySerializer(BaseAlignmentSerializer):
    def __init__(self):
        self.root_json_format = {
            "categories": [
                {
                    "name": "བོད་སྐད་ལ་ཚོད་ལྟའི་འགྲེལ་བཤད་",
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
            ann_data = {}
            for data in ann:
                ann_data[data.key().id()] = str(data.value())

            ann_text = "" if str(ann) == "\n" else str(ann).replace("\n", "<br>")

            if "root_idx_mapping" in ann_data:
                related_root_indices = parse_root_idx_mapping_string(
                    ann_data["root_idx_mapping"]
                )
                for related_root_idx in related_root_indices:
                    mapping_ann = f"<{related_root_idx}>"
                    text_with_mapping_ann.append(f"{mapping_ann}{ann_text}")
            else:
                text_with_mapping_ann.append(ann_text)

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
    ) -> Dict:
        self.set_metadata_to_json(root_opf, commentary_opf)
        self.fill_segments_to_json(root_opf, commentary_opf)

        json_output = {
            "source": self.commentary_json_format,
            "target": self.root_json_format,
        }

        return json_output


def parse_root_idx_mapping_string(root_idx_mapping: str) -> List[str]:
    related_root_indices = []
    for root_idx in root_idx_mapping.strip().split(","):
        root_idx = root_idx.strip()
        if "-" in root_idx:
            start, end = root_idx.split("-")
            related_root_indices.extend(
                [str(i) for i in range(int(start), int(end) + 1)]
            )
        else:
            related_root_indices.append(root_idx)
    return related_root_indices
