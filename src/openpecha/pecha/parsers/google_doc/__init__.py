from pathlib import Path
from typing import Dict, Union

from openpecha.pecha.parsers.google_doc.commentary.number_list import (
    DocxNumberListCommentaryParser,
)
from openpecha.pecha.parsers.google_doc.numberlist_translation import (
    DocxNumberListTranslationParser,
)


class DocxParser:
    def parse(
        self,
        docx_file: Union[str, Path],
        metadata: Dict,
        is_commentary: bool,
        output_path: Path,
        pecha_id: Union[str, None] = None,
    ):
        """
                Parses the document based on the metadata and returns the parsed result.
        x
                Returns:
                    Parsed result (Pecha).
        """
        if is_commentary:
            return DocxNumberListTranslationParser().parse(
                input=docx_file,
                metadata=metadata,
                output_path=output_path,
                pecha_id=pecha_id,
            )
        else:
            return DocxNumberListCommentaryParser().parse(
                input=docx_file,
                metadata=metadata,
                output_path=output_path,
                pecha_id=pecha_id,
            )
