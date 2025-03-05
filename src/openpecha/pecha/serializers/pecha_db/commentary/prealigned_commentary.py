from pathlib import Path
from typing import Any, Dict, List

from pecha_org_tools.extract import CategoryExtractor
from stam import AnnotationStore

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataValidationError, PechaCategoryNotFoundError
from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.metadata import PechaMetaData
from openpecha.utils import get_text_direction_with_lang

logger = get_logger(__name__)


class PreAlignedCommentarySerializer:
    def extract_metadata(self, pecha: Pecha):
        """
        Extract neccessary metadata from opf for serialization to json
        """
        metadata: PechaMetaData = pecha.metadata

        if not isinstance(metadata.title, dict):
            logger.error(f"Title is not available in the Commentary Pecha {pecha.id}.")
            raise MetaDataValidationError(
                f"[Error] Commentary Pecha {pecha.id} has no English or Tibetan Title."
            )

        pecha_lang = pecha.metadata.language.value
        src_lang = "en" if pecha_lang == "bo" else pecha_lang
        source_title = metadata.title.get(src_lang.lower()) or metadata.title.get(
            src_lang.upper()
        )
        source_title = (
            source_title if src_lang == "en" else f"{source_title}[{src_lang}]"
        )
        target_lang = "bo"
        target_title = metadata.title.get(target_lang.lower()) or metadata.title.get(
            target_lang.upper()
        )

        src_metadata = {
            "title": source_title,
            "language": src_lang,
            "versionSource": metadata.source if metadata.source else "",
            "direction": get_text_direction_with_lang("en"),
            "completestatus": "done",
        }

        tgt_metadata = {
            "title": target_title,
            "language": target_lang,
            "versionSource": metadata.source if metadata.source else "",
            "direction": get_text_direction_with_lang("bo"),
            "completestatus": "done",
        }

        return src_metadata, tgt_metadata

    def get_category(self, category_name: str):
        """
        Input: title: Title of the pecha commentary which will be used to get the category format
        Process: Get the category format from the pecha.org categorizer package
        """

        try:
            categorizer = CategoryExtractor()
            category = categorizer.get_category(category_name)
        except Exception as e:
            logger.error(
                f"Category not found for pecha title: {category_name}. {str(e)}"
            )
            raise PechaCategoryNotFoundError(
                f"Category not found for pecha title: {category_name}. {str(e)}"
            )
        return category

    def add_root_reference_to_category(self, category: Dict[str, Any], root_title: str):
        """
        Modify the category format to the required format for pecha.org commentary
        """
        for lang in ["bo", "en"]:
            last_category = category[lang][-1]
            last_category.update(
                {
                    "base_text_titles": [root_title],
                    "base_text_mapping": "many_to_one",
                    "link": "Commentary",
                }
            )
        return category

    def get_categories(self, pecha: Pecha, root_title: str):
        """
        Set the category format to self.category attribute
        """

        title = pecha.metadata.title.get("bo") or pecha.metadata.title.get("BO")
        category = self.get_category(title)
        category = self.add_root_reference_to_category(category, root_title)

        return (category["en"], category["bo"])  # source and target category

    def get_first_layer_path(self, pecha: Pecha) -> Path:
        return next(pecha.layer_path.rglob("*.json"))

    def base_update(self, src_pecha: Pecha, tgt_pecha: Pecha) -> Path:
        """
        1. Take the layer from src pecha
        2. Migrate the layer to tgt pecha using base update
        """
        src_base_name = list(src_pecha.bases.keys())[0]
        tgt_base_name = list(tgt_pecha.bases.keys())[0]
        tgt_pecha.merge_pecha(src_pecha, src_base_name, tgt_base_name)

        src_layer_name = next(src_pecha.layer_path.rglob("*.json")).name
        new_layer_path = tgt_pecha.layer_path / tgt_base_name / src_layer_name
        return new_layer_path

    def extract_root_anns(self, layer: AnnotationStore) -> Dict:
        """
        Extract annotation from layer(STAM)
        """
        anns = {}
        for ann in layer.annotations():
            start, end = ann.offset().begin().value(), ann.offset().end().value()
            ann_metadata = {}
            for data in ann:
                ann_metadata[data.key().id()] = str(data.value())
            anns[int(ann_metadata["root_idx_mapping"])] = {
                "Span": {"start": start, "end": end},
                "text": str(ann),
                "root_idx_mapping": int(ann_metadata["root_idx_mapping"]),
            }
        return anns

    def map_layer_to_layer(
        self, src_layer: AnnotationStore, tgt_layer: AnnotationStore
    ):
        """
        1. Extract annotations from source and target layers
        2. Map the annotations from source to target layer
        src_layer -> tgt_layer (One to Many)
        """
        mapping: Dict = {}

        src_anns = self.extract_root_anns(src_layer)
        tgt_anns = self.extract_root_anns(tgt_layer)

        for src_idx, src_span in src_anns.items():
            src_start, src_end = src_span["Span"]["start"], src_span["Span"]["end"]
            mapping[src_idx] = []

            for tgt_idx, tgt_span in tgt_anns.items():
                tgt_start, tgt_end = tgt_span["Span"]["start"], tgt_span["Span"]["end"]

                # Check for mapping conditions
                is_overlap = (
                    src_start <= tgt_start < src_end or src_start < tgt_end <= src_end
                )
                is_contained = tgt_start < src_start and tgt_end > src_end
                is_edge_overlap = tgt_start == src_end or tgt_end == src_start
                if is_overlap or is_contained and not is_edge_overlap:
                    mapping[src_idx].append(tgt_idx)

        # Sort the mapping by source indices
        return dict(sorted(mapping.items()))

    def get_root_pechas_mapping(
        self, root_pecha: Pecha, root_display_pecha: Pecha
    ) -> Dict[int, List]:
        """
        Get segmentation mapping from root_pecha -> root_display_pecha
        """
        display_layer_path = self.get_first_layer_path(root_display_pecha)
        new_tgt_layer = self.base_update(root_pecha, root_display_pecha)

        display_layer = AnnotationStore(file=str(display_layer_path))
        transfer_layer = AnnotationStore(file=str(new_tgt_layer))

        map = self.map_layer_to_layer(transfer_layer, display_layer)

        # Clean up the layer
        new_tgt_layer.unlink()
        return map

    def get_serialized_commentary(
        self, root_display_pecha: Pecha, root_pecha: Pecha, commentary_pecha: Pecha
    ) -> List[str]:
        def is_empty(text):
            """Check if text is empty or contains only newlines."""
            return not text.strip().replace("\n", "")

        root_map = self.get_root_pechas_mapping(root_pecha, root_display_pecha)

        root_display_layer_path = self.get_first_layer_path(root_display_pecha)
        root_display_anns = self.extract_root_anns(
            AnnotationStore(file=str(root_display_layer_path))
        )

        root_layer_path = self.get_first_layer_path(root_pecha)
        root_anns = self.extract_root_anns(AnnotationStore(file=str(root_layer_path)))

        commentary_layer_path = self.get_first_layer_path(commentary_pecha)
        commentary_anns = get_anns(AnnotationStore(file=str(commentary_layer_path)))
        serialized_content = []
        for ann in commentary_anns:
            root_indices = parse_root_mapping(ann["root_idx_mapping"])
            root_idx = root_indices[0]
            commentary_text = ann["text"]

            # Skip if commentary is empty
            is_commentary_empty = is_empty(commentary_text)
            if is_commentary_empty:
                continue

            # Dont include mapping if root is empty
            idx_not_in_root = root_idx not in root_anns
            is_root_empty = is_empty(root_anns[root_idx]["text"])
            if is_commentary_empty or idx_not_in_root or is_root_empty:
                serialized_content.append(commentary_text)
                continue

            # Dont include mapping if root_display is empty
            root_display_idx = root_map[root_idx][0]
            idx_not_in_root_display = root_display_idx not in root_display_anns
            is_root_display_empty = is_empty(
                root_display_anns[root_display_idx]["text"]
            )
            if idx_not_in_root_display or is_root_display_empty:
                serialized_content.append(commentary_text)
                continue

            serialized_content.append(f"<1><{root_display_idx}>{commentary_text}")
        return serialized_content

    def get_pecha_en_title(self, pecha: Pecha):
        metadata: PechaMetaData = pecha.metadata

        if not isinstance(metadata.title, dict):
            logger.error(
                f"Title data type is not dictionary in the Root Pecha {pecha.id}."
            )
            raise MetaDataValidationError(
                f"[Error] Root Pecha {pecha.id} title data type is not dictionary."
            )

        if "en" not in metadata.title and "EN" not in metadata.title:
            logger.error(
                f"English title is not available in the Root Pecha {pecha.id}."
            )
            raise MetaDataValidationError(
                f"[Error] Root Pecha {pecha.id} has no English Title."
            )

        root_en_title = metadata.title.get("en") or metadata.title.get("EN")
        return root_en_title

    def serialize(
        self, root_display_pecha: Pecha, root_pecha: Pecha, commentary_pecha: Pecha
    ):
        src_book, tgt_book = [], []
        src_metadata, tgt_metadata = self.extract_metadata(commentary_pecha)
        src_book.append(src_metadata)
        tgt_book.append(tgt_metadata)

        root_en_title = self.get_pecha_en_title(root_display_pecha)
        src_category, tgt_category = self.get_categories(
            commentary_pecha, root_en_title
        )

        src_content: List[List[str]] = []
        tgt_content = self.get_serialized_commentary(
            root_display_pecha, root_pecha, commentary_pecha
        )

        src_book[0]["content"] = src_content
        tgt_book[0]["content"] = tgt_content

        serialized_json = {
            "source": {"categories": src_category, "books": src_book},
            "target": {"categories": tgt_category, "books": tgt_book},
        }
        logger.info(f"Pecha {commentary_pecha.id} is serialized successfully.")
        return serialized_json


def parse_root_mapping(mapping: str) -> List[int]:
    res = []
    for map in mapping.strip().split(","):
        map = map.strip()
        if "-" in map:
            start, end = map.split("-")
            res.extend(list(range(int(start), int(end) + 1)))
        else:
            res.append(int(map))

    res.sort()
    return res
