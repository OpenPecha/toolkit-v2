from typing import Dict, List, Union

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.pecha import Pecha, get_pecha_with_id
from openpecha.pecha.metadata import Language
from openpecha.utils import chunk_strings, get_text_direction_with_lang


class TextTranslationSerializer:
    def get_pecha_category(self, pecha: Pecha):
        """
        Set pecha category both in english and tibetan in the JSON output.
        """
        pecha_title = self.get_pecha_bo_title(pecha)
        category_extractor = CategoryExtractor()
        categories = category_extractor.get_category(pecha_title)
        return categories["bo"], categories["en"]

    def get_metadata_for_pecha_org(self, pecha: Pecha, lang: Union[str, None] = None):
        """
        Extract required metadata from opf
        """
        if not lang:
            lang = pecha.metadata.language.value
        direction = get_text_direction_with_lang(lang)
        title = pecha.metadata.title
        if isinstance(title, dict):
            title = title.get(lang.lower(), None) or title.get(  # type: ignore
                lang.upper(), None  # type: ignore
            )
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

    def get_root_content(self, pecha: Pecha, pecha_layer_path: str):
        segment_layer = AnnotationStore(
            file=pecha.pecha_path.parent.joinpath(pecha_layer_path).as_posix()
        )
        segments = self.get_texts_from_layer(segment_layer)
        return chunk_strings(segments)

    def get_translation_content(self, pecha: Pecha, layer_path: str):
        """
        Processes:
        1. Get the first txt file from root and translation opf
        2. Read meaning layer from the base txt file from each opfs
        3. Read segment texts and fill it to 'content' attribute in json formats
        """

        translation_segment_layer = AnnotationStore(
            file=pecha.pecha_path.parent.joinpath(layer_path).as_posix()
        )

        segments: Dict[int, List[str]] = {}
        for ann in translation_segment_layer:
            ann_data = {}
            for data in ann:
                ann_data[str(data.key().id())] = data.value().get()

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

        return chunk_strings(translation_segments)

    def get_pecha_bo_title(self, pecha: Pecha):
        """
        Get tibetan title from the Pecha metadata
        """
        title = pecha.metadata.title
        if isinstance(title, dict):
            title = title.get("bo") or title.get("BO")

        return title

    def serialize(
        self,
        pecha: Pecha,
        alignment_data: Union[Dict, None] = None,
    ) -> Dict:

        if alignment_data is None:
            root_pecha = pecha
            translation_pecha = None

            root_layer_path = next(root_pecha.layer_path.rglob("*.json"))
            relative_layer_path = root_layer_path.relative_to(
                root_pecha.pecha_path.parent
            )
            root_content = self.get_root_content(root_pecha, relative_layer_path)
            translation_content = []
        else:
            root_pecha_id = alignment_data["root"].split("/")[0]
            root_pecha = get_pecha_with_id(root_pecha_id)
            translation_pecha = pecha

            root_content = self.get_root_content(root_pecha, alignment_data["root"])
            translation_content = self.get_translation_content(
                translation_pecha, alignment_data["translation"]
            )

        # Get pecha category from pecha_org_tools package and set to JSON
        bo_category, en_category = self.get_pecha_category(root_pecha)

        root_json: Dict[str, List] = {
            "categories": bo_category,
            "books": [
                {**self.get_metadata_for_pecha_org(root_pecha), "content": root_content}
            ],
        }
        translation_json: Dict[str, List] = {
            "categories": en_category,
            "books": [
                {
                    **self.get_metadata_for_pecha_org(translation_pecha),
                    "content": translation_content,
                }
                if translation_pecha
                else {
                    **self.get_metadata_for_pecha_org(
                        root_pecha, Language.english.value
                    ),
                    "content": translation_content,
                }
            ],
        }

        # Set the content for source and target and set it to JSON
        serialized_json = {
            "source": translation_json,
            "target": root_json,
        }

        return serialized_json
