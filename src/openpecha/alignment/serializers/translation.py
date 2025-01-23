from typing import Dict, List

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.alignment.alignment import AlignmentEnum
from openpecha.alignment.serializers import BaseAlignmentSerializer
from openpecha.pecha import Pecha
from openpecha.utils import chunk_strings, get_text_direction_with_lang


class TextTranslationSerializer(BaseAlignmentSerializer):
    def __init__(self):
        self.root_json: Dict[str, List] = {
            "categories": [],
            "books": [],
        }
        self.translation_json: Dict[str, List] = {
            "categories": [],
            "books": [],
        }

        self.root_basename: str
        self.translation_basename: str

        self.root_layername: str
        self.translation_layername: str

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

    def set_root_content(self, pecha: Pecha):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """
        segment_layer = AnnotationStore(
            file=pecha.layer_path.joinpath(
                self.root_basename, self.root_layername
            ).as_posix()
        )
        segments = self.get_texts_from_layer(segment_layer)
        self.root_json["books"][0]["content"] = chunk_strings(segments)

    def set_translation_content(self, pecha: Pecha, is_pecha_display: bool):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """

        translation_segment_layer = AnnotationStore(
            file=pecha.layer_path.joinpath(
                self.translation_basename, self.translation_layername
            ).as_posix()
        )

        segments: Dict[int, List[str]] = {}
        for ann in translation_segment_layer:
            ann_data = {}
            for data in ann:
                ann_data[str(data.key().id())] = data.value().get()

            if is_pecha_display:
                if "alignment_mapping" in ann_data:
                    for map in ann_data["alignment_mapping"]:
                        root_map = map[0]
                        if root_map in segments:
                            segments[root_map].append(str(ann))
                        else:
                            segments[root_map] = [str(ann)]
            else:
                if "root_idx_mapping" in ann_data:
                    root_map = int(ann_data["root_idx_mapping"])
                    segments[root_map] = [str(ann)]

        max_root_idx = max(segments.keys())
        translation_segments = []
        for root_idx in range(1, max_root_idx + 1):
            if root_idx in segments:
                translation_segments.append("".join(segments[root_idx]))
            else:
                translation_segments.append("")

        self.translation_json["books"][0]["content"] = chunk_strings(
            translation_segments
        )

    def get_root_and_translation_layer(
        self, root_pecha: Pecha, translation_pecha: Pecha, is_pecha_display: bool
    ):
        """
        Get the root layer and translation layer to serialize the layer(STAM) to JSON
        1.First it checks if the 'pecha_display_alignments' contains in the metadata (from translation opf)
        2.Select the first meaning segment layer found in each of the opf
        """
        if is_pecha_display:
            assert (
                AlignmentEnum.pecha_display_alignments.value
                in translation_pecha.metadata.source_metadata
            ), f"pecha display alignment not present to serialize in translation Pecha {translation_pecha.id}"
            pecha_display_alignments = translation_pecha.metadata.source_metadata[
                AlignmentEnum.pecha_display_alignments.value
            ]
            for alignment in pecha_display_alignments:
                root_basename, root_layer = (
                    alignment["pecha_display"].split("/")[-2],
                    alignment["pecha_display"].split("/")[-1],
                )
                translation_basename, translation_layer = (
                    alignment["translation"].split("/")[-2],
                    alignment["translation"].split("/")[-1],
                )
                if root_pecha.get_layer_by_filename(
                    root_basename, root_layer
                ) and translation_pecha.get_layer_by_filename(
                    translation_basename, translation_layer
                ):
                    self.root_basename = root_basename
                    self.translation_basename = translation_basename
                    self.root_layername = root_layer
                    self.translation_layername = translation_layer
                    return None
            raise LookupError(
                f"No proper pecha display alignment found in Root {root_pecha.id} and translation {translation_pecha.id} to serialize"
            )
        else:
            assert (
                AlignmentEnum.translation_alignment.value
                in translation_pecha.metadata.source_metadata
            ), f"translation alignment not present to serialize in translation Pecha {translation_pecha.id}"
            translation_alignments = translation_pecha.metadata.source_metadata[
                AlignmentEnum.translation_alignment.value
            ]
            for alignment in translation_alignments:
                root_basename, root_layer = (
                    alignment["source"].split("/")[-2],
                    alignment["source"].split("/")[-1],
                )
                translation_basename, translation_layer = (
                    alignment["target"].split("/")[-2],
                    alignment["target"].split("/")[-1],
                )
                if root_pecha.get_layer_by_filename(
                    root_basename, root_layer
                ) and translation_pecha.get_layer_by_filename(
                    translation_basename, translation_layer
                ):
                    self.root_basename = root_basename
                    self.translation_basename = translation_basename
                    self.root_layername = root_layer
                    self.translation_layername = translation_layer
                    return None
            raise LookupError(
                f"No proper translation alignment found in Root {root_pecha.id} and translation {translation_pecha.id} to serialize"
            )

    def get_pecha_title(self, pecha: Pecha):
        lang = pecha.metadata.language.value
        title = pecha.metadata.title
        if isinstance(title, dict):
            title = title.get(lang.lower()) or title.get(lang.upper())

        return title

    def serialize(
        self,
        root_pecha: Pecha,
        translation_pecha: Pecha,
        is_pecha_display: bool = True,
    ) -> Dict:

        # Extract metadata from opf and set to JSON
        self.root_json["books"].append(self.extract_metadata(root_pecha))
        self.translation_json["books"].append(self.extract_metadata(translation_pecha))

        # Get pecha category from pecha_org_tools package and set to JSON
        pecha_title = self.get_pecha_title(root_pecha)
        self.set_pecha_category(pecha_title)

        # Get the root and translation layer to serialize the layer(STAM) to JSON
        self.get_root_and_translation_layer(
            root_pecha, translation_pecha, is_pecha_display
        )

        # Set the content for source and target and set it to JSON
        self.set_root_content(root_pecha)
        self.set_translation_content(translation_pecha, is_pecha_display)

        json_output = {
            "source": self.translation_json,
            "target": self.root_json,
        }

        return json_output
