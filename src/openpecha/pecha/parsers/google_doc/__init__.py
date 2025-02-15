from pathlib import Path
from typing import Dict, List, Union

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.google_doc.commentary.number_list import (
    DocxNumberListCommentaryParser,
)
from openpecha.pecha.parsers.google_doc.numberlist_translation import (
    DocxNumberListTranslationParser,
)


class DocxParser:
    def is_commentary_pecha(self, metadatas: List[Dict]) -> bool:
        for metadata in metadatas:
            if "commentary_of" in metadata and metadata["commentary_of"]:
                return True
        return False

    def parse(
        self,
        docx_file: Union[str, Path],
        metadatas: List[Dict],
        output_path: Path,
        pecha_id: Union[str, None] = None,
    ) -> Pecha:
        """_summary_

        Args:
            docx_file (Union[str, Path]): _description_
            metadatas (List[Dict]): list of dictionary. Each dictionary contains metadata of the pecha.
            output_path (Path): _description_
            pecha_id (Union[str, None], optional): _description_. Defaults to None.

        Returns:
            Pecha: _description_
        """
        is_commentary = self.is_commentary_pecha(metadatas)

        if is_commentary:
            return DocxNumberListCommentaryParser().parse(
                input=docx_file,
                metadata=metadatas[0],
                output_path=output_path,
                pecha_id=pecha_id,
            )
        else:
            return DocxNumberListTranslationParser().parse(
                input=docx_file,
                metadata=metadatas[0],
                output_path=output_path,
                pecha_id=pecha_id,
            )
