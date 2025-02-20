from pathlib import Path
from typing import Dict, List, Union

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
from openpecha.pecha.parsers.docx.numberlist_translation import (
    DocxNumberListTranslationParser,
)


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
        docx_file: Union[str, Path],
        metadatas: List[Dict],
        pecha_id: Union[str, None] = None,
    ) -> Pecha:
        """Parses a DOCX file and generates a Pecha object based on its type.

        Args:
            docx_file (Union[str, Path]): Path to the DOCX file to be parsed.
            metadatas (List[Dict]): List of dictionaries, where each dictionary
                                    contains metadata of the Pecha.
            output_path (Path):
            pecha_id (Union[str, None], optional): Pecha ID to be assigned. Defaults to None.

        Returns:
            Pecha: Pecha object.
        """
        is_commentary = self.is_commentary_pecha(metadatas)

        if is_commentary:
            return DocxSimpleCommentaryParser().parse(
                input=docx_file,
                metadata=metadatas[0],
                pecha_id=pecha_id,
            )
        else:
            return DocxNumberListTranslationParser().parse(
                input=docx_file,
                metadata=metadatas[0],
                pecha_id=pecha_id,
            )
