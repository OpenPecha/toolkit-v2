from pathlib import Path
from typing import Dict, List, Tuple

from openpecha.config import get_logger
from openpecha.exceptions import (
    MetaDataMissingError,
    MetaDataValidationError,
    ParseNotReadyForThisAnnotation,
)
from openpecha.pecha import Pecha, annotation_path
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
from openpecha.pecha.parsers.docx.root.number_list_root import DocxRootParser

logger = get_logger(__name__)


class PechaOrgPechaMetaDataValidator:
    def validate_metadata(self, metadata: Dict):
        self.validate_metadata_dtype(metadata)
        self.validate_en_title(metadata)
        self.validate_bo_title(metadata)
        self.validate_lang_title(metadata)

    def ensure_no_forbidden_symbols(self, title: str):
        symbols = ["-", ":", "_", ".", "/"]
        for symbol in symbols:
            if symbol in title:
                logger.error(f"Title can't have symbol {symbol}")
                raise MetaDataValidationError(f"Title can't have symbol {symbol}")

    def validate_metadata_dtype(self, metadata: Dict):
        if not isinstance(metadata, dict):
            logger.error("Input metadata should be a dictionary")
            raise TypeError("Input metadata should be a dictionary")

    def validate_en_title(self, metadata: Dict):
        en_title = metadata.get("title", {}).get("en", None)

        if not en_title:
            logger.error("English title is missing in metadata")
            raise MetaDataMissingError("English title is missing in metadata")

        self.ensure_no_forbidden_symbols(en_title)

    def validate_bo_title(self, metadata: Dict):
        bo_title = metadata.get("title", {}).get("bo", None)

        if not bo_title:
            logger.error("Tibetan title is missing in metadata")
            raise MetaDataMissingError("Tibetan title is missing in metadata")

        self.ensure_no_forbidden_symbols(bo_title)

    def validate_lang_title(self, metadata: Dict):
        lang = metadata.get("lang", None)

        if not lang:
            logger.error("Language is missing in metadata")
            raise MetaDataMissingError("Language is missing in metadata")

        lang_title = metadata.get("title", {}).get(lang, None)
        if not lang_title:
            logger.error(f"{lang} title is missing in metadata")
            raise MetaDataMissingError(f"{lang} title is missing in metadata")

        self.ensure_no_forbidden_symbols(lang_title)


class DocxParser:
    def is_commentary_pecha(self, metadatas: List[Dict]) -> bool:
        """Checks if the given metadata corresponds to a commentary Pecha.

        Args:
            metadatas (List[Dict]): List of dictionaries containing metadata of the Pecha.

        Returns:
            bool: True if the Pecha is a commentary, otherwise False.
        """
        for metadata in metadatas:
            if "commentary_of" in metadata and metadata["commentary_of"]:
                return True
        return False

    def parse(
        self,
        docx_file: str | Path,
        annotation_type: AnnotationType | str,
        metadatas: List[Dict],
        pecha_id: str | None = None,
    ) -> Tuple[Pecha, annotation_path]:
        """Parses a DOCX file and generates a Pecha object based on its type.

        Args:
            docx_file (str | Path): Path to the DOCX file to be parsed.
            metadatas (List[Dict]): List of dictionaries, where each dictionary
                                    contains metadata of the Pecha.
            output_path (Path):
            pecha_id (str | None, optional): Pecha ID to be assigned. Defaults to None.

        Returns:
            Pecha: Pecha object.
        """

        # Accept both str and AnnotationType, convert str to AnnotationType
        if isinstance(annotation_type, str):
            try:
                annotation_type = AnnotationType(annotation_type)
            except ValueError:
                raise ParseNotReadyForThisAnnotation(
                    f"Invalid annotation type: {annotation_type}"
                )

        is_commentary = self.is_commentary_pecha(metadatas)

        if is_commentary:
            pecha, annotation_path = DocxSimpleCommentaryParser().parse(
                input=docx_file,
                annotation_type=annotation_type,
                metadata=metadatas[0],
                pecha_id=pecha_id,
            )
            return (pecha, annotation_path)
        else:
            pecha, annotation_path = DocxRootParser().parse(
                input=docx_file,
                annotation_type=annotation_type,
                metadata=metadatas[0],
                pecha_id=pecha_id,
            )
            return (pecha, annotation_path)
